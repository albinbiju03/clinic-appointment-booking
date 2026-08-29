from django import forms
from datetime import datetime, timedelta
from .models import Appointment, Patient, Review, Service, Doctor


class BookingForm(forms.ModelForm):
    # Patient fields
    full_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Full Name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email Address'})
    )
    phone = forms.CharField(
        max_length=17,
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number'})
    )

    class Meta:
        model = Appointment
        fields = ['service', 'doctor', 'appointment_date', 'appointment_time', 'notes']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Any special requests...'}),
        }
        labels = {
            'service': 'Service',
            'doctor': 'Preferred Doctor',
            'appointment_date': 'Preferred Date',
            'appointment_time': 'Preferred Time',
            'notes': 'Additional Notes',
        }
        error_messages = {
            'service': {'required': 'Please select a service.'},
            'appointment_date': {'required': 'Please choose a date.'},
            'appointment_time': {'required': 'Please choose a time.'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].required = False
        self.fields['doctor'].empty_label = "No Preference"
        self.fields['service'].queryset = Service.objects.filter(is_active=True)
        self.fields['doctor'].queryset = Doctor.objects.filter(active=True)

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('appointment_date')
        time = cleaned_data.get('appointment_time')

        if date and time:
            slot_start = datetime.combine(date, time)
            slot_end = slot_start + timedelta(minutes=30)

            conflicts = Appointment.objects.filter(
                appointment_date=date,
                status__in=['confirmed', 'pending'],
            ).exclude(pk=self.instance.pk)

            for appt in conflicts:
                exist_start = datetime.combine(date, appt.appointment_time)
                exist_end = exist_start + timedelta(minutes=30)
                if slot_start < exist_end and exist_start < slot_end:
                    self.add_error(
                        'appointment_time',
                        'This time‑slot has already been taken. Please choose another time.'
                    )
                    break
        return cleaned_data

    def save(self, commit=True):
        email = self.cleaned_data['email']
        patient, created = Patient.objects.get_or_create(
            email=email,
            defaults={
                'full_name': self.cleaned_data['full_name'],
                'phone': self.cleaned_data['phone'],
            }
        )
        if not created:
            patient.full_name = self.cleaned_data['full_name']
            patient.phone = self.cleaned_data['phone']
            patient.save()

        appointment = super().save(commit=False)
        appointment.patient = patient
        appointment.status = 'confirmed'
        if commit:
            appointment.save()
        return appointment


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, f"{i} star{'s' if i > 1 else ''}") for i in range(1, 6)],
        widget=forms.RadioSelect,
        label='Rating',
        error_messages={'required': 'Please select a star rating.'}
    )

    class Meta:
        model = Review
        fields = ['name', 'rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Tell us about your experience...'
            }),
        }