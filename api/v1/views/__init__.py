#!/usr/bin/env python3
""" simple api """

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.companies import *
from api.v1.views.departments import *
from api.v1.views.jobs import *
from api.v1.views.employees import *
from api.v1.views.attendances import *
from api.v1.views.absences import *
