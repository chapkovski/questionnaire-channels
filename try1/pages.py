from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Task(Page):
    pass


class Results(Page):
    pass


page_sequence = [
    Task,
    Results,
]
