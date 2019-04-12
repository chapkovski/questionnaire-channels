from channels.generic.websockets import JsonWebsocketConsumer
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
import logging
from try1.forms import TaskForm
from try1.models import Player, Task

logger = logging.getLogger(__name__)


class TaskTracker(JsonWebsocketConsumer):
    url_pattern = (r'^/tasktracker/(?P<player_pk>[0-9]+)$')

    def clean_kwargs(self):
        self.player_pk = self.kwargs['player_pk']

    def get_player(self):
        self.clean_kwargs()
        return Player.objects.get(pk=self.player_pk)

    def process_task(self, content):
        """We get the answer from a client, obtain task id, get it from db, and update it with actual answer."""
        task_id = int(content['task_id'])
        answer = content['answer']
        task = Task.objects.get(pk=task_id)
        task.answer = answer
        task.save()

    def feed_task(self):
        """
        We get the task, if it is available, and feed it to the form template. If it is not available we
        send an 'over' signal which forwards player to Results page.
        """
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
        """When a new client is connected we find the task and feed it back to him"""
        logger.info('client connected....')
        self.feed_task()

    def receive(self, content, **kwargs):
        """When the new message is receved, we register it (updating current task). and feed him/her back a new task."""
        self.process_task(content)
        self.feed_task()
