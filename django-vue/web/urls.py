from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from .views.auth import login_user
from .views.home import HomeView, DashboardView, TestView, PasswordView
from .views.tools import ToolsApi
#from .views.admin.home import AccountSetupView
from .views.admin.reading import AdminReadingView
from .views.admin.user import AdminUserView
# change

from .views.admin import change_user
from .views.admin.final_test import *

# change
from .views.student.home import AvatarView
from .views.student.quiz import QuizView
from .views.student.reports import StudentGeneralReportView
from .views.student.tutorial import TutorialView

from .views.admin.api.reading import AdminReadingApi

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^admin/', admin.site.urls),
    url(r'^$', HomeView.as_view(), name='index'),
    url(r'^login/$', login_user),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^update-password/$', PasswordView.as_view()),
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),

    url(r'^reading/$', AdminReadingView.as_view(), name='reading-list'),
    url(r'^reading/(?P<page_action>\D+)$', AdminReadingView.as_view(), name='reading-manager'),
    url(r'^user/$', AdminUserView.as_view(), name='user-list'),
    # change
    url(r'^active-yes/', change_user.active, name='active-yes'),
    url(r'^active-no/', change_user.archive, name='active-no'),
    url(r'^activate-test/', change_user.activate_record, name='active-yes'),
    url(r'^active-archive/', change_user.change_state, name='active-archive'),
    url(r'^individual_status/', change_user.state, name='individual-status'),
    url(r'^add_new_group/', change_user.add_group, name='add-new-group'),
    url(r'^upload/$', change_user.upload_csv, name='upload_csv'),
    url(r'^test_list/$', AdminTestingView.as_view(), name='test-list'),
    url(r'^test_list/(?P<page_action>\D+)$', AdminTestingView.as_view(), name='testing-manager'),
    url(r'^delete_group/$', change_user.delete_group, name='delete-group'),
    # end
    url(r'^report/$', StudentGeneralReportView.as_view(), name='user-general-report'),

    url(r'^user/(?P<page_action>\D+)$', AdminUserView.as_view(), name='user-manager'),
    url(r'^quiz/(?P<page_action>\D+)$', QuizView.as_view(), name='test-manager'),

    url(r'^avatar/$', AvatarView.as_view(), name='avatar'),

    url(r'^belajar/$', TutorialView.as_view(), name='tutorial-manager'),
    url(r'^tools/(?P<tool_name>(\D+))/(?P<tool_param>\D+)$', ToolsApi.as_view(), name='tools-api'),

    url(r'^api/reading/(?P<page_action>\D+)$', AdminReadingApi.as_view(), name='admin-reading-api'),

    # url(r'^account-setup/$', AccountSetupView.as_view(), name='account-setup'),
    # url(r'^test/$', TestView.as_view(), name='test'),
]