from django.db import models
from django.contrib.auth.models import User


class Ticket(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=False)
    date = models.DateField()
    image = models.ImageField(upload_to='media/')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Название: {self.title}, Дата: {self.date},  Цена: {self.price}"


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    bought_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'ticket')


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField(max_length=500)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'ticket')

    def __str__(self):
        return f"{self.user.username} о {self.ticket.title}: {self.rating}★"


























