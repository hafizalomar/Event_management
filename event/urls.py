from django.urls import path #type: ignore
from event.views import home, create_event, create_category, create_participant, dashbord, show_events_data, update_event, delete_event ,show_categorys_data, update_category, delete_category, show_participants_data, update_participants, delete_participants, eventDitals

urlpatterns = [
    path('', home),
    path('dashbord/', dashbord,  name="dashbord"),
    path('create_event/', create_event, name="create_event"),
    path('create_category/', create_category, name="create_category"),
    path('create_participant/', create_participant, name="create_participant"),
    path('event_ditals/<int:id>/', eventDitals, name="event_ditals"),
    path('show_events_dashbord/', show_events_data, name="events_dashbord"),
    path('update_event/<int:id>/', update_event, name="update_event"),
    path('delete_event/<int:id>/', delete_event, name="delete_event"),
    path('show_categorys_dashbord/', show_categorys_data, name="categorys_dashbord"),
    path('update_category/<int:id>/', update_category, name="update_category"),
    path('delete_category/<int:id>/', delete_category, name="delete_category"),
    path('show_participants_dashbord/', show_participants_data, name="participants_dashbord"),
    path('update_participant/<int:id>/', update_participants, name="update_participant"),
    path('delete_participant/<int:id>/', delete_participants, name="delete_participant")
]