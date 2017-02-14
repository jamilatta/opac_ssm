# -*- coding: utf-8 -*-

import io
import json
import logging

from django.core.files import File

from opac_ssm.taskapp.celery import app
from . import models

logger = logging.getLogger(__name__)


@app.task(bind=True)
def add_asset(self, file, filename, type=None, metadata=None, bucket_name=""):
    """
    Task to create a new asset.

    The only field mandatory is field file

    Params:
        :param file: Bytes (Mandatory)
        :param filename: Name of file (Mandatory)
        :param type: is the type of asset
        :param metadata: JSON with metadada about asset
        :param bucket_name: Name of bucket related to asset
    """

    try:
        fp = io.BytesIO(file)
    except TypeError as e:
        logger.error(e)
        raise

    if bucket_name == "":
        bucket_name = "UNKNOW"

    bucket, created = models.AssetBucket.objects.get_or_create(name=bucket_name)

    if created:
        logger.info(u"Novo bucket adicionado com o nome: %s", bucket.name)

    asset = models.Asset()
    asset.file = File(fp, filename)
    asset.filename = filename
    asset.type = type
    asset.metadata = metadata
    asset.task_id = self.request.id # Save task id
    asset.bucket = bucket
    asset.save()

    logger.info(u"Successfully created asset with the id=%s, size=%s and path=%s",
                asset.id, asset.file.size, asset.file.path)

    return self.request.id
