from django import forms
from .models import Student
from bootstrap_datepicker.widgets import DatePicker
import datetime


class DateInput(DatePicker):
    def __init__(self):
        DatePicker.__init__(self, format="%Y-%m-%d")


class StudentForm(forms.ModelForm):
    class Meta:
        widgets = {
            'birth_date': forms.DateInput(format=('%m/%d/%Y'),
                                          attrs={'class': 'form-control', 'placeholder': 'Select a date',
                                                 'type': 'date'}),
        }
        model = Student
        fields = ['name', 'birth_date', 'total']
        exclude = ['age_calculated', 'total_percentage']
