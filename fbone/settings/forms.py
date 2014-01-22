# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import (ValidationError, HiddenField, PasswordField, SubmitField)
from wtforms.validators import (Required, Length, EqualTo)
from flask.ext.login import current_user

from ..user import User
from ..utils import PASSWORD_LEN_MIN, PASSWORD_LEN_MAX


class PasswordForm(Form):
    next = HiddenField()
    password = PasswordField('Current password', [Required()])
    new_password = PasswordField('New password',
                                 [Required(),
                                  Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)])
    password_again = PasswordField('Password again',
                                   [Required(),
                                    Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX),
                                    EqualTo('new_password')])
    submit = SubmitField(u'Save')

    def validate_password(form, field):
        user = User.get_by_id(current_user.id)
        if not user.check_password(field.data):
            raise ValidationError("Password is wrong.")
