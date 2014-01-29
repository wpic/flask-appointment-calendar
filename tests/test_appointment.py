# -*- coding: utf-8 -*-

from datetime import date
import time

from flask import session

from fbone.extensions import db
from fbone.appointment.models import Appointment

from fbone.appointment.views import (get_utc_seconds,
                                     get_local_minutes, appointment_ok)

from tests import TestCase


class TestAppointment(TestCase):

    name = "TestName"
    email = "testemail@sample.com"
    timezone = float(-time.timezone/3600)
    message = "Some kind of test message for calendar."
    today = date.today()
    epoch_date = date(1970, 1, 1)
    appointment_times = ((60, 120), (180, 300), (360, 600), (1200, 1440))

    def setUp(self):
        super(TestAppointment, self).setUp()
        self.init_some_appointments()

    def make_an_appointment(self, start_time, end_time, timezone):
        return Appointment(name=self.name,
                           email=self.email,
                           start_time=start_time,
                           end_time=end_time,
                           timezone=self.timezone,
                           message=self.message)

    def make_an_appointment_dict(self, date, start_time, end_time):
        return dict(name=self.name,
                    email=self.email,
                    date=date,
                    start_time=start_time,
                    end_time=end_time,
                    timezone=self.timezone,
                    message=self.message)

    def init_some_appointments(self):
        for start, end in self.appointment_times:
            start_time = get_utc_seconds(self.today, start, self.timezone)
            end_time = get_utc_seconds(self.today, end, self.timezone)
            appointment = self.make_an_appointment(start_time, end_time,
                                                   self.timezone)
            db.session.add(appointment)

        db.session.commit()

    def test_all_appointments(self):
        resp = self.client.get('/appointment/')
        self.assertEqual(resp.mimetype, 'application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['timezone'], 0.0)
        self.assertEqual(resp.json['date'], str(self.today))

    def test_all_appointments_with_date(self):
        date = '1988-08-08'
        resp = self.client.get('/appointment/?date=%s' % date)
        self.assertEqual(resp.mimetype, 'application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['timezone'], 0.0)
        self.assertEqual(resp.json['date'], date)

    def test_all_appointments_with_timezone(self):
        resp = self.client.get('/appointment/?timezone=%s' % self.timezone)
        self.assertEqual(resp.mimetype, 'application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['timezone'], self.timezone)
        self.assertEqual(resp.json['date'], str(self.today))
        self.assertEqual(len(resp.json['apt_time_utc_seconds']),
                         len(self.appointment_times))

    def test_appointment_ok(self):
        start_time1 = 948816000  # 1/26/2000 12:00:00 AM GMT+8
        # date = "2000-01-26"
        hour = 3600
        timezone = 8.0
        apt1 = self.make_an_appointment(start_time1, start_time1 + 4*hour,
                                        timezone)
        db.session.add(apt1)
        db.session.commit()

        ok, message = appointment_ok(apt1)
        self.assertFalse(ok)

        apt2 = self.make_an_appointment(start_time1+hour, start_time1 + 2*hour,
                                        timezone)
        ok, message = appointment_ok(apt2)
        self.assertFalse(ok)

        apt3 = self.make_an_appointment(start_time1, start_time1 + 2*hour,
                                        timezone)
        ok, message = appointment_ok(apt3)
        self.assertFalse(ok)

        apt4 = self.make_an_appointment(start_time1+2*hour,
                                        start_time1 + 4*hour,
                                        timezone)
        ok, message = appointment_ok(apt4)
        self.assertFalse(ok)

        apt5 = self.make_an_appointment(start_time1+2*hour,
                                        start_time1 + 2*hour,
                                        timezone)
        ok, message = appointment_ok(apt5)
        self.assertFalse(ok)

        apt6 = self.make_an_appointment(start_time1+4*hour,
                                        start_time1 + 8*hour,
                                        timezone)
        ok, message = appointment_ok(apt6)
        self.assertTrue(ok)

    def test_all_appointments_day_before_after(self):
        zero_time = 948816000  # 1/26/2000 12:00:00 AM GMT+8
        hour = 3600
        timezone = 8.0
        date = "2000-01-26"
        apt_before = self.make_an_appointment(zero_time - hour, zero_time,
                                              timezone)
        apt_after = self.make_an_appointment(zero_time, zero_time + hour,
                                             timezone)
        db.session.add(apt_before)
        db.session.add(apt_after)
        db.session.commit()
        url = '/appointment/?date=%s&timezone=%s' % (date, timezone)
        resp = self.client.get(url)
        self.assert200(resp)
        self.assertEqual(resp.json['date'], date)
        self.assertEqual(resp.json['apt_time_utc_seconds'],
                         [[zero_time - hour, zero_time],
                          [zero_time, zero_time + hour]])
        self.assertEqual(resp.json['timezone'], timezone)
        self.assertEqual(resp.json['apt_time_slider_minutes'],
                         [[0, 0], [0, 60]])
        timezone = 9.0
        url = '/appointment/?date=%s&timezone=%s' % (date, timezone)
        resp = self.client.get(url)
        self.assert200(resp)
        self.assertEqual(resp.json['date'], date)
        self.assertEqual(resp.json['apt_time_utc_seconds'],
                         [[zero_time - hour, zero_time],
                          [zero_time, zero_time + hour]])
        self.assertEqual(resp.json['timezone'], timezone)
        self.assertEqual(resp.json['apt_time_slider_minutes'],
                         [[0, 60], [60, 120]])
        timezone = 7.0
        url = '/appointment/?date=%s&timezone=%s' % (date, timezone)
        resp = self.client.get(url)
        self.assert200(resp)
        self.assertEqual(resp.json['date'], date)
        self.assertEqual(resp.json['apt_time_utc_seconds'],
                         [[zero_time, zero_time + hour]])
        self.assertEqual(resp.json['timezone'], timezone)
        self.assertEqual(resp.json['apt_time_slider_minutes'],
                         [[0, 0]])

    def test_all_appointments_a_whole_day(self):
        # Test cases where appointments last for a whole day long
        start_time = 948816000  # 1/26/2000 12:00:00 AM GMT+8
        end_time = 948902400    # 1/27/2000 12:00:00 AM GMT+8
        timezone = 8.0
        day_seconds = 24 * 3600
        date = "2000-01-26"
        apt1 = self.make_an_appointment(start_time, end_time, timezone)
        db.session.add(apt1)
        db.session.commit()
        url = '/appointment/?date=%s&timezone=%s' % (date, timezone)
        resp = self.client.get(url)
        self.assert200(resp)
        self.assertEqual(resp.json['date'], date)
        self.assertEqual(resp.json['apt_time_utc_seconds'],
                         [[start_time, end_time]])
        self.assertEqual(resp.json['timezone'], timezone)
        self.assertEqual(resp.json['apt_time_slider_minutes'],
                         [[0, 1440]])

        url = '/appointment/?date=%s&timezone=%s' % (date, timezone + 1)
        resp = self.client.get(url)
        self.assert200(resp)
        self.assertEqual(resp.json['date'], date)
        self.assertEqual(resp.json['apt_time_utc_seconds'],
                         [[start_time, end_time]])
        self.assertEqual(resp.json['timezone'], timezone + 1)
        self.assertEqual(resp.json['apt_time_slider_minutes'],
                         [[0 + 60, 1440]])

        url = '/appointment/?date=%s&timezone=%s' % (date, timezone - 3)
        resp = self.client.get(url)
        self.assert200(resp)
        self.assertEqual(resp.json['date'], date)
        self.assertEqual(resp.json['apt_time_utc_seconds'],
                         [[start_time, end_time]])
        self.assertEqual(resp.json['timezone'], timezone - 3)
        self.assertEqual(resp.json['apt_time_slider_minutes'],
                         [[0, 1440 - 60*3]])

        # Create another appointment just after apt1
        apt2 = self.make_an_appointment(start_time + day_seconds,
                                        end_time + day_seconds,
                                        timezone)
        db.session.add(apt2)
        db.session.commit()
        for tz_delta in range(-12, 0):
            tz = timezone + tz_delta
            url = '/appointment/?date=%s&timezone=%s' % (date, tz)
            resp = self.client.get(url)
            self.assert200(resp)
            self.assertEqual(resp.json['date'], date)
            self.assertEqual(resp.json['apt_time_utc_seconds'],
                             [[start_time,
                               start_time + day_seconds],
                              [start_time + day_seconds,
                               end_time + day_seconds]])
            self.assertEqual(resp.json['timezone'], tz)
            self.assertEqual(resp.json['apt_time_slider_minutes'],
                             [[0, 1440 + tz_delta*60],
                              [1440 + tz_delta*60, 1440]])

    def test_post_create(self):
        data = self.make_an_appointment_dict("2011-02-03", "60", "120")
        with self.client:
            resp = self.client.post('/appointment/create', data=data,
                                    follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertTrue("Thank" in resp.data)

            # Ensure session contains something.
            self.assertEqual(session['name'], data['name'])
            self.assertEqual(session['email'], data['email'])

    def test_post_illegal_data(self):
        illegal_date = "2011-02-033"
        data = self.make_an_appointment_dict(illegal_date, "60", "120")
        resp = self.client.post('/appointment/create', data=data,
                                follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

    def test_get_local_minutes(self):
        seconds1 = 1390665600   # 1/26/2014 12:00:00 AM GMT+8
        seconds2 = 1390752000   # 1/27/2014 12:00:00 AM GMT+8
        date_obj = date(2014, 1, 26)
        timezone = 8            # GMT+8
        m1 = get_local_minutes(seconds1, date_obj, timezone)
        m2 = get_local_minutes(seconds2, date_obj, timezone)
        self.assertEqual(m1, 0)
        self.assertEqual(m2, 1440)

        timezone = 7            # GMT+7
        m1 = get_local_minutes(seconds1, date_obj, timezone)
        m2 = get_local_minutes(seconds2, date_obj, timezone)
        self.assertEqual(m1, 0)
        self.assertEqual(m2, 1380)

        timezone = 9            # GMT+9
        m1 = get_local_minutes(seconds1, date_obj, timezone)
        m2 = get_local_minutes(seconds2, date_obj, timezone)
        self.assertEqual(m1, 60)
        self.assertEqual(m2, 1440)
