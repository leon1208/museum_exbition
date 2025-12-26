from minio import Minio
from ruoyi_common.ruoyi.config import CONFIG_CACHE

class MinioUtil:

    _client: Minio = None

    @classmethod
    def get_client(cls) -> Minio:
        if cls._client is None:
            cls._client = Minio(
                endpoint=CONFIG_CACHE.get('flask.MINIO_ENDPOINT'),
                access_key=CONFIG_CACHE.get('flask.MINIO_ACCESS_KEY'),
                secret_key=CONFIG_CACHE.get('flask.MINIO_SECRET_KEY'),
                secure=False
            )
        return cls._client

    @classmethod
    def upload_file(
        cls,
        object_name: str,
        file_stream,
        content_type: str,
        bucket_name: str = CONFIG_CACHE.get('flask.MINIO_BUCKET')
    ):
        client = cls.get_client()

        # bucket 不存在就创建
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)

        client.put_object(
            bucket_name=bucket_name,
            object_name=object_name,
            data=file_stream,
            length=-1,
            part_size=10 * 1024 * 1024,
            content_type=content_type
        )

        return client.stat_object(bucket_name, object_name)
        
