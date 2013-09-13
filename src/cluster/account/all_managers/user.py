# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from cluster.account.actions import ChangeUserName
from cluster.utils.forms import ClusterBaseModelForm
from cluster.utils.manager.action import AddAction, DeleteAction
from cluster.utils.manager.main import ObjectsManager, ManagerColumn
from cluster.utils.permissions import PermissionController

__author__ = 'M.Y'


class UserForm(ClusterBaseModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class UserManager(ObjectsManager):
    manager_name = u"users"
    manager_verbose_name = u"مدیریت کاربران"
    filter_form = UserForm

    actions = [DeleteAction(), ChangeUserName(), AddAction(UserForm)]

    def get_all_data(self):
        return User.objects.filter()

    def get_columns(self):
        columns = [
            ManagerColumn('first_name', u"نام", '10'),
            ManagerColumn('last_name', u"نام خانوادگی", '10'),
            ManagerColumn('username', u"نام کاربری", '10'),
            ]
        return columns

    def can_view(self):
        if PermissionController.is_admin(self.http_request.user):
            return True
        return False