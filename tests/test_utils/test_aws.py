import io

import pytest

from scripts.utils.aws import ClientS3


@pytest.fixture(autouse=True)
def mock_session(mocker):
    mock_session_cls = mocker.patch("boto3.Session")
    mock_session = mocker.Mock()
    mock_resource = mocker.Mock()
    mock_session.resource.return_value = mock_resource
    mock_session_cls.return_value = mock_session
    yield mock_session, mock_resource


def test_init_sets_profile_and_resource(mock_session):
    mock_session_obj, mock_resource = mock_session
    client = ClientS3("my-profile")
    assert client.profile_name == "my-profile"
    assert client.session == mock_session_obj
    assert client.resource == mock_resource


def test_get_bucket_returns_bucket(mocker):
    s3_resource = mocker.Mock()
    bucket = mocker.Mock()
    s3_resource.Bucket.return_value = bucket
    result = ClientS3.get_bucket(s3_resource, "bucket-name")
    s3_resource.Bucket.assert_called_once_with(name="bucket-name")
    assert result == bucket


def test_get_object_returns_object(mocker):
    bucket = mocker.Mock()
    obj = mocker.Mock()
    bucket.Object.return_value = obj
    result = ClientS3.get_object(bucket, "object-key")
    bucket.Object.assert_called_once_with("object-key")
    assert result == obj


def test_get_object_streaming_body_returns_body(mocker):
    obj = mocker.Mock()
    body = mocker.Mock()
    obj.get.return_value = {"Body": body}
    result = ClientS3.get_object_streaming_body(obj)
    obj.get.assert_called_once_with()
    assert result == body


def test_get_object_stream_returns_text_stream(mocker):
    obj = mocker.Mock()
    body = io.BytesIO(b"hello world")
    obj.get.return_value = {"Body": body}
    client = ClientS3("profile")
    mocker.patch.object(ClientS3, "get_object_streaming_body", return_value=body)
    stream = client.get_object_stream(obj)
    assert isinstance(stream, io.TextIOWrapper)
    assert stream.read() == "hello world"


def test__get_s3_stream_calls_methods_in_order(mocker):
    client = ClientS3("profile")
    s3 = mocker.Mock()
    bucket = mocker.Mock()
    obj = mocker.Mock()
    stream = mocker.Mock()
    mock_get_bucket = mocker.patch.object(ClientS3, "get_bucket", return_value=bucket)
    mock_get_object = mocker.patch.object(ClientS3, "get_object", return_value=obj)
    mock_get_stream = mocker.patch.object(
        ClientS3, "get_object_stream", return_value=stream
    )
    result = client._get_s3_stream("bucket", "key", s3)
    mock_get_bucket.assert_called_once_with(s3, "bucket")
    mock_get_object.assert_called_once_with(bucket, "key")
    mock_get_stream.assert_called_once_with(obj)
    assert result == stream
    assert result == stream
    mocker.patch("boto3.Session")  # Prevent real AWS profile lookup


def test_get_s3_stream_delegates_to__get_s3_stream(mocker):
    client = ClientS3("profile")
    mock__get = mocker.patch.object(ClientS3, "_get_s3_stream", return_value="stream")
    result = client.get_s3_stream("bucket", "key")
    mock__get.assert_called_once_with("bucket", "key", client.resource)
    assert result == "stream"
    mock__get.assert_called_once_with("bucket", "key", client.resource)
    assert result == "stream"
