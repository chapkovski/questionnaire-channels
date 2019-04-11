from django import forms
from try1.models import Q
import random
import json
from otree.api import widgets


class TaskForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pks = Q.objects.all().values_list('pk', flat=True)
        rpk = random.choice(pks)
        rQ = Q.objects.get(pk=rpk)
        choices = json.loads(rQ.chs)
        choices = ((c, c,) for c in choices)
        self.fields['myfield'] = forms.ChoiceField(label=rQ.text, choices=choices,
                                                   widget=widgets.RadioSelect)
