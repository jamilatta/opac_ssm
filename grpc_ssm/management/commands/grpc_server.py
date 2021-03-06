# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.conf import settings

from grpc_ssm import grpc_server


class Command(BaseCommand):
    help = 'GRCP Server'

    def handle(self, *args, **options):

        self.stdout.write("Starting GRPC... Host: {0}, Port: {1}".format(
                          settings.GRCP_HOST, settings.GRCP_PORT))

        grpc_server.serve(settings.GRCP_HOST, settings.GRCP_PORT,
                          settings.GRCP_MAX_WORKERS,
                          settings.GRPC_MAX_RECEIVE_MESSAGE_LENGTH,
                          settings.GRPC_MAX_SEND_MESSAGE_LENGTH)
