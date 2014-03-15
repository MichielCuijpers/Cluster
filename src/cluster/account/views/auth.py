# -*- coding:utf-8 -*-
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.static import serve
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from cluster.account.account.models import Member
from cluster.account.forms import SignInForm
from cluster.news.models import File
from cluster.project.models import ProjectArbiter, Project, ProjectReport
from cluster.utils.permissions import PermissionController
from django.conf import settings
__author__ = 'M.Y'


def login_view(request):
    if request.method == 'POST':
        login_form = SignInForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is None or not user.is_active:
                messages.error(request, u"نام کاربری یا گذرواژه نادرست است.")
            elif PermissionController.is_member(user) and user.member.is_confirmed is False:
                messages.error(request, u"ثبت نام شما از طرف مدیریت رد شده است و نمی توانید در سامانه وارد شوید.")
            else:
                login(request, user)
                next_page = request.GET.get('next')
                #if PermissionController.is_admin(user):
                #    ProjectMilestone.check_milestones()
                if next_page:
                    return HttpResponseRedirect(next_page)
                else:
                    return HttpResponseRedirect(PermissionController.get_user_redirect_url(user))
    else:
        login_form = SignInForm()

    return render_to_response('accounts/login_page.html', {'login_form': login_form},
                              context_instance=RequestContext(request))


mapping = {
    'attachments': File,
    'education_certificates':Member,
    'elite_certificates':Member,
    'member_images':Member,
    'national_id_cards':Member,
    'project_arbiter_attachments':ProjectArbiter,
    'project_certificate_images':Project,
    'project_intro_attachments':Project,
    'project_patents':Project,
    'project_proposal':Project,
    'project_reports':ProjectReport,
    'arbiter_form.docx': 1,
    'prop':1
}

@login_required
def get_media(request,path):
    def return_file(path,send=True):
        if not send:
            raise Http404()
        return serve(request, path, document_root=settings.MEDIA_ROOT, show_indexes=False)

    if not path:
        return return_file(path,False)
    try:
        id = path.split('!target_id=')[1]
        path = path.split('!target_id=')[0]
    except:
        return return_file(path,False)
    try:
        slug = path.split('/')[0]
    except:
        return return_file(path,False)
    klass = mapping.get(slug,None)
    if not klass:
        return return_file(path,False)
    if klass == 1:
        return return_file(path)
    object = klass.objects.get(pk=id)
    if PermissionController().is_admin(request.user) or PermissionController().is_supervisor(request.user):
        return return_file(path)
    if PermissionController().is_arbiter(request.user) and not isinstance(klass,Member):
        return return_file(path)
    if PermissionController().is_member(request.user):
        try:
            member = request.user.member
        except:
            return return_file(path,False)
        if not member:
            return return_file(path,False)
        if member == object:
            return return_file(path)
        if isinstance(object,Project):
            if check_project_access(object,member):
                return return_file(path)
        if isinstance(object,ProjectReport):
            if check_project_access(object.project,member):
                return return_file(path)
    return return_file(path,False)



def check_project_access(object,member):
    if object.cluster:
        if object.cluster.head == member:
            return True
        for item in object.cluster.members.all():
            if item == member:
                return True
    else:
        if member == object.single_member:
            return True
    return False
