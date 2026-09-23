from django.urls import path
from pricelist.views import pricelist, edit, create, delete, CategoryListView, CategoryCreateView, CategoryDeleteView, CategoryUpdateView


app_name = "pricelist"

urlpatterns = [
    path('', pricelist, name="list"),
    path('<int:id>/edit/', edit, name="edit"),
    path('<int:id>/delete/', delete, name="delete"),
    path('create/', create, name="create"),
    path('category/', CategoryListView.as_view(), name="category_list"),
    path('category/create/', CategoryCreateView.as_view(), name="category_create"),
    path('category/<int:pk>/update/', CategoryUpdateView.as_view(), name="category_update"),
    path('category/<int:pk>/delete/', CategoryDeleteView.as_view(), name="category_delete"),
]