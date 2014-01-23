# -*- coding: utf-8 -*-

from datetime import datetime, date
import smtplib
import time

from flask import (Blueprint, render_template, request, abort, flash, url_for,
                   redirect, session, current_app, jsonify)
from flask.ext.mail import Message

from ..extensions import db, mail
from .forms import MakeAppointmentForm
from .models import Appointment


appointment = Blueprint('appointment', __name__, url_prefix='/appointment')


def get_epoch_time(date_obj, minutes, timezone):
    """Get seconds from epoch

    date_obj: a datetime.date object
    minutes: an integer in [0, 1400]
    timezone: an float in [-12, 12]

    return: seconds from epcoh time.
    """
    epoch_date = date(1970, 1, 1)
    seconds = (date_obj - epoch_date).total_seconds()
    seconds += minutes * 60
    seconds -= timezone * 3600

    return int(seconds)


def get_local_time_minutes(minutes, timezone):
    date_obj = datetime.fromtimestamp(minutes).time()
    minutes = date_obj.hour * 60 + date_obj.minute
    timezone_delta = -time.timezone/3600 - timezone
    minutes -= 60 * timezone_delta
    return minutes


def appointment_ok(appointment):
    start = Appointment.query.filter(Appointment.start_time <=
                                     appointment.start_time,
                                     Appointment.end_time >=
                                     appointment.start_time).count()
    end = Appointment.query.filter(Appointment.start_time <=
                                   appointment.end_time,
                                   Appointment.end_time >=
                                   appointment.end_time).count()

    if start == 1 or end == 1:
        return False
    return True


@appointment.route('/')
def all_appointments():
    """Returns a json object which contains all appointments in a specific
    date.
    """
    if not request.args.get('date'):
        date_obj = date.today()
    else:
        date_obj = datetime.strptime(request.args.get('date'),
                                     "%Y-%m-%d").date()
    timezone = float(str(request.args.get('timezone', 0.00)))
    start_time = get_epoch_time(date_obj, 0, timezone)
    end_time = get_epoch_time(date_obj, 1440, timezone)

    result = Appointment.query.filter(Appointment.start_time >= start_time,
                                      Appointment.end_time <= end_time).\
        order_by(Appointment.start_time)

    apt_time_seconds = [[a.start_time, a.end_time] for a in result]
    apt_time_slider = [[get_local_time_minutes(a[0], timezone),
                        get_local_time_minutes(a[1], timezone)]
                       for a in apt_time_seconds]

    return jsonify(apt_time_seconds=apt_time_seconds,
                   apt_time_slider=apt_time_slider,
                   date=str(date_obj),
                   timezone=timezone)


@appointment.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        wpic_no_send_email = u"no-send@wpic.com"
        form = MakeAppointmentForm(next=request.args.get('next'))

        if form.email.data is u"" or form.email.data is "":
            form.email.data = wpic_no_send_email

        if not form.validate_on_submit():
            return render_template('appointment/create.html',
                                   form=form,
                                   horizontal=True)
        else:
            appointment = Appointment()
            form.populate_obj(appointment)
            appointment.start_time = get_epoch_time(form.date.data,
                                                    int(form.start_time.data),
                                                    float(form.timezone.data))
            appointment.end_time = get_epoch_time(form.date.data,
                                                  int(form.end_time.data),
                                                  float(form.timezone.data))

            if appointment_ok(appointment):
                db.session.add(appointment)
                db.session.commit()
            else:
                flash_message = "Sorry but your appointment time is occupied."
                flash(flash_message)
                return redirect(url_for('appointment.create'))

            flash_message = """
            Congratulations! You've just made an appointment
            on WPIC Web Calendar system, please check your email for details.
            """
            flash(flash_message)

            mail_message = Message("WPIC Web Calendar Appointment@%s" %
                                   form.date.data,
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

            if form.email.data is not wpic_no_send_email:
                try:
                    mail.send(mail_message)
                except smtplib.SMTPException as e:
                    current_app.logger.debug("Send email faied, %s", e.message)

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
                                          datetime.today().strftime('%Y-%m-%d'),  # NOQA
                                          "%Y-%m-%d"))
            else:
                setattr(getattr(form, key), 'data',
                        request.args.get(key) or session.get(key))

        return render_template('appointment/create.html',
                               form=form,
                               horizontal=True)

    else:
        abort(405)
