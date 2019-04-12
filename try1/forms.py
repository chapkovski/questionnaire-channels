from django import forms
import json


class TaskForm(forms.Form):
    def __init__(self, task, *args, **kwargs):
        super().__init__(*args, **kwargs)
        q = task.question
        if task.open:
            choices = json.loads(q.chs)
            choices = ((c, c,) for c in choices)
            self.fields['question'] = forms.ChoiceField(label=q.text, choices=choices,
                                                        widget=forms.RadioSelect(),
                                                        required=True
                                                        )
        else:
            self.fields['question'] = forms.CharField(label=q.text,
                                                      required=True
                                                      )
        self.fields['question'].widget.attrs.update({'data-task': task.id})
