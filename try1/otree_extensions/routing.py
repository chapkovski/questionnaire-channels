from channels.routing import route_class
from channels.generic.websockets import JsonWebsocketConsumer
import random
from try1.models import Player
from django import forms
from otree.api import widgets


class TaskTracker(JsonWebsocketConsumer):
    url_pattern = (r'^/tasktracker/(?P<player>[0-9]+)$')

    def prepare_task(self, player, task, choice):
        return {'question': task.current_q,
                'QuizF': forms.ChoiceField(widget=widgets.RadioSelect, choices=choice),
                'choice': choice,
                'num_answered': player.num_answered1,
                'num_correct': player.num_correct1, }

    def connect(self, message, **kwargs):
        player = Player.objects.get(id=self.kwargs['player'])
        task = player.task(self)
        choices = player.choices(self)
        response = self.prepare_task(player, task, choices)
        self.send(response)

    def receive(self, text=None, bytes=None, **kwargs):
        player = Player.objects.get(id=self.kwargs['player'])
        oldtask = player.tasks.filter(answer__isnull=True).first()
        oldtask.answer = text
        oldtask.save()
        player.num_answered1 += 1
        if Player.correct == oldtask.answer:
            player.num_correct1 += 1
        task = Player.task
        choices = Player.choices
        response = self.prepare_task(player, task, choices)
        player.save()
        self.send(response)


channel_routing = [
    route_class(TaskTracker, path=TaskTracker.url_pattern),
]
