from channels.generic.websockets import JsonWebsocketConsumer
import json
from try1.forms import TaskForm
from django.http import JsonResponse
from django.utils.safestring import mark_safe

class TaskTracker(JsonWebsocketConsumer):
    url_pattern = (r'^/tasktracker/(?P<player>[0-9]+)$')

    def connect(self, message, **kwargs):

        print('client connected....')
        self.send({'myform': mark_safe(TaskForm().as_table())})
