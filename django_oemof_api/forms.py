import logging
import pickle
import os
import json
import io
import csv
import numpy as np


from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.conf import settings as django_settings

class UploadFileForm(forms.Form):
    file = forms.FileField()
