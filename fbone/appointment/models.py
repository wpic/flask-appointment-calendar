# -*- coding: utf-8 -*-

from ..extensions import db
from ..utils import USERNAME_LEN_MAX
from .forms import MESSAGE_LEN_MAX, EMAIL_LEN_MAX, TIMEZONE_LEN_MAX


class Appointment(db.Model):

    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(USERNAME_LEN_MAX), nullable=False)
    email = db.Column(db.String(EMAIL_LEN_MAX), nullable=False)
    start_time = db.Column(db.Integer, nullable=False)
    end_time = db.Column(db.Integer, nullable=False)
    timezone = db.Column(db.String(TIMEZONE_LEN_MAX), nullable=False)
    message = db.Column(db.String(MESSAGE_LEN_MAX), nullable=False)
