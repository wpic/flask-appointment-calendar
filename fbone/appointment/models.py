# -*- coding: utf-8 -*-

from ..extensions import db
from ..utils import (get_current_time, USERNAME_LEN_MAX)
from .forms import CONTENT_LEN_MAX, EMAIL_LEN_MAX


class Appointment(db.Model):

    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(USERNAME_LEN_MAX), nullable=False)
    last_name = db.Column(db.String(USERNAME_LEN_MAX), nullable=False)
    email = db.Column(db.String(EMAIL_LEN_MAX), nullable=False)
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.String(CONTENT_LEN_MAX), nullable=False)
