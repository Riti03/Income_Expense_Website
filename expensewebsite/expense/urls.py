from django.urls import path
from . import views



urlpatterns = [
    path('',views.index,name='expense'),
    path('addexpense',views.add_expense,name='addexpense')

]
