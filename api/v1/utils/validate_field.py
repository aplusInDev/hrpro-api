#!/usr/bin/env python3

from models import storage, Form

def is_exists_field(form_id, data):
    form = storage.get(Form, form_id)
    if form is None:
        return True
    for field in form.fields:
        if field.fname == data['fname']:
            return True
    return False