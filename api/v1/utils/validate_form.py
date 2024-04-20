#!/usr/bin/env python3

from models import storage, Company


def is_exists_form(company_id, data):
    company = storage.get(Company, company_id)
    if company is None:
        return True
    for form in company.forms:
        if form.name == data['name']:
            return True
    return False
