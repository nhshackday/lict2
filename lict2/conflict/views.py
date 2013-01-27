# Create your views here.
from django.views.generic.base import RedirectView, TemplateView
from django.http import HttpResponse
from django.views.generic.list import ListView
#from django.core.paginator import Paginator
from .mongomodels import Doctor, Study
import pdb
import datetime

class RootRedirect(RedirectView):
    url = "doctors/"
    permanent = False

class DoctorListView(ListView):
    def get_queryset(self):
        return Doctor.objects.all()
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
        return Doctor.objects.filter(studies__exists=True).order_by("surname")


class SearchView(TemplateView):
    template_name = "conflict/search.html"


def SearchViewResults(request):
    search = request.__dict__.get('META').get('QUERY_STRING')

    html = "<html><body>Search: %s.</body></html>" % search
    return HttpResponse(html)

