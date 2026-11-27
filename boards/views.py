from django.http import JsonResponse
from .models import ServerRoom


def create_room(request):

    room = ServerRoom.objects.create(
        max_users=4
    )

    return JsonResponse({
        "room_code": room.code,
        "max_users": room.max_users
    })