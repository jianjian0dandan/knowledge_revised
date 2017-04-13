# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext import admin
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
            UserMixin, RoleMixin, utils
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin.contrib import sqla
from wtforms.fields import PasswordField
from wtforms import form, fields, validators


__all__ = ['admin']

# Create database connection object
db = SQLAlchemy()

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class UserAdmin(sqla.ModelView):

    # Don't display the password on the list of Users
    # column_exclude_list = ('password',)

    # Don't include the standard password field when creating or editing a User (but see below)
    # form_excluded_columns = ('password',)

    # Automatically display human-readable names for the current and available Roles when creating or editing a User
    column_auto_select_related = True

    # Prevent administration of Users unless the currently logged-in user has the "admin" role
    # def is_accessible(self):
    #     return current_user.has_role('sysadmin')

    # On the form for creating or editing a User, don't display a field corresponding to the model's password field.
    # There are two reasons for this. First, we want to encrypt the password before storing in the database. Second,
    # we want to use a password field (with the input masked) rather than a regular text field.
    # def scaffold_form(self):

    #     # Start with the standard form as provided by Flask-Admin. We've already told Flask-Admin to exclude the
    #     # password field from this form.
    #     form_class = super(UserAdmin, self).scaffold_form()

    #     # Add a password field, naming it "password2" and labeling it "New Password".
    #     form_class.password2 = PasswordField('New Password')
    #     return form_class

    # This callback executes when the user saves changes to a newly-created or edited User -- before the changes are
    # committed to the database.
    def on_model_change(self, form, model, is_created):

        # If the password field isn't blank...
        if len(model.password):
            # ... then encrypt the new password prior to storing it in the database. If the password field is blank,
            # the existing password in the database will be retained.
            model.password = generate_password_hash(model.password)



# class UserView(sqla.ModelView):
#     # def is_accessible(self):
#     #     return current_user.is_authenticated

#     def on_model_change(self, form, User, is_created):
#         User.password = form.password.data

class Role(db.Model, RoleMixin):
    """用户角色
    """
    id = db.Column(db.Integer(), primary_key=True)
    # 该用户角色名称
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __unicode__(self):
        return self.name

    def __name__(self):
        return u'角色管理'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    #confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    # Required for administrative interface. For python 3 please use __str__ instead.
    def __unicode__(self):
        return self.email

    def __name__(self):
        return u'用户管理'
   
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security()


# Create admin
admin = admin.Admin(name=u'权限管理', template_mode='bootstrap3')
