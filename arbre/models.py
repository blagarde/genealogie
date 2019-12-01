# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=20, help_text='First name.')
    middle_name = models.CharField(null=True, max_length=20, help_text='Middle name, space-separated if more than one.')
    last_name = models.CharField(max_length=20, help_text='Last name.')
    parent =  models.ManyToManyField('Person', related_name='children', help_text='ID of the parent in the Persons table.')
    birth_place = models.CharField(null=True, max_length=20, help_text='Place of birth, generally a city.')
    birth_date = models.DateField(null=True, help_text='Birth date.')
    birth_date_is_approximative = models.BooleanField(default=False, help_text='Boolean indicating uncertainty around the birth date.')
    death_place = models.CharField(null=True, max_length=20, help_text='Place of death, generally a city.')
    death_date = models.DateField(null=True, help_text='Death date.')
    death_date_is_approximative = models.BooleanField(default=False, help_text='Boolean indicating uncertainty around the death date.')
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')], help_text="Person's gender.")
    comments = models.TextField(null=True, help_text='Freeform comments.')

    def as_dict(self):
        dct = {k: v for k, v in self.__dict__.items() if k != '_state'}
        dct['type'] = "person"
        return dct
