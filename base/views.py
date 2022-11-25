from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm
from .algorithms.graphs import *
from .algorithms.biLineSearch import *
from .algorithms.quickSort import *
# Create your views here.

# rooms = [
#     {'id': 1, 'name': 'Lets learn python!'},
#     {'id': 2, 'name': 'Design with me'},
#     {'id': 3, 'name': 'Frontend developers'},
# ]


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form': form})

def topic():
    topics = Topic.objects.all()
    topics = list(topics)
    quickSortName(topics, 0, len(topics) - 1)
    return topics

def home(request):
    q = request.GET.get('q')

    topics = Topic.objects.all()[0:5]

    #? Grafos - Algoritmos
    #Empieza el uso de Grafos en la págixna
    z = request.GET.get('q') if request.GET.get('q') != None else ''

    g=Grafo()
    messagesV = Message.objects.all()
    usuarios = User.objects.all()
    
    print(messagesV)
    #Se llena el grafo de vertices, donde los vertices son los usuarios
    for us in usuarios:
        a = Vertice(us.id)
        if g.agregarVertice(a):
            #print("A: " + str(a.nombre)) #! Desarrollo
            continue

    #Se ingresan en el grafo las aristas, donde las aristas son las salas 
    for mess in messagesV:
        a = Vertice(mess.user.id)
        b = Vertice(mess.room.host.id)
        g.agregarArista(a.nombre, b.nombre)
        #print("Ingresando A: " + str(a.nombre) + " B: " + str(b.nombre) + " = " + str(g.agregarArista(a, b))) #! Desarrollo
   
    #se realiza BFS
    if str(request.user) != "AnonymousUser" and request.user.id in g.vertices:
        g.bfs(g.vertices[request.user.id])

    #g.imprimeGrafo() #! Desarrollo

    #Se filtran las salas por sus topicos
    filtered_rooms = Room.objects.filter(
        Q(topic__name__icontains=z))

    recommended_rooms = []
    near_ids = []
    
    #Se filtran de nuevo las salas, ahora por su relacion con los demas usuarios
    for key in sorted(list(g.vertices.keys())):
        if g.vertices[key].distancia <= 2 and int(g.vertices[key].nombre) != int(request.user.id):
            near_ids.append(g.vertices[key].nombre)

    #print(near_ids)

    for key2 in near_ids:
        for room2 in filtered_rooms:
            if key2 == room2.host.id:
                #print(str(room2.host.name))
                recommended_rooms.append(room2)

    #? Grafos - Algoritmos

    room = Room.objects.all() #Here we receive all the room with DB
    ##Creating a python dictionary 
    room = list(room)
    
    if request.GET.get('q') != None:
        q = request.GET.get('q')
        quickSortTopic(room, 0, len(room) - 1) #? order by **Topic** (a-z) so the search can work 
        search = biLineTopic(room, 0, len(room)-1, q) #? search for the query returning the indexes
        
        filroom = []
        if search != None:
            for i in search:
                filroom.append(room[i]) #? add the rooms to a list
       
        topics = topic()[0:5] #? order by Topic (a-z)
        room_count = len(filroom)

        context = {'rooms': filroom, 'topics': topics,
               'room_count': room_count, 'recommended_rooms': recommended_rooms}
        return render(request, 'base/home.html', context)  #Return the rooms that match with the query


    quickSortName(room, 0, len(room) - 1) #? order by **name** (a-z)
    topics = topic()[0:5] #? Check the topic function


    room_count = len(room)

    context = {'rooms': room, 'topics': topics,
               'room_count': room_count, 'recommended_rooms': recommended_rooms}
    
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    print(room_messages)
    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, 'base/room.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics}
    print(room_messages)
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})

#! Cambiar para manejo de archivos
@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})


def topicsPage(request):
    topics = Topic.objects.all()
    topics = list(topics)
    quickSortName(topics, 0, len(topics) - 1)
    if request.GET.get('q') != None:
        q = request.GET.get('q')  
        topics = Topic.objects.filter(name__icontains=q)
        topics = list(topics)
        quickSortName(topics, 0, len(topics) - 1)
    return render(request, 'base/topics.html', {'topics': topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})
