# -*- coding:utf-8 -*-
from cluster.utils.date import handel_date_fields
from cluster.utils.js_validation import process_js_validations

__author__ = 'M.Y'
from django import forms


class ClusterBaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ClusterBaseForm, self).__init__(*args, **kwargs)
        handel_date_fields(self)
        process_js_validations(self)


class ClusterBaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ClusterBaseModelForm, self).__init__(*args, **kwargs)
        handel_date_fields(self)
        process_js_validations(self)