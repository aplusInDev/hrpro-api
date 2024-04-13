#!/usr/bin/env python3

from models import storage, Company


def is_valid_form(data):
    if data is None:
        return False
    if 'name' not in data or 'fields' not in data:
        return False
    if data['name'] not in ['employee_form', 'job_form', 'department_form']:
        return False
    return True

def is_exists_form(company_id, data):
    company = storage.get(Company, company_id)
    if company is None:
        return True
    if is_valid_form(data):
        for form in company.forms:
            if form.name == data['name']:
                return True
        return False
    return True
