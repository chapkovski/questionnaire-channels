import csv
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from django.db import models as djmodels
import json

author = "Philip Chapkovski, chapkovski@gmail.com"

doc = """
Feeding the stream of questions to a player till he dies...

So the procedure is the following:
The guy reaches the page.
The server shows him a multiple choice question;
he provides the answer
the answer is recorded 
we show them the next one which is not answered yet correctly
when there are no unsanswerd questions he proceeds to the next page.

So we create a new answer to the question every time the client submits.
We show him the choices retrieved from the question model

We pick 
"""


class Constants(BaseConstants):
    name_in_url = 'try1'
    players_per_group = None
    num_rounds = 1
    with open('try1/quiz1.csv') as f:
        qs = list(csv.DictReader(f))
    # print(qs)


class Subsession(BaseSubsession):
    def creating_session(self):
        for q in Constants.qs:
            choices = [q.get(f'choice{i}') for i in range(1, 5)]

            Q.objects.get_or_create(id=q['id'], defaults={'text': q['question'],
                                                          'chs': json.dumps(choices),
                                                          'solution': q['solution']})


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    dump_tasks = models.LongStringField()


class Q(djmodels.Model):
    text = models.StringField()
    chs = models.StringField()
    solution = models.StringField()

    def __str__(self):
        return f'{self.text}: {self.chs}, correct answer: {self.solution}'


class Task(djmodels.Model):
    player = djmodels.ForeignKey(to=Player, related_name='tasks')
    question = djmodels.ForeignKey(to=Player, related_name='answers')
    answer = models.StringField()

