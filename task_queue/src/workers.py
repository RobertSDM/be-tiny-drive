import io
import json
import os
import signal
import tempfile

from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
from PIL import Image

from task_queue.src.constants import SUPA_BUCKETID, SUPPORTED_IMAGE_PREVIEW_TYPES
from task_queue.src.lib.supabase.storage import supabase_storage_client
from task_queue.src.utils import image_to_jpg, make_file_bucket_path, resize_image


def preview_worker(
    ch: BlockingChannel,
    method: Basic.Deliver,
    properties: BasicProperties,
    body: bytes,
):
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    json_data: dict[str, str] = json.loads(body)

    id_ = json_data["fileid"]
    content_type = json_data["content_type"]

    tempfile_name = f"{id_}-{content_type.split('/')[0]}"

    temp = tempfile.NamedTemporaryFile(suffix=tempfile_name, delete=False)
    temp.write(
        supabase_storage_client.download(
            SUPA_BUCKETID, make_file_bucket_path(json_data["ownerid"], id_, "file")
        )
    )

    temp.seek(0)
    temp.close()

    # Gerating Preview
    if content_type not in SUPPORTED_IMAGE_PREVIEW_TYPES:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    image = Image.open(temp.name)
    image = resize_image(image)
    image = image_to_jpg(image)

    supabase_storage_client.save(
        SUPA_BUCKETID,
        "image/jpg",
        make_file_bucket_path(json_data["ownerid"], id_, "preview"),
        io.BufferedReader(image),
    )

    os.remove(temp.name)

    ch.basic_ack(delivery_tag=method.delivery_tag)
