from .views import RegistrationView,UsernameValidationView,EmailValidationView, VerificationView, LoginView,LogoutView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('register', RegistrationView.as_view(), name="register"),
    path('validateusername',csrf_exempt(UsernameValidationView.as_view()), name="validateusername"),
    path('validateemail',csrf_exempt(EmailValidationView.as_view()) , name="validateemail"),
    path('activate/<uidb64>/<token>',VerificationView.as_view(), name='activate'),
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),

]