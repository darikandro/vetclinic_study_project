from django.urls import path
from pets.views import create, admin_page, admin_create


app_name = "pets"

urlpatterns = [
    path('create/', create, name="create"),
    path('<int:pet_id>/admin_page/', admin_page, name="admin_page"),
    path('<int:id>/create/', admin_create, name="admin_create"),
]