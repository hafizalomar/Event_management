from django.shortcuts import render, redirect 
from django.contrib import messages 
from django.db.models import Q, Count
from event.models import Event, Category, Participant
from event.forms import EventModelForm, CategoryModelForm, ParticipantModelForm
from datetime import date


# Create your views here.
def home(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category_id', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    print(category_id)

    categorys = Category.objects.all()
    singleEvent = Event.objects.select_related('category').prefetch_related('participants').order_by('?').first()

    if query:
        events = Event.objects.filter(Q(name__icontains=query) | Q(location__icontains=query))
    elif category_id:
        events = Event.objects.select_related('category').filter(category_id=category_id)
    elif start_date and end_date:
        events = Event.objects.filter(date__range=[start_date, end_date])
    else:
        events = Event.objects.select_related('category').prefetch_related('participants').all()
    
    

    context = {
        "events": events,
        "query": query,
        "singleEvent": singleEvent,
        "categorys": categorys
    }

    return render(request, "home.html", context)

def eventDitals(request, id):
    event = Event.objects.select_related('category').prefetch_related('participants').get(id=id)

    context = {
        "event": event
    }

    return render(request, "event_ditals.html", context)

def dashbord(request):
    type = request.GET.get('type')
    today = date.today()
    total_participants = Participant.objects.count()

    # total_participants = Event.objects.aggregate(Count('participants'))

    counts = Event.objects.aggregate(
        total_events = Count('id'),
        upcoming_events = Count('id', filter=Q(date__gte=today)),
        past_events = Count('id', filter=Q(date__lt=today)),
    )

    if type == "total_event":
        events = Event.objects.select_related('category').prefetch_related('participants').all()
    elif type == "upcoming_events":
        events = Event.objects.select_related('category').prefetch_related('participants').filter(date__gte=today)
    elif type == "past_events":
        events = Event.objects.select_related('category').prefetch_related('participants').filter(date__lt=today)
    else:
        events = Event.objects.filter(date=today).select_related('category')

    context = {
        'events': events,
        'total_participants': total_participants,
        'counts': counts
    }

    return render(request, "new_dashbord.html", context)
    

def create_event(request):
    event_form =  EventModelForm() # For GET

    if request.method == "POST":
        event_form = EventModelForm(request.POST)

        if event_form.is_valid():

            """ For Model Form Data """
            event = event_form.save()

            messages.success(request, "Event Created Successfully")
            return redirect('create_event')

    context = {
        "event_form": event_form
    }
    return render(request, "forms/event_form.html", context)

def create_category(request):
    category_form =  CategoryModelForm() # For GET

    if request.method == "POST":
        category_form =  CategoryModelForm(request.POST)

        if category_form.is_valid():

            """ For Model Form Data """
            category = category_form.save()

            messages.success(request, "Category Created Successfully")
            return redirect('create_category')

    context = {
        "category_form": category_form
    }
    return render(request, "forms/category_form.html", context)

def create_participant(request):
    participant_form =  ParticipantModelForm() # For GET

    if request.method == "POST":
        participant_form = ParticipantModelForm(request.POST)

        if participant_form.is_valid():

            """ For Model Form Data """
            participant = participant_form.save()

            messages.success(request, "participant Created Successfully")
            return redirect('create_participant')

    context = {
        "participant_form": participant_form
    }
    return render(request, "forms/participant_form.html", context)

#event methods
def show_events_data(request):
    events = Event.objects.select_related('category').all()
    context = {
        "events": events
    }

    return render(request, "events_dashbord.html", context)

def update_event(request, id):
    event = Event.objects.get(id=id)
    event_form = EventModelForm(instance=event)

    if request.method == "POST":
        event_form = EventModelForm(request.POST, instance=event)

        if event_form.is_valid():
            """ For Model Form Data """
            event_form.save()

            messages.success(request, "Event updated Successfully")
            return redirect('events_dashbord')

    context = {"event_form": event_form}
    return render(request, "forms/event_form.html", context)


def delete_event(request, id):
    if request.method == "POST":
        event = Event.objects.get(id=id)
        event.delete()
        messages.success(request, "Event Delete Successfully")
        return redirect('events_dashbord')


# categorys metods
def show_categorys_data(request):
    categorys = Category.objects.all()
    context = {
        "categorys": categorys
    }

    return render(request, "category_dashbord.html", context)

def update_category(request, id):
    category = Category.objects.get(id=id)
    category_form = CategoryModelForm(instance=category)

    if request.method == "POST":
        category_form = CategoryModelForm(request.POST, instance=category)

        if category_form.is_valid():
            """ For Model Form Data """
            category_form.save()

            messages.success(request, "Category updated Successfully")
            return redirect('categorys_dashbord')

    context = {"category_form": category_form}
    return render(request, "forms/category_form.html", context)


def delete_category(request, id):
    if request.method == "POST":
        category = Category.objects.get(id=id)
        category.delete()
        messages.success(request, "Category Delete Successfully")
        return redirect('categorys_dashbord')
    
#participant methodes
def show_participants_data(request):
    participants = Participant.objects.all()
    context = {
        "participants": participants
    }

    return render(request, "participant_dashbord.html", context)

def update_participants (request, id):
    participant = Participant.objects.get(id=id)
    participant_form = ParticipantModelForm(instance=participant)

    if request.method == "POST":
        participant_form = ParticipantModelForm(request.POST, instance=participant)

        if participant_form.is_valid():
            """ For Model Form Data """
            participant_form.save()

            messages.success(request, "participant updated Successfully")
            return redirect('participants_dashbord')

    context = {"participant_form": participant_form}
    return render(request, "forms/participant_form.html", context)


def delete_participants(request, id):
    if request.method == "POST":
        participants = Participant.objects.get(id=id)
        participants.delete()
        messages.success(request, "Participant Delete Successfully")
        return redirect('participants_dashbord')