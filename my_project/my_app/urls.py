# my_app/urls.py
from django.urls import path
from my_app import views

urlpatterns = [
    path('', views.user_login, name='user_login'),
    path('registration/', views.registration, name='registration'),
    path('home/', views.Home.as_view(), name='home'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/detail/', views.profile_detail, name='profile_detail'),
    path('medicine/detail/<int:pk>/', views.MedicineDetailView.as_view(), name='medicine_details'),
    path('consultation/', views.PatientSymptome.as_view(), name="consultation"),
    path('ordonnance/<str:symptomes>/', views.CureView.as_view(), name = "cure")
]
