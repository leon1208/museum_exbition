# -*- coding: utf-8 -*-
"""
自定义缓存清理装饰器，对应 Java 版本的 `@CustomCacheEvict`。
执行目标函数后，根据前缀/字段路径/参数组合构造通配符 Key，并批量删除 Redis 缓存。
"""

from __future__ import annotations

import functools
import inspect
import logging
from typing import Any, Callable, Iterable, Mapping, MutableMapping, Sequence

from werkzeug.local import LocalProxy

from .custom_cacheable import (
    ARGS_HASH_PREFIX,
    COMMON_SEPARATOR,
    _get_value_by_field_path,
    _hash_arguments,
    _resolve_redis_client,
)

logger = logging.getLogger(__name__)

__all__ = ["custom_cache_evict"]


def custom_cache_evict(
    key_prefixes: Sequence[str],
    key_fields: Sequence[str] | None = None,
    use_query_params_as_key: bool = False,
) -> Callable:
    """
    Redis 缓存清理装饰器。

    Args:
        key_prefixes: 缓存前缀数组，必填，对应待清理的一组 Key。
        key_fields:   与前缀一一对应的字段路径，允许缺省；缺省时直接按前缀通配符清理。
        use_query_params_as_key: 是否将函数参数序列化为 Key 的一部分（需与存储端保持一致）。
    """

    if not key_prefixes:
        raise ValueError("key_prefixes 不能为空")

    def decorator(func: Callable) -> Callable:
        signature = inspect.signature(func)

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            client = _resolve_redis_client()
            if client is None:
                return result

            params = _bind_arguments(signature, *args, **kwargs)
            args_hash = _hash_arguments(params) if use_query_params_as_key else None

            for idx, prefix in enumerate(key_prefixes):
                if not prefix:
                    continue

                pattern = prefix
                field_value = _extract_field_value(params, key_fields, idx)

                if field_value not in (None, ""):
                    pattern = f"{pattern}{COMMON_SEPARATOR}{field_value}"

                if use_query_params_as_key and args_hash:
                    pattern = f"{pattern}{COMMON_SEPARATOR}{ARGS_HASH_PREFIX}:{args_hash}"

                pattern = f"{pattern}*"
                _delete_keys_by_pattern(client, pattern)

            return result

        return wrapper

    return decorator


def _bind_arguments(signature: inspect.Signature, *args: Any, **kwargs: Any) -> MutableMapping[str, Any]:
    """
    对函数参数做一次绑定，得到“参数名 -> 值”的映射，便于后续取字段。
    """

    bound_args = signature.bind_partial(*args, **kwargs)
    bound_args.apply_defaults()
    return bound_args.arguments


def _extract_field_value(
    params: Mapping[str, Any],
    key_fields: Sequence[str] | None,
    index: int,
) -> Any:
    """
    根据 key_fields 配置提取对应的嵌套字段值，超过范围时返回 None。
    """

    if not key_fields or index >= len(key_fields):
        return None
    field_path = key_fields[index]
    if not field_path:
        return None
    return _get_value_by_field_path(params, field_path)


def _delete_keys_by_pattern(client: LocalProxy, pattern: str) -> None:
    """
    使用 scan_iter 增量拉取匹配 Key 并删除，避免阻塞 Redis。
    """

    try:
        pipeline = client.pipeline(transaction=False)
        batch: list[str] = []
        for key in client.scan_iter(match=pattern, count=200):
            batch.append(key)
            if len(batch) >= 200:
                _execute_delete_batch(pipeline, batch)
                batch.clear()
        if batch:
            _execute_delete_batch(pipeline, batch)
    except Exception as exc:  # noqa: BLE001
        logger.warning("按模式删除缓存失败 %s: %s", pattern, exc)


def _execute_delete_batch(pipeline: Any, batch: Iterable[str]) -> None:
    """
    批量删除 Key 并立即执行 pipeline。
    """

    try:
        for key in batch:
            pipeline.delete(key)
        pipeline.execute()
    except Exception as exc:  # noqa: BLE001
        logger.warning("批量删除缓存失败: %s", exc)

