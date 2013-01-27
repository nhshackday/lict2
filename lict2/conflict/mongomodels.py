# -*- coding: UTF-8 -*-

from __future__ import print_function, division, absolute_import, unicode_literals
from mongoengine.document import Document
from mongoengine.fields import StringField, IntField, DateTimeField

class Doctor(Document):
    """
    #keys = ['GMC Ref Number', 'Given Names', 'Surname', 'Status', 'Prov Reg Date', 'Full Reg Date', 'Annual Fee Due Date', '']
    3527470, Peter Robert, Ahee, Registered with a licence to practise, N/A, 10/01/91, 10/01/14,
    """
    surname = StringField()
    given_names = StringField()
    gmc_reference_number = IntField(unique=True)
    registration_date = DateTimeField()
