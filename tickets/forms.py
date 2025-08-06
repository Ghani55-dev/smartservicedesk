from django import forms
from .models import Ticket
from core.models import User

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority']

class AssignTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['assigned_to']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.filter(role='agent')

class UpdateStatusForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status']
