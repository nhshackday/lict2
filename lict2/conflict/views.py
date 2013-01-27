# Create your views here.
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
#from django.core.paginator import Paginator
from .mongomodels import Doctor, Study
import pdb

class RootRedirect(RedirectView):
    url = "doctors/"
    permanent = False

class DoctorListView(ListView):
    def get_queryset(self):
        return Doctor.objects.all()
    paginate_by = 2
    context_object_name = 'doctor_list'
    template_name = "conflict/doctor_list.html"

class StudyListView(ListView):
    def get_queryset(self):
        return Study.objects.all()
    paginate_by = 10
    context_object_name = 'study_list'
    template_name = 'conflict/study_list.html'
