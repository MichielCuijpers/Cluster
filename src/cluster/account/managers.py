# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from cluster.account.actions import DeleteUserAction, ChangeUserName
from cluster.utils.forms import ClusterBaseModelForm
from cluster.utils.manager.action import AddAction
from cluster.utils.manager.main import ObjectsManager, ManagerColumn

__author__ = 'M.Y'


class UserForm(ClusterBaseModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class UserManager(ObjectsManager):
    manager_name = u"users"
    manager_verbose_name = u"کاربران"
    filter_form = UserForm

    actions = [DeleteUserAction(), ChangeUserName(), AddAction(UserForm)]

    def get_all_data(self):
        return User.objects.filter()

    def get_columns(self):
        columns = [
            ManagerColumn('first_name', u"نام", '10'),
            ManagerColumn('last_name', u"نام خانوادگی", '10'),
            ManagerColumn('username', u"نام کاربری", '10'),
        ]
        return columns
