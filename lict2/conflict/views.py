# Create your views here.
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
#from django.core.paginator import Paginator
from .mongomodels import Doctor
import pdb

class RootRedirect(RedirectView):
    url = "doctors/"
    permanent = False

class DoctorListView(ListView):
    queryset = Doctor.objects.all()
    #paginator = Paginator(queryset)
    paginate_by = 2
    context_object_name = 'doctor_list'
    template_name = "conflict/doctor_list.html"
