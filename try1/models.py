import csv
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from django.db import models as djmodels
from django import forms
author = "Philip Chapkovski, chapkovski@gmail.com"

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'try1'
    players_per_group = None
    num_rounds = 1
    init = -1
    choices = 4
    with open('try1/quiz1.csv') as questions_file:
        reader = csv.reader(questions_file)
        for row in reader:
            question = row[0],
            ChoiceA = row[1],
            ChoiceB = row[2],
            ChoiceC = row[3],
            ChoiceD = row[4],
            Correct = row[5]
    ...



class Player(BasePlayer):
    # dump_tasks = models.LongStringField()
    num_answered1 = models.IntegerField(initial=0)
    num_correct1 = models.IntegerField(initial=0)
    submitted_answer = models.StringField(widget=widgets.RadioSelect)
    question = models.StringField()
    def current_q(self):
        question = self.current_q(Task1)
        return question

    def task(self):
        task = self.current_q(Task1)
        return task

    def choices(self):
        choices = (self.choice_a(Task1),
                   self.choice_b(Task1),
                   self.choice_c(Task1),
                   self.choice_d(Task1),
                   )
        return choices


class Task1(djmodels.Model):
    player = djmodels.ForeignKey(to=Player, related_name='task1')
    question = Constants.question
    ChoiceA = Constants.ChoiceA
    ChoiceB = Constants.ChoiceB
    ChoiceC = Constants.ChoiceC
    ChoiceD = Constants.ChoiceD
    Correct = Constants.Correct
    Choice = models.StringField()

    def current_q(self):
        Constants.init += 1
        return self.question[Constants.init]

    def choice_a(self):
        return self.ChoiceA[models.Constants.init]

    def choice_b(self):
        return self.ChoiceB[models.Constants.init]

    def choice_c(self):
        return self.ChoiceC[models.Constants.init]

    def choice_d(self):
        return self.ChoiceD[models.Constants.init]


class QuizF(forms.Form):
    submitted_answer = forms.ChoiceField(widget=widgets.RadioSelect)



class Subsession(BaseSubsession):

    ...


class Group(BaseGroup):
    ...


