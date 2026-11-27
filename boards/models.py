from django.db import models
import random
import string

class ServerRoom(models.Model):
    code = models.CharField(
        max_length=10,
        unique=True,
        blank=True
    )

    max_users = models.IntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        if not self.code:

            self.code = ''.join(
                random.choices(
                    string.ascii_uppercase + string.digits,
                    k=6
                )
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.code


class Board(models.Model):
    room = models.ForeignKey(
        ServerRoom,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(max_length=100)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class StickyNote(models.Model):
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE
    )

    text = models.TextField()

    x = models.IntegerField()

    y = models.IntegerField()

    color = models.CharField(
        max_length=20,
        default="yellow"
    )

    def __str__(self):
        return self.text


class Drawing(models.Model):
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE
    )

    color = models.CharField(
        max_length=20,
        default="black"
    )

    size = models.IntegerField(
        default=3
    )

    points = models.JSONField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )
