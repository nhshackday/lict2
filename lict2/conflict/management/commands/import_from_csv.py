# -*- coding: UTF-8 -*-

from __future__ import print_function, division, absolute_import, unicode_literals
import csv
import logging
from django.core.management.base import BaseCommand
from conflict.mongomodels import Doctor

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def handle(self, *args, **options):
        for csv_file_name in args:
            logger.info("Starting import from %s" % csv_file_name)
            Doctor.objects.delete() #TODO Sanity
            with open(csv_file_name, 'rb') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    doctor = Doctor()
                    doctor.first_name = row['First name']
                    doctor.last_name = row['Last name']
                    doctor.save()
            logger.info("Finished import from %s" % csv_file_name)
        logger.info("Finished importing %s", ', '.join(args))
