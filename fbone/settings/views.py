# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, flash
from flask.ext.login import login_required, current_user

from ..extensions import db
from ..user import User
from .forms import PasswordForm


settings = Blueprint('settings', __name__, url_prefix='/settings')


@settings.route('/password', methods=['GET', 'POST'])
@login_required
def password():
    user = User.query.filter_by(name=current_user.name).first_or_404()
    form = PasswordForm(next=request.args.get('next'))

    if form.validate_on_submit():
        form.populate_obj(user)
        user.password = form.new_password.data

        db.session.add(user)
        db.session.commit()

        flash('Password updated.', 'success')

    return render_template('settings/password.html', user=user,
                           active="password", form=form)
