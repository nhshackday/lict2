# -*- coding: UTF-8 -*-

from __future__ import print_function, division, absolute_import, unicode_literals
import logging
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from conflict.mongomodels import Study

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def handle(self, *args, **options):
        for file_name in args:
            logger.info("Starting import from %s" % file_name)
            with open(file_name, 'rb') as data_file:
                try:
                    html_doc = data_file.read()

                    if b"No study found" in html_doc:
                        continue

                    doc = BeautifulSoup(html_doc)

                    # ARGH

                    def find_Cell_from_title(title):
                        def find_TitleCell_by_content(content):
                            """
                            I'm so so sorry
                            """
                            cells = doc.find_all(class_="TitleCell")
                            for cell in cells:
                                if cell.string.strip() == content:
                                    return cell
                        title_cell = find_TitleCell_by_content(title)
                        tr = title_cell.parent
                        td = tr.find(class_="Cell")
                        if td.string:
                            return td.string.strip()
                        if len(td.contents) > 1:
                            return td.contents[0].strip()

                    ukcrn_id = int(find_Cell_from_title("UKCRN ID"))
                    (study, _) = Study.objects.get_or_create(ukcrn_id=ukcrn_id)
                    study.name = doc.find_all("p", align="justify")[0].string.strip()
                    study.funder = find_Cell_from_title("Funder(s)")
                    study.sponsor = find_Cell_from_title("Sponsor(s)")
                    study.save()
                except Exception as e: # I AM A VERY VERY BAD PERSON
                    logger.warn(e)

            logger.info("Finished import from %s" % file_name)
        logger.info("Finished importing %s", ', '.join(args))
