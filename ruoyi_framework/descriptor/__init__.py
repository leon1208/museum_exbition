# -*- coding: utf-8 -*-
"""
descriptor 包用于存放与 AOP/注解语义相关的工具。
"""

from .custom_cacheable import custom_cacheable
from .custom_cache_evict import custom_cache_evict

__all__ = ["custom_cacheable", "custom_cache_evict"]

