# -*- coding: UTF-8 -*-

from __future__ import print_function, division, absolute_import, unicode_literals
import csv
import logging
from django.core.management.base import BaseCommand
from conflict.mongomodels import Doctor

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def handle(self, *args, **options):
        for file_name in args:
            logger.info("Starting import from %s" % file_name)
            logger.info("Finished import from %s" % file_name)
        logger.info("Finished importing %s", ', '.join(args))
