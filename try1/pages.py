from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class IntroTask(Page):
    template_name = 'try1/Task.html'
    def is_displayed(self) -> bool:
        return not self.player.qs_not_available

    def vars_for_template(self) -> dict:
        return {'channel_stem': 'intro_task'}


class Results(Page):
    pass


class SecondTask(Page):
    template_name = 'try1/Task.html'
    def vars_for_template(self) -> dict:
        return {'channel_stem': 'real_task'}

    def is_displayed(self) -> bool:
        return not self.player.qs_not_available


page_sequence = [
    IntroTask,
    Results,
    SecondTask,
]
