from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Task(Page):
    timeout_seconds = 5
    def is_displayed(self) -> bool:
        return not self.player.qs_not_available


class Results(Page):
    pass


page_sequence = [
    Task,
    Results,
]
