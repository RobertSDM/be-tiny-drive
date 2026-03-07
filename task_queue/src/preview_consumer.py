import concurrent.futures
import io
import json
import os
import signal
import tempfile
from PIL import Image
from typing import List, Tuple

from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from task_queue.src.constants import PREVIEW_SIZES, SUPA_BUCKETID
from task_queue.src.lib.supabase.storage import supabase_storage_client
from task_queue.src.shemas import PreviewBody
from task_queue.src.utils import make_file_bucket_path


def save_previews(
    previews: List[Tuple[PREVIEW_SIZES, io.BytesIO]], preview_body: PreviewBody
):
    with concurrent.futures.ThreadPoolExecutor() as exec:
        futures = list()
        for preview_size, preview in previews:
            future = exec.submit(
                supabase_storage_client.save,
                SUPA_BUCKETID,
                "image/jpg",
                make_file_bucket_path(
                    preview_body.ownerid, preview_body.fileid, f"preview+{preview_size}"
                ),
                io.BufferedReader(preview),
            )
            futures.append(future)

        concurrent.futures.wait(futures)


def preview_worker(
    ch: BlockingChannel,
    method: Basic.Deliver,
    properties: BasicProperties,
    body: bytes,
):
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    preview_body = PreviewBody.model_validate(json.loads(body))

    tempfile_name = f"{preview_body.fileid}-{preview_body.content_type.split('/')[0]}"

    temp = tempfile.NamedTemporaryFile(suffix=tempfile_name, delete=False)
    temp.write(
        supabase_storage_client.download(
            SUPA_BUCKETID,
            make_file_bucket_path(preview_body.ownerid, preview_body.fileid, "file"),
        )
    )

    temp.seek(0)
    temp.close()

    if preview_body.content_type.startswith("image"):
        from task_queue.src.processors.image_processor import preview_processing

        previews = preview_processing(Image.open(temp.name), preview_body.content_type)
    elif preview_body.content_type.startswith("text"):
        from task_queue.src.processors.text_processor import text_processing

        previews = text_processing(temp.name, preview_body.content_type)
    else:
        ch.basic_nack(delivery_tag=method.delivery_tag)
        return

    save_previews(previews, preview_body)

    os.remove(temp.name)

    ch.basic_ack(delivery_tag=method.delivery_tag)
