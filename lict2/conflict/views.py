# Create your views here.
from django.views.generic.base import RedirectView, TemplateView
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.shortcuts import render_to_response
#from django.core.paginator import Paginator
from .mongomodels import Doctor, Study
import pdb
import datetime
import re

class RootRedirect(RedirectView):
    url = "doctors/"
    permanent = False

class DoctorListView(ListView):
    def get_queryset(self):
        term = self.request.GET.get('search')
        queryset = Doctor.objects.all().order_by("surname")
        if term:
            queryset = queryset.filter(surname__icontains=term)
        return queryset
    paginate_by = 50
    context_object_name = 'doctor_list'
    template_name = "conflict/doctor_list.html"

class StudyListView(ListView):
    def get_queryset(self):
        return Study.objects.all()
    paginate_by = 10
    context_object_name = 'study_list'
    template_name = 'conflict/study_list.html'

class LandingPage(TemplateView):
    template_name = "conflict/landing_page.html"


class InterestingDoctorListView(DoctorListView):
    def get_queryset(self):
        return super(InterestingDoctorListView, self).get_queryset().filter(studies__exists=True)


def searchViewResults(request):
    search_param = request.GET.get('search')
    if search_param:
        queryset = Doctor.objects.filter(surname=search_param).order_by("surname")

        return render(request, "conflict/doctor_list.html", {"doctor_list": queryset, "searching": "Searching for '%s'" % search_param})
    else:
        return render_to_response("conflict/search.html")

