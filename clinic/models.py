from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

class Service(models.Model):
    """The dental services offered."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    short_description = models.TextField(max_length=300)
    full_description = models.TextField()
    icon_class = models.CharField(max_length=50, help_text="Font Awesome class, e.g., fas fa-brush")
    badge_text = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Doctor(models.Model):
    """Dental professionals."""
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    bio = models.TextField()
    photo = models.ImageField(upload_to='doctors/', blank=True, null=True)
    email = models.EmailField(blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.name}"

class Patient(models.Model):
    """People who book appointments."""
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'.")
    phone = models.CharField(validators=[phone_regex], max_length=17)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class Appointment(models.Model):
    """Appointment bookings."""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    SERVICE_CHOICES = [
        ('General Checkup', 'General Checkup'),
        ('Teeth Cleaning', 'Teeth Cleaning'),
        ('Teeth Whitening', 'Teeth Whitening'),
        ('Root Canal', 'Root Canal'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-appointment_date', '-appointment_time']

    def __str__(self):
        return f"{self.patient.full_name} – {self.service} on {self.appointment_date}"

class ContactMessage(models.Model):
    """Messages from the contact form."""
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} – {self.subject}"

class Review(models.Model):
    name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} – {self.rating}★"