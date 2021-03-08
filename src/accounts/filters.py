import django_filters
from django_filters import DateFilter

from .models import *


class ProfileFilter(django_filters.FilterSet):
    class Meta:
        model = Profile  # model that will be filter
        fields = "__all__"  # which fields from that model to filter
        exclude = ["user", "date_created"]  # which fields from that model not to filter
