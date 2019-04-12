import csv
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from django.db import models as djmodels
from django.db.models import F
import json
import random

author = "Philip Chapkovski, chapkovski@gmail.com"

doc = """
Feeding the stream of questions to a player till he dies...

The logic is the following:
We need to request all questions that have no answers to it for this player
"""


class Constants(BaseConstants):
    name_in_url = 'try1'
    players_per_group = None
    num_rounds = 1
    with open('try1/quiz1.csv') as f:
        qs = list(csv.DictReader(f))


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
    qs_not_available = models.BooleanField(initial=False)

    @property
    def total_attempts(self):
        return self.tasks.filter(answer__isnull=False).count()

    @property
    def correct_answers(self):
        return self.tasks.filter(answer=F('question__solution')).count()

    @property
    def available_qs(self):
        correct_qs_ids = self.tasks.filter(answer=F('question__solution')).values_list('question__id', flat=True)
        return Q.objects.exclude(id__in=correct_qs_ids)

    def get_random_question(self):
        available_qs = self.available_qs
        if available_qs.exists():
            return random.choice(available_qs)

    def get_or_create_task(self):
        unfinished_tasks = self.tasks.filter(answer__isnull=True)
        if unfinished_tasks.exists():
            return unfinished_tasks.latest()
        else:
            q = self.get_random_question()
            if q:
                open = random.choice([True, False])
                task = self.tasks.create(question=q, open=open)
                return task


class Q(djmodels.Model):
    text = models.StringField()
    chs = models.StringField()
    solution = models.StringField()

    def __str__(self):
        return f'{self.text}: {self.chs}, correct answer: {self.solution}'


class Task(djmodels.Model):
    class Meta:
        get_latest_by = 'created_at'

    player = djmodels.ForeignKey(to=Player, related_name='tasks')
    question = djmodels.ForeignKey(to=Q, related_name='answers')
    answer = models.StringField()
    open = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_answer_time(self):
        sec = (self.updated_at - self.created_at).total_seconds()
        return f'{int((sec/60)%60):02d}:{int(sec):02d}'
