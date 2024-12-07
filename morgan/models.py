from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models

# Dog Profile Model
class Dog(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='dog_images/')
    video_url = models.URLField(blank=True, null=True)
    price=models.DecimalField(decimal_places=2, max_digits=4,default=99.00)

    def __str__(self):
        return self.name

# Cart Model to store selected dogs for an order
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dog= models.ForeignKey(Dog, on_delete=models.CASCADE, null=True, blank=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"

# Order Model to handle the order and notify admin
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dogs = models.ManyToManyField(Dog)
    ordered_on = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def notify_admin(self):
        send_mail(
            'New Order Notification',  # Subject of the email
            f'User {self.user.username} has placed an order with {self.dogs.count()} dogs.',  # Body of the email
            'companiondogmanagement@gmail.com',  # Sender email (replace with actual email)
            ['morganwanjala121@gmail.com'],  # Admin email
            fail_silently=False,  # If this is set to True, it will suppress any errors in case of failure
        )

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
