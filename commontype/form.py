from django.forms import ModelForm
from commontype.models import CommonType


class CommonTypeForm(ModelForm):
    class Meta:
        model = CommonType
        fields = ["name", "parent"]
