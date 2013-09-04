# -*- coding:utf-8 -*-
__author__ = 'M.Y'


def process_js_validations(form):
    from django import forms

    for field in form.fields:
        validations = ''
        if form.fields[field].required:
            validations += 'required,'
        if isinstance(form.fields[field], (forms.DateField, forms.DateTimeField)):
            validations += 'custom[date],'
        elif isinstance(form.fields[field], forms.EmailField):
            validations += 'custom[email],'
        elif isinstance(form.fields[field], forms.FloatField):
            validations += 'custom[number]'
        elif isinstance(form.fields[field], forms.IntegerField):
            validations += 'custom[integer]'
        if hasattr(form,'extra_js_validation') and form.extra_js_validation.get(field):
            validations += form.extra_js_validation.get(field)

        form.fields[field].widget.attrs.update({'class': 'validate[%s] text-input' % validations})
