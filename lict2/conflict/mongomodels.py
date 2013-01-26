# -*- coding: UTF-8 -*-

from __future__ import print_function, division, absolute_import, unicode_literals
from mongoengine.document import Document
from mongoengine.fields import StringField

class Doctor(Document):
    """
    Ideally we'd use the LRMP list. We don't have that, but we do have a CSV subset...

    Massively temporary: Last name,First name,Title,Type,Site name,Address1,Address2,Address3,Postcode,Telephone,Institution
    """
    last_name = StringField()
    first_name = StringField()
    title = StringField()
    type = StringField() #TODO Enumalike?
    site_name = StringField()
    # TODO Address?
    institution = StringField() #TODO Reference
