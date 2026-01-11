from minio import Minio
import ffmpeg
from datetime import timedelta
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
        
    # 通过ffmpeg获取一个音频文件的时长
    @classmethod
    def get_audio_duration_from_minio(
        cls,
        object_name: str,
        bucket: str = CONFIG_CACHE.get('flask.MINIO_BUCKET')
    ) -> float:
        client = cls.get_client()
        url = client.presigned_get_object(
            bucket,
            object_name,
            expires = timedelta(minutes=5)  # 5 分钟
        )
        probe = ffmpeg.probe(url)
        return float(probe["format"]["duration"])
    
    # 通过ffmpeg获取一个视频文件的时长和首帧
    @classmethod
    def get_video_duration_and_first_frame(
        cls,
        object_name: str,
        bucket: str = CONFIG_CACHE.get('flask.MINIO_BUCKET')
    ) -> tuple[float, str]:
        client = cls.get_client()
        url = client.presigned_get_object(
            bucket,
            object_name,
            expires = timedelta(minutes=5)  # 5 分钟
        )
        probe = ffmpeg.probe(url)
        duration = float(probe["format"]["duration"])

        #将object_name的后缀替换为.jpg
        object_name_jpg = object_name.replace(object_name.split('.')[-1], 'jpg')
        #提取首帧
        first_frame = cls.extract_first_frame_bytes(url, object_name_jpg)
        return duration, first_frame

    @classmethod
    def extract_first_frame_bytes(cls, url: str, object_name_jpg: str) -> str:
        (out, _) = (
            ffmpeg
            .input(url, ss=0.1)
            .output(
                'pipe:',
                vframes=1,
                format='image2pipe',
                vcodec='mjpeg'
            )
            .run(capture_stdout=True, capture_stderr=True)
        )
        # 上传到 MinIO
        import io
        stat = cls.upload_file(object_name_jpg, io.BytesIO(out), 'image/jpeg')
        return stat.object_name
