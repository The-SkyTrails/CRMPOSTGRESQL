import django_filters
from .models import Enquiry

class EnquiryFilter(django_filters.FilterSet):
    class Meta:
        model = Enquiry
        fields = ['enquiry_number']