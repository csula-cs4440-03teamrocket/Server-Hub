from django.shortcuts import render

# Create your views here.

def lobby(request):
    return render(request, 'whiteboard/lobby.html')

def whiteboard(request):
    return render(request, 'whiteboard/whiteboard.html')

