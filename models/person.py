#!/usr/bin/env python3

from models import *


class Person(BaseModel):
    """Person class"""

    def __init__(self, *args, **kwargs):
        """Initializes a new instance"""
        super().__init__(*args, **kwargs)
        self.name = ""
        self.last_name = ""
        self.info = "{}"
