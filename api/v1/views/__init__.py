#!/usr/bin/env python3
""" simple api """

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1', template_folder='templates')

from api.v1.views.index import *
from api.v1.views.companies import *
from api.v1.views.departments import *
from api.v1.views.jobs import *
from api.v1.views.employees import *
from api.v1.views.attendances import *
from api.v1.views.forms import *
from api.v1.views.fields import *
from api.v1.views.auth_session import *
from api.v1.views.accounts import *
from api.v1.views.absences import *
from api.v1.views.leaves import *
