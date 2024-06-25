from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic
from .forms import RoomForm
# Create your views here.

def loginPage(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(password)

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "No user found")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password not right")
    context ={}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__contains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        ) #
    room_count = rooms.count()
    topics = Topic.objects.all()

    context = {'rooms':rooms,
               'topics':topics,
               'room_count':room_count}
    return render(request, 'base/home.html',context)

def room(request, pk):
    room = Room.objects.get(id=int(pk))
    context = {'rooms':room}
    return render(request, 'base/room.html',context)

@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host :
        return HttpResponse('You are not allowed here!!')

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context ={'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def delete_room(request,pk):

    if request.user != room.host :
        return HttpResponse('You are not allowed here!!')

    room = Room.objects.get(id = pk)
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})
