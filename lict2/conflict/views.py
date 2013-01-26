# Create your views here.
from django.views.generic.list import ListView
from .mongomodels import Doctor

class DoctorListView(ListView):
    queryset = Doctor.objects.all()
    context_object_name = 'doctor_list'
    template_name = "conflict/doctor_list.html"
