from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User


class BaseView(View):
    NUM_PAGES = 30
    context = {'page': 'default'}

    def __init__(self):
        pass

    def get_context(self):
        return self.context

    def set_page(self, page_slug, page_title=None):
        self.context.update({ 'page': page_slug })
        self.context.update({ 'page_title': page_title if page_title else page_slug })

    def render(self, request, template):
        return render(request, template, self.context)


class ProtectedView(LoginRequiredMixin, BaseView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def __init__(self):
        pass


class StudentView(UserPassesTestMixin, ProtectedView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def __init__(self):
        pass

    def test_func(self):
        #return self.request.user.is_authenticated and User.objects.filter(pk=self.request.user.id, groups__name='student').exists()
        return self.request.user.is_authenticated and self.request.user.groups.filter(name='student').exists()

    def handle_no_permission(self):
        return redirect('dashboard')


class AdminView(UserPassesTestMixin, ProtectedView):

    def __init__(self):
        pass

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.groups.filter(name__in=['admin', 'teacher']).exists()

    def handle_no_permission(self):
        return redirect('dashboard')