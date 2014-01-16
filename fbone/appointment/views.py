# -*- coding: utf-8 -*-

from flask import (Blueprint, render_template, request,
                   flash, url_for, redirect, session)
from flask.ext.mail import Message

from ..extensions import db, mail
from .forms import MakeAppointmentForm
from .models import Appointment


appointment = Blueprint('appointment', __name__, url_prefix='/appointment')


@appointment.route('/create', methods=['GET', 'POST'])
def create():
    form = MakeAppointmentForm(formdata=request.args,
                               next=request.args.get('next'))

    # Dump all available data from request or session object to form fields.
    for key in form.data.keys():
        setattr(getattr(form, key), 'data',
                request.args.get(key) or session.get(key))

    if form.validate_on_submit():
        appointment = Appointment()
        form.populate_obj(appointment)

        db.session.add(appointment)
        db.session.commit()

        flash_message = """
        Congratulations! You've just made an appointment
        on WPIC Web Calendar system, please check your email for details.
        """
        flash(flash_message)

        return redirect(url_for('appointment.create'))

    return render_template('appointment/create.html', form=form)
