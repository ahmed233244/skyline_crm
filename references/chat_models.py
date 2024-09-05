from django.db import models
import requests
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
class WhatsappMattermostMapping(models.Model):
    whatsapp_number = models.CharField(max_length=15, unique=True)
    mattermost_channel_id = models.CharField(max_length=64)

    def __str__(self):
        return f"WhatsApp: {self.whatsapp_number} -> Mattermost Channel: {self.mattermost_channel_id}"

class Message(models.Model):
    whatsapp_number = models.CharField(max_length=15)
    mattermost_channel_id = models.CharField(max_length=64)
    message_type = models.CharField(max_length=10, choices=[('text', 'Text'), ('image', 'Image'), ('video', 'Video'), ('document', 'Document'), ('audio', 'Audio')])
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.whatsapp_number} to {self.mattermost_channel_id} at {self.timestamp}"
class customer_service(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    password=models.CharField(max_length=50)
    assigned_channels=models.IntegerField(default=0)
    mattermost_id=models.CharField(max_length=100,default='pewgi3qaiiyamps4nbxtcjphzc')

    def __str__(self):
        return self.name
    class Meta:
        indexes = [
            models.Index(fields=['assigned_channels']),
        ]
        verbose_name = "Customer Service"
        verbose_name_plural = "Customer Service"
    @staticmethod
    def get_user_with_least_assigned_channels():
        return customer_service.objects.order_by('assigned_channels').first()

    def delete(self, *args, **kwargs):
        # Delete Mattermost user before deleting the CustomerService instance
        success = self.delete_mattermost_user()
        if success:
            super().delete(*args, **kwargs)  # Delete the instance

    def delete_mattermost_user(self):
        if self.mattermost_id:
            url = f'https://chat.skylineegypttours.com/api/v4/users/{self.mattermost_id}'
            headers = {
                'Authorization': 'Bearer edrb4ebxw78fiqazc84op9qxfr',
            }

            response = requests.delete(url, headers=headers)

            if response.status_code == 200:
                return True
            else:
                print(f"Failed to delete user in Mattermost: {response.content}")
                return False
        return True

    def add_user_to_team(self, user_id):
        team_id = 'um9hayeomjbujbcgnk7n1ozyqe'
        url = f'https://chat.skylineegypttours.com/api/v4/teams/{team_id}/members'
        headers = {
            'Authorization': 'Bearer edrb4ebxw78fiqazc84op9qxfr',
            'Content-Type': 'application/json',
        }
        data = {
            'team_id': team_id,
            'user_id': user_id,
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code != 201:
            print(f"Failed to add user to team in Mattermost: {response.content}")

@receiver(post_save, sender=customer_service)
def save_mattermost_user(sender, instance, created, **kwargs):
    if created:
        # Define your Mattermost API endpoint and token
        MATTERMOST_API_URL = 'https://chat.skylineegypttours.com/api/v4'
        MATTERMOST_API_TOKEN = 'edrb4ebxw78fiqazc84op9qxfr'

        # Construct the payload for creating a new user in Mattermost
        data = {
            "email": instance.email,  # Replace with a logic to create a unique email
            "username": instance.name.lower().replace(' ', '-'),
            "password": instance.password,  # Use a secure password logic
            "first_name": instance.name.split(' ')[0],
            "last_name": ' '.join(instance.name.split(' ')[1:]),
        }

        headers = {'Authorization': f'Bearer {MATTERMOST_API_TOKEN}', 'Content-Type': 'application/json'}

        response = requests.post(f'{MATTERMOST_API_URL}/users', headers=headers, json=data)

        if response.status_code == 201:
            # Successfully created the user in Mattermost
            mattermost_user_id = response.json().get('id')
            customer_service.add_user_to_team(instance,mattermost_user_id)
            instance.mattermost_id = mattermost_user_id
            instance.assigned_channels=customer_service.get_user_with_least_assigned_channels().assigned_channels
            instance.save()
        else:
            # Handle errors (e.g., log them)
            print(f"Failed to create Mattermost user: {response.json()}")
