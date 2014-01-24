# -*- coding: utf-8 -*-

import datetime
import time

from fbone.extensions import db
from fbone.appointment.models import Appointment

from fbone.appointment.views import get_epoch_time

from tests import TestCase


class TestAppointment(TestCase):

    name = "TestName"
    email = "testemail@sample.com"
    timezone = float(-time.timezone/3600)
    message = "Some kind of test message for calendar."
    today = datetime.date.today()
    epoch_date = datetime.date(1970, 1, 1)
    appointment_times = ((60, 120), (180, 300), (360, 600), (1200, 1440))

    def setUp(self):
        super(TestAppointment, self).setUp()
        self.init_some_appointments()

    def make_an_appointment(self, start_time, end_time):
        return Appointment(name=self.name,
                           email=self.email,
                           start_time=start_time,
                           end_time=end_time,
                           timezone=self.timezone,
                           message=self.message)

    def init_some_appointments(self):
        for start, end in self.appointment_times:
            start_time = get_epoch_time(self.today, start, self.timezone)
            end_time = get_epoch_time(self.today, end, self.timezone)
            appointment = self.make_an_appointment(start_time, end_time)
            db.session.add(appointment)

        db.session.commit()

    def test_available_time_range(self):
        resp = self.client.get('/appointment/')
        self.assertEqual(resp.mimetype, 'application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['timezone'], 0.0)
        self.assertEqual(resp.json['date'], str(self.today))

    def test_available_time_range_with_date(self):
        date = '1988-08-08'
        resp = self.client.get('/appointment/?date=%s' % date)
        self.assertEqual(resp.mimetype, 'application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['timezone'], 0.0)
        self.assertEqual(resp.json['date'], date)

    def test_available_time_range_with_timezone(self):
        resp = self.client.get('/appointment/?timezone=%s' % self.timezone)
        self.assertEqual(resp.mimetype, 'application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['timezone'], self.timezone)
        self.assertEqual(resp.json['date'], str(self.today))
        self.assertEqual(len(resp.json['apt_time_seconds']),
                         len(self.appointment_times))
