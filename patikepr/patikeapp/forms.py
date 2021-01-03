from django.forms import ModelForm
from .models import Patike, Ocene


class PatikeForm(ModelForm):
    class Meta:
        model=Patike
        fields=['naziv','model','velicina','cena']


class OceneForm(ModelForm):
    class Meta:
        model=Ocene
        fields=['ocena','opis']