from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from accounts.views import register, profile, visits, visit_context


app_name = "accounts"

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('<uuid:secure_id>/profile/', profile, name='profile'),
    path('<uuid:secure_id>/profile/,visits/', visits, name='visits'),
    path('<uuid:secure_id>/visits/<int:visit_id>/', visit_context, name='visit_context'),
 ]