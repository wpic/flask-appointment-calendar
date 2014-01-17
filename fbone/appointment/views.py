# -*- coding: utf-8 -*-

from datetime import datetime

from flask import (Blueprint, render_template, request, abort,
                   flash, url_for, redirect, session)
from flask.ext.mail import Message

from ..extensions import db, mail
from .forms import MakeAppointmentForm
from .models import Appointment


appointment = Blueprint('appointment', __name__, url_prefix='/appointment')


@appointment.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        form = MakeAppointmentForm(next=request.args.get('next'))

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

            mail_message = Message("WPIC Web Calendar Appointment@%s" % form.date.data,
                                   recipients=[form.email.data])
            mail_message.body = """Dear %s:

Congratulations! You've just made an appointment on WPIC Web
Calendar system. Here's the appointment details:

----
Date: %s
Timezone: %s
Your message:
%s
----
            """ % (form.name.data, form.date.data,
                   form.timezone.data, form.message.data)

            mail.send(mail_message)

            return redirect(url_for('appointment.create'))

    elif request.method == 'GET':
        form = MakeAppointmentForm(formdata=request.args,
                                   next=request.args.get('next'))
        # Dump all available data from request or session object to form
        # fields.
        for key in form.data.keys():
            if key == "date":
                setattr(getattr(form, key), 'data',
                        datetime.strptime(request.args.get(key) or
                                          session.get(key) or
                                          datetime.today().strftime('%Y-%m-%d'),
                                          "%Y-%m-%d"))
            else:
                setattr(getattr(form, key), 'data',
                        request.args.get(key) or session.get(key))

        return render_template('appointment/create.html', form=form)

    else:
        abort(405)
