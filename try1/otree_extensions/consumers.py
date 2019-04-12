from channels.generic.websockets import JsonWebsocketConsumer

import random
from try1.forms import TaskForm
from try1.models import Player, Task
from django.utils.safestring import mark_safe
from django.db.models import F
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)


class TaskTracker(JsonWebsocketConsumer):
    url_pattern = (r'^/tasktracker/(?P<player_pk>[0-9]+)$')

    def clean_kwargs(self):
        self.player_pk = self.kwargs['player_pk']

    def get_player(self):
        self.clean_kwargs()
        return Player.objects.get(pk=self.player_pk)

    def process_task(self, content):
        task_id = int(content['task_id'])
        answer = content['answer']
        task = Task.objects.get(pk=task_id)
        task.answer = answer
        task.save()

    def feed_task(self):
        player = self.get_player()
        task = player.get_or_create_task()
        if task:
            form_block = mark_safe(render_to_string('try1/includes/q_block.html', {
                'form': TaskForm(task=task).as_table(),
                'player': player,
            }))

            self.send({'form_block': form_block})
        else:
            player.qs_not_available = True
            player.save()
            self.send({'over': True})

    def connect(self, message, **kwargs):
        logger.info('client connected....')
        self.feed_task()

    def receive(self, content, **kwargs):
        self.process_task(content)
        self.feed_task()
