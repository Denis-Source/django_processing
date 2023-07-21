from logging import getLogger

from asgiref.sync import async_to_sync
from billiard.exceptions import SoftTimeLimitExceeded
from channels.layers import get_channel_layer

from api.v1.task.consumers import TaskMessageTypes
from api.v1.task.serializers import TaskSerializer
from core.celery import app
from task.maze.maze import Maze
from task.maze.utils import convert_to_64, image_to_file
from task.models import MazeGenerationTask, Task
from websocket.general import construct

logger = getLogger()


@app.task
def generate_maze_task(task_id):
    channel_layer = get_channel_layer()

    task = MazeGenerationTask.objects.get(id=task_id)
    task.update_status(MazeGenerationTask.Statuses.RUNNING)
    maze = Maze(task.width, task.height, task.width * 12, task.height * 12, line_width=5)

    image = None

    data = TaskSerializer(task).data
    try:
        for i, image in enumerate(maze.generate_maze(task.algorithm)):
            if i % 20 == 0:
                data["extra"] = {
                    "image": (convert_to_64(image))
                }
                async_to_sync(channel_layer.group_send)(
                    task.initiator.username,
                    construct(TaskMessageTypes.UPDATED, data))


        task.update_status(MazeGenerationTask.Statuses.FINISHED)
        if image:
            async_to_sync(channel_layer.group_send)(
                task.initiator.username,
                construct(TaskMessageTypes.UPDATED, data))

            task.set_result(image_to_file(image))
    except SoftTimeLimitExceeded:
        task.set_result(Task.Statuses.CANCELED)