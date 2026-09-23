from django.urls import path, include
from clients.views import ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView


app_name = "clients"

urlpatterns = [
    path('', ClientListView.as_view(), name="list"),
    path('create/', ClientCreateView.as_view(), name="create"),
    path('<int:id>/update/', ClientUpdateView.as_view(), name="update"),
    path('<int:pk>/delete/', ClientDeleteView.as_view(), name="delete"),
    path('<uuid:secure_id>/pets/', include('pets.urls'), name="pets")
]