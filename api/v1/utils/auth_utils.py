#!/usr/bin/env python3
from api.v1.auth.auth import Auth
from sqlalchemy.orm.exc import NoResultFound


def verify_account_company_id(session_id: str, company_id: str) -> bool:
    """Verify account company_id.

    Args:
        session_id: String representing the session ID.
        company_id: String representing the company ID.

    Returns:
        True if the company ID matches the account's company ID.
        False otherwise.
    """
    try:
        account = Auth().get_account_from_session_id(session_id)
        if account.company_id == company_id:
            return True
    except NoResultFound:
        return False

    return False
