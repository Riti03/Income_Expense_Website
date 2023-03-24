from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt



urlpatterns = [
    path('',views.index,name='income'),
    path('add-income/',views.add_income,name='add-income'),
    path('edit-income/<int:id>/', views.income_edit, name="income-edit"),
    path('income-delete/<int:id>', views.delete_income, name="income-delete"),

    path('blog-page/',views.blog_page,name='blog_page'),
    
    path('consulting-page/',views.consulting_page,name='consulting_page'),
    path('consulting-page/bookings/',views.booking_page,name='booking_page'),
    path('consulting-page/checkout/<int:id>',views.checkout,name='checkout'),

    path('meetinglist/',views.meetinglist,name='meetinglist'),
    path('meetinglist/createmeeting',views.createmeetingin,name='createmeeting'),
    path('meetinglist/cancelmeeting',views.cancelmeetingin,name='cancelmeeting'),
    path('meetinglist/meetingdetails/',views.meetingdetails,name='meetingdetails'),








    path('search-income', csrf_exempt(views.search_income),name="search_income"),

]
