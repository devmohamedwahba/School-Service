from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('add_student/', views.add_student, name='add_student'),
    path('student_remove/<int:student_id>/', views.student_remove, name='student_remove'),
    path('export_csv/', views.export_csv, name='export_csv'),
    path('export_pdf/', views.export_pdf, name='export_pdf'),
    path('', views.main, name='main'),

]
