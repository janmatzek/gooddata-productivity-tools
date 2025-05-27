import io
from typing import IO, cast

import boto3
from botocore.response import StreamingBody
from mypy_boto3_s3.service_resource import (
    Bucket,
    Object,
    S3ServiceResource,
)


class ClientS3:
    def __init__(self, profile_name: str) -> None:
        self.profile_name = profile_name
        self.session = boto3.Session(profile_name=profile_name)
        self.resource: S3ServiceResource = self.session.resource("s3")

    @staticmethod
    def get_bucket(s3_resource: S3ServiceResource, bucket_name: str) -> Bucket:
        """Get an S3 bucket using the specified resource and bucket name."""
        return s3_resource.Bucket(name=bucket_name)

    @staticmethod
    def get_object(bucket: Bucket, object_key: str) -> Object:
        """Get an object from the specified bucket using the object key."""
        return bucket.Object(object_key)

    @staticmethod
    def get_object_streaming_body(obj: Object) -> StreamingBody:
        """Get the streaming body of the specified object."""
        return obj.get()["Body"]

    def get_object_stream(self, obj: Object) -> io.TextIOWrapper:
        """Returns text stream of the specified object."""
        body: StreamingBody = self.get_object_streaming_body(obj)

        # cast the body to IO[bytes] to avoid type errors
        return io.TextIOWrapper(cast(IO[bytes], body), encoding="utf-8")

    def _get_s3_stream(
        self, bucket_name: str, object_key: str, s3: S3ServiceResource
    ) -> io.TextIOWrapper:
        bucket = self.get_bucket(s3, bucket_name)
        obj = self.get_object(bucket, object_key)
        stream = self.get_object_stream(obj)
        return stream

    def get_s3_stream(self, bucket_name: str, object_key: str) -> io.TextIOWrapper:
        """Returns a text stream of the specified object in the given bucket."""
        return self._get_s3_stream(bucket_name, object_key, self.resource)
