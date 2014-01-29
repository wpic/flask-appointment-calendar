# -*- coding: utf-8 -*-

from datetime import datetime, date
import smtplib

from flask import (Blueprint, render_template, request, abort, flash, url_for,
                   redirect, session, current_app, jsonify)
from flask.ext.mail import Message

from sqlalchemy.sql import select, and_, or_

from ..extensions import db, mail
from .forms import MakeAppointmentForm
from .models import Appointment


appointment = Blueprint('appointment', __name__, url_prefix='/appointment')


def get_utc_seconds(date_obj, minutes, timezone):
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


def get_local_minutes(seconds, date_obj, timezone):
    init_seconds = get_utc_seconds(date_obj, 0, timezone)
    delta_seconds = seconds - init_seconds
    if delta_seconds < 0:
        delta_seconds = 0
    elif delta_seconds > 86400:
        delta_seconds = 86400

    return delta_seconds / 60


def appointment_ok(appointment):
    if appointment.start_time >= appointment.end_time:
        return False, "Start time %s and end time %s is illegal." % \
            (appointment.start_time, appointment.end_time)
    start = Appointment.query.filter(Appointment.start_time <
                                     appointment.start_time,
                                     Appointment.end_time >
                                     appointment.start_time).count()
    end = Appointment.query.filter(Appointment.start_time <
                                   appointment.end_time,
                                   Appointment.end_time >
                                   appointment.end_time).count()
    equal = Appointment.query.filter(Appointment.start_time ==
                                     appointment.start_time,
                                     Appointment.end_time ==
                                     appointment.end_time).count()

    if start == 1 or end == 1 or equal == 1:
        return False, "Your appointment time is occupied."
    return True, "Appointment ok."


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
    start_time = get_utc_seconds(date_obj, 0, timezone)
    end_time = get_utc_seconds(date_obj, 1440, timezone)

    conn = db.engine.connect()
    query = select([Appointment],
                   or_(and_(Appointment.start_time >= start_time,
                            Appointment.start_time <= end_time),
                       and_(Appointment.end_time >= start_time,
                            Appointment.end_time <= end_time))).\
        order_by(Appointment.start_time)
    result = conn.execute(query).fetchall()

    apt_time_utc_seconds = [[a.start_time, a.end_time] for a in result]
    apt_time_slider_minutes = [[get_local_minutes(a[0], date_obj, timezone),
                                get_local_minutes(a[1], date_obj, timezone)]
                               for a in apt_time_utc_seconds]

    return jsonify(apt_time_utc_seconds=apt_time_utc_seconds,
                   apt_time_slider_minutes=apt_time_slider_minutes,
                   date=str(date_obj),
                   timezone=timezone)


@appointment.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        wpic_no_send_email = u"wpic-no-send-anonymous@wpic.com"
        form = MakeAppointmentForm(next=request.args.get('next'))

        if form.email.data is u"" or form.email.data is "":
            form.email.data = wpic_no_send_email

        if not form.validate_on_submit():
            message = "Illegal post data."
            return render_template('appointment/create.html',
                                   form=form,
                                   horizontal=True)
        else:
            # Keep name and email in session
            session['name'] = form.name.data
            session['email'] = form.email.data

            appointment = Appointment()
            form.populate_obj(appointment)
            appointment.start_time = get_utc_seconds(form.date.data,
                                                     int(form.start_time.data),
                                                     float(form.timezone.data))
            appointment.end_time = get_utc_seconds(form.date.data,
                                                   int(form.end_time.data),
                                                   float(form.timezone.data))

            ok, message = appointment_ok(appointment)
            if ok:
                db.session.add(appointment)
                db.session.commit()
            else:
                flash(message)
                return redirect(url_for('appointment.create'))

            flash_message = """
            Thank you for contacting us. If you have any questions, please email
            ernie.diaz@web-presence-in-china.com.
            """
            flash(flash_message)

            mail_message = Message("New Appointment from wpicmeet.com",
                                   recipients=["ernie.diaz@web-presence-in-china.com"])
            mail_message.body = """New appointment here:

----
Name: %s
Message: %s
Date: %s
Email: %s
Time: %s - %s
Timezone: %s
----
            """ % (form.name.data, form.message.data,
                   form.date.data,
                   form.email.data,
                   form.start_time.data, form.end_time.data,
                   form.timezone.data)

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
