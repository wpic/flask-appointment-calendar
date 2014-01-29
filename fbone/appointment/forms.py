import datetime

from flask.ext.wtf import Form
from wtforms import (Field, HiddenField, TextField,
                     TextAreaField, SubmitField, DateField, SelectField)
from wtforms.validators import Required, Length, Email
from flask.ext.wtf.html5 import EmailField

from ..utils import (USERNAME_LEN_MIN, USERNAME_LEN_MAX)

EMAIL_LEN_MIN = 4
EMAIL_LEN_MAX = 64

MESSAGE_LEN_MIN = 16
MESSAGE_LEN_MAX = 1024

TIMEZONE_LEN_MIN = 1
TIMEZONE_LEN_MAX = 64

TIMEZONES = {
    "TZ1": [("-8.00", "(GMT -8:00) Pacific Time (US & Canada)"),
            ("-7.00", "(GMT -7:00) Mountain Time (US & Canada)"),
            ("-6.00", "(GMT -6:00) Central Time (US & Canada), Mexico City"),
            ("-5.00", "(GMT -5:00) Eastern Time (US & Canada), Bogota, Lima")],
    "TZ2": [("8.00", "(GMT +8:00) Beijing, Perth, Singapore, Hong Kong")],
    "TZ3": [("-12.00", "(GMT -12:00) Eniwetok, Kwajalein"),
            ("-11.00", "(GMT -11:00) Midway Island, Samoa"),
            ("-10.00", "(GMT -10:00) Hawaii"),
            ("-9.00", "(GMT -9:00) Alaska"),
            ("-8.00", "(GMT -8:00) Pacific Time (US & Canada)"),
            ("-7.00", "(GMT -7:00) Mountain Time (US & Canada)"),
            ("-6.00", "(GMT -6:00) Central Time (US & Canada), Mexico City"),
            ("-5.00", "(GMT -5:00) Eastern Time (US & Canada), Bogota, Lima"),
            ("-4.00", "(GMT -4:00) Atlantic Time (Canada), Caracas, La Paz"),
            ("-3.50", "(GMT -3:30) Newfoundland"),
            ("-3.00", "(GMT -3:00) Brazil, Buenos Aires, Georgetown"),
            ("-2.00", "(GMT -2:00) Mid-Atlantic"),
            ("-1.00", "(GMT -1:00 hour) Azores, Cape Verde Islands"),
            ("0.00", "(GMT) Western Europe Time, London, Lisbon, Casablanca"),
            ("1.00", "(GMT +1:00 hour) Brussels, Copenhagen, Madrid, Paris"),
            ("2.00", "(GMT +2:00) Kaliningrad, South Africa"),
            ("3.00", "(GMT +3:00) Baghdad, Riyadh, Moscow, St. Petersburg"),
            ("3.50", "(GMT +3:30) Tehran"),
            ("4.00", "(GMT +4:00) Abu Dhabi, Muscat, Baku, Tbilisi"),
            ("4.50", "(GMT +4:30) Kabul"),
            ("5.00", "(GMT +5:00) Ekaterinburg, Islamabad, Karachi, Tashkent"),
            ("5.50", "(GMT +5:30) Bombay, Calcutta, Madras, New Delhi"),
            ("5.75", "(GMT +5:45) Kathmandu"),
            ("6.00", "(GMT +6:00) Almaty, Dhaka, Colombo"),
            ("7.00", "(GMT +7:00) Bangkok, Hanoi, Jakarta"),
            ("8.00", "(GMT +8:00) Beijing, Perth, Singapore, Hong Kong"),
            ("9.00", "(GMT +9:00) Tokyo, Seoul, Osaka, Sapporo, Yakutsk"),
            ("9.50", "(GMT +9:30) Adelaide, Darwin"),
            ("10.00", "(GMT +10:00) Eastern Australia, Guam, Vladivostok"),
            ("11.00", "(GMT +11:00) Magadan, Solomon Islands, New Caledonia"),
            ("12.00", "(GMT +12:00) Auckland, Wellington, Fiji, Kamchatka")]
}

MESSAGE_PLACEHOLDER = """Please indicate how you would like us to contact you
 for the conversation to launch your complimentary service package: we offer
 conference calling via Webex and Go To Meeting, and telephony as well. Should
 you choose to leave your email, we will use it only for contact in this
 case."""

class SelectOptgroupField(SelectField):
    """
    Monkey-patched SelectField to make it support one-level optgroup.
    """

    # A really really dirty workaround, or we will get a "too many values to
    # unpack" error.
    def pre_validate(self, form):
        return True


class TimeRangeSliderField(Field):
    pass


class MakeAppointmentForm(Form):
    next = HiddenField()

    name = TextField(u'Name',
                     [Required(),
                      Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)])
    time_range = TimeRangeSliderField(u'Time Range')
    start_time = HiddenField(u'start_time')
    end_time = HiddenField(u'end_time')
    email = EmailField(u'Email',
                       [Email(),
                        Length(EMAIL_LEN_MIN, EMAIL_LEN_MAX)])
    date = DateField(u'Date',
                     [Required()],
                     default=datetime.date.today())
    timezone = SelectOptgroupField(u'Timezone',
                                   [Required(),
                                    Length(TIMEZONE_LEN_MIN,
                                           TIMEZONE_LEN_MAX)],
                                   choices=TIMEZONES)
    message = TextAreaField(u'Message',
                            [Required(),
                             Length(MESSAGE_LEN_MIN, MESSAGE_LEN_MAX)],
                            description={'placeholder': MESSAGE_PLACEHOLDER})
    submit = SubmitField('OK')
