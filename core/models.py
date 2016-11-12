from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    loan_eligibility = models.CharField(max_length=200, db_index=True)
    account_number = models.CharField(max_length=200, db_index=True)
    incharge = models.CharField(max_length=200, db_index=True)
    incharge2 = models.CharField(max_length=200, db_index=True)


class Member(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    age = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200)
    phone  = models.CharField(max_length=200)

