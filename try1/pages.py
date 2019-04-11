from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class MyPage(Page):
    timer_text = 'Time left to complete the task:'
    timeout_seconds = 20
    form_model = 'player'
    form_fields = ['submitted_answer']
    def submitted_answer_choices(self):
        return [
            Constants.ChoiceA[Constants.init],
            Constants.ChoiceC[Constants.init],
            Constants.ChoiceB[Constants.init],
            Constants.ChoiceD[Constants.init],
        ]

page_sequence = [
    MyPage,
]
