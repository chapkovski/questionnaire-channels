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

"""


class Constants(BaseConstants):
    name_in_url = 'try1'
    players_per_group = 2
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
    qs_not_available = models.BooleanField(initial=False)  # When this is true the user asnwers all questions correctly.

    @property
    def total_attempts(self):
        """We get all tasks associated to the current user, to which he provided any answers."""
        return self.tasks.filter(answer__isnull=False).count()

    @property
    def correct_answers(self):
        """We get all tasks associated to the current user, to which he provided correct answers."""
        return self.tasks.filter(answer=F('question__solution')).count()

    @property
    def available_qs(self):
        """Here we check for all questions that already correctly answered by a user."""
        correct_qs_ids = self.tasks.filter(answer=F('question__solution')).values_list('question__id', flat=True)
        return Q.objects.exclude(id__in=correct_qs_ids)

    def get_random_question(self):
        """We pick a random question from the list of available ones.
        NB: If the list of questions  is huge it should be done differently. """
        available_qs = self.available_qs
        if available_qs.exists():
            return random.choice(available_qs)

    def get_or_create_task(self):
        """We check whether there is unfinished task, if there is we return it. If there is not, we create a new one."""
        unfinished_tasks = self.tasks.filter(answer__isnull=True)
        if unfinished_tasks.exists():
            return unfinished_tasks.latest()
        else:
            q = self.get_random_question()
            if q:
                open = random.choice([True, False])  # we create a type of question (open/multiple choice) randomly
                # Of course, this logic can be different.
                task = self.tasks.create(question=q, open=open)
                return task


class Q(djmodels.Model):
    """This model just to keep the track of all avaialble questions and their correct answers."""
    text = models.StringField()
    chs = models.StringField()
    solution = models.StringField()

    def __str__(self):
        """We do not need this but it is convenient to have when we need to print the object (mostly for debugging."""
        return f'{self.text}: {self.chs}, correct answer: {self.solution}'


class Task(djmodels.Model):
    class Meta:
        """We also do not crucially need this but it is convenient to pick just the most recent unanswered task.
        Ideally there should be just one, but just in case it is better to be safe."""
        get_latest_by = 'created_at'

    player = djmodels.ForeignKey(to=Player, related_name='tasks')
    question = djmodels.ForeignKey(to=Q, related_name='answers')
    answer = models.StringField()
    open = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)  # this and the following field is to track time
    updated_at = models.DateTimeField(auto_now=True)

    def get_answer_time(self):
        """We need this to show the question durations for the user in a nice mode."""
        sec = (self.updated_at - self.created_at).total_seconds()
        return f'{int((sec/60)%60):02d}:{int(sec):02d}'
