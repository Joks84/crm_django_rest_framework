from rest_framework.test import APITestCase
from crm.models import Tasks, User, Agent
from django.urls import reverse
from rest_framework import status
from crm.serializers import TaskListSerializer, TaskDetailSerializer
from datetime import date
from collections import OrderedDict

class TestTaskViewSet(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="jelena")
        self.agent = Agent.objects.create(user=self.user)
        self.task = Tasks.objects.create(
            headline="First Task Headline",
            body="First Task Body",
            owner=self.agent,
            progress="In Progress",
        )

    def test_list_tasks(self):
        # Testing get method - listing tasks.
        response = self.client.get(reverse('tasks-list'))
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Checking data.
        self.assertEqual(len(data[0]), 3)
        self.assertEqual(data[0]['headline'], self.task.headline)
        self.assertEqual(data[0]['task_owner_name'], self.task.owner.user.username)
        self.assertEqual(data[0]['progress'], self.task.progress)

        # Checking serializer.
        serializer = TaskListSerializer([self.task], many=True)
        self.assertEqual(serializer.data, data)

    def test_retrieve_task(self):
        # Testing retrieve method - getting one task.
        response = self.client.get(reverse('tasks-detail', args=[self.task.id]))
        self.assertEqual(reverse('tasks-detail', args=[self.task.id]), f'/tasks/{self.task.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Checking data.
        data = response.data

        self.assertEqual(data['headline'], self.task.headline)
        self.assertEqual(data['body'], self.task.body)
        self.assertEqual(data['task_owner_name'], self.task.owner.user.username)
        self.assertEqual(data['progress'], self.task.progress)
        self.assertEqual(data['date_created'], f"{date.today():%Y-%m-%d}")

        # Checking serializer.
        serializer = TaskDetailSerializer([self.task], many=True)
        self.assertEqual(serializer.data, [OrderedDict(data)])

    def test_create_task(self):
        create_data = {
            'headline': 'Task Two Headline',
            'body': 'Task Two Body',
            'owner': self.agent.id,
        }
        response = self.client.post(reverse('tasks-list'), create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.data
        self.assertEqual(data['headline'], create_data['headline'])
        self.assertEqual(data['body'], create_data['body'])
        self.assertEqual(data['task_owner_name'], self.agent.user.username)
        self.assertEqual(data['owner'], self.agent.id)
        self.assertEqual(data['progress'], 'Opened')
        self.assertEqual(data['date_created'], f"{date.today():%Y-%m-%d}")

    def test_delete_task(self):
        # Testing delete method.
        # Checking how many tasks there are before delete().
        response = self.client.get(reverse('tasks-list'))
        self.assertEqual(len(response.data), 1)
        # Deleting task.
        response = self.client.delete(reverse('tasks-detail', args=[self.task.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Checking if the task was deleted.
        response = self.client.get(reverse('tasks-list'))
        self.assertEqual(len(response.data), 0)
