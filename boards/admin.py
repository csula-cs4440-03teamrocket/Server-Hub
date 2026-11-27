from django.contrib import admin
from .models import Board, ServerRoom, StickyNote, Drawing

admin.site.register(Board)
admin.site.register(StickyNote)
admin.site.register(Drawing)
admin.site.register(ServerRoom)