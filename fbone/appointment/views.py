# -*- coding: utf-8 -*-

from uuid import uuid4

from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort)
from flask.ext.mail import Message
from flask.ext.babel import gettext as _
from flask.ext.login import login_required, login_user, current_user, logout_user, confirm_login, login_fresh

from ..user import User, UserDetail
from ..extensions import db, mail, login_manager, oid
from .forms import MakeAppointmentForm


appointment = Blueprint('appointment', __name__, url_prefix='/appointment')


@appointment.route('/create', methods=['GET', 'POST'])
def create():
    form = MakeAppointmentForm()
    return render_template('appointment/create.html', form=form)
