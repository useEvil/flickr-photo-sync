import os, re, mimetypes

from django import forms


class FileUploadForm(forms.Form):

    dataFile = forms.FileField(
        label='Select a file',
    )

class AssociationForm(forms.Form):

    association = forms.CharField(max_length=50, required=False)
    account = forms.CharField(max_length=50, required=False)
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    address_1 = forms.CharField(max_length=50, required=False)
    address_2 = forms.CharField(max_length=50, required=False)
    address_3 = forms.CharField(max_length=50, required=False)
    address_4 = forms.CharField(max_length=50, required=False)
    address_last_line = forms.CharField(max_length=50, required=False)
    property_address = forms.CharField(max_length=50, required=False)
    amount_due = forms.CharField(max_length=50, required=False)
