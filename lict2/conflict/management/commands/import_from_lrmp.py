# -*- coding: UTF-8 -*-

from __future__ import print_function, division, absolute_import, unicode_literals
import csv
import logging
import pdb
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from conflict.mongomodels import Doctor

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def handle(self, *args, **options):
        for html_file_name in args:
            logger.info("Starting import from %s" % html_file_name)
            #Doctor.objects.delete() #TODO Sanity
            with open(html_file_name, 'rb') as html_file:
                html_doc = html_file.read()
                doc = BeautifulSoup(html_doc)

                #get table cells out of page
                info = []
                for td in doc.find_all('td'):
                    if td.get('class') and td.get('class')[0] == 'listapplettablerows':
                        info.append(td)


                #keys = ['GMC Ref Number', 'Given Names', 'Surname', 'Status', 'Prov Reg Date',
                #        'Full Reg Date', 'Annual Fee Due Date']
                # split on every 7th
                column = 0
                doctor = None
                for result in info:
                    value = result.text

                    if column == 0:
                        doctor = Doctor()
                        doctor.gmc_reference_number = value
                    elif column == 1:
                        doctor.given_names = value
                    elif column == 2:
                        doctor.surname = value
                    elif column == 3:
                        # status
                        pass
                    elif column == 4:
                        # prov reg date
                        pass
                    elif column == 5:
                        # full reg date
                        v = value.split('/')
                        v.reverse()

                        year = int(v[0])
                        if year > 14: #blerghh
                            year = '19%02s' % year
                        else:
                            year = '20%02s' % year

                        v[0] = year
                        value2 = '-'.join(v)
                        doctor.registration_date = value2
                    elif column == 6:
                        # annual fee due date
                        pass

                    column += 1
                    if column == 7:
                        doctor.save()
                        column = 0

            logger.info("Finished import from %s" % html_file_name)
        logger.info("Finished importing %s", ', '.join(args))
