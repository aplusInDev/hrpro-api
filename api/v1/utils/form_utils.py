#!/usr/bin/env python3

from models import storage


def get_all_fields(form_name: str, company_id: str) -> list:
    """ retrive fields """
    form = storage.find_form_by_(name=form_name, company_id=company_id)
    if form is None:
        return None
    return [field.to_dict() for field in form.fields]


def handle_update_info(form_name: str, company_id: str, data: dict) -> dict:
    """def handle_update_info(
        form_name: str, company_id: str,
        data: dict
    ) -> dict | None:
    This function is used to validate the data that is going to be updated
    in the database
    Args:
        form_name: the name of the form
        company_id: the id of
        data: the data that is going to be updated
    Returns:
        the data that is going to be updated if the data is valid
        None if the data is not valid
    """
    fields_names = []
    to_delete = []
    all_fields = get_all_fields(form_name, company_id)
    if not all_fields:
        return []
    for field in all_fields:
        field_name = field["name"].replace(' ', '_')
        fields_names.append(field_name)
        if field_name not in data:
            # Check if the field is required then raise an error
            if field["is_required"] is True:
                raise ValueError(f"Missing {field_name} field")
            # If the field is not required then set the default value
            else:
                data[field_name] = field["default_value"]

    # Delete the fields that are not in the form
    for key in data.keys():
        if key not in fields_names:
            to_delete.append(key)

    for key in to_delete:
        del data[key]

    return data
