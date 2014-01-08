from flask.ext.wtf import Form
from wtforms import (ValidationError, HiddenField, TextField, TextAreaField,
                     SubmitField, DateTimeField)
from wtforms.validators import Required, Length, Email
from flask.ext.wtf.html5 import EmailField

from ..user import User
from ..utils import (USERNAME_LEN_MIN, USERNAME_LEN_MAX)

CONTENT_LEN_MIN = 16
CONTENT_LEN_MAX = 1024


class MakeAppointmentForm(Form):
    next = HiddenField()

    first_name = TextField(u'Your first name.',
                           [Required(),
                            Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)])
    last_name = TextField(u'Your last name.',
                          [Required(),
                           Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)])
    email = EmailField(u'Email', [Required(), Email()])
    start_datetime = DateTimeField(u'Start Time')
    end_datetime = DateTimeField(u'End Time')
    content = TextAreaField(u'Content',
                            [Required(),
                             Length(CONTENT_LEN_MIN, CONTENT_LEN_MAX)])
    submit = SubmitField('OK')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError(u'This email is taken')
