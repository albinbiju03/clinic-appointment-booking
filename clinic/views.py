from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .models import Service, Doctor, Appointment, ContactMessage
from .forms import BookingForm

# ========== BASIC PAGES ==========
def home(request):
    return render(request, 'clinic/home.html')

def about(request):
    return render(request, 'clinic/about.html')

def team(request):
    doctors = Doctor.objects.filter(active=True)
    return render(request, 'clinic/team.html', {'doctors': doctors})

# ========== SERVICES ==========
def services(request):
    services = Service.objects.filter(is_active=True)
    return render(request, 'clinic/services.html', {'services': services})

def service_detail(request, service_slug):
    service = get_object_or_404(Service, slug=service_slug, is_active=True)
    return render(request, 'clinic/service_detail.html', {'service': service})

# ========== BOOKING (Email confirmation + slot conflict detection) ==========
def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            appointment = form.save()

            # ----- EMAIL CONFIRMATION -----
            patient_email = appointment.patient.email
            subject = f"Appointment Confirmation - {appointment.service.name}"
            email_message = (
                f"Dear {appointment.patient.full_name},\n\n"
                f"Your appointment for {appointment.service.name} "
                f"on {appointment.appointment_date} at {appointment.appointment_time} is confirmed.\n\n"
                f"We look forward to seeing you!\nSmileCare Dental"
            )
            try:
                send_mail(
                    subject,
                    email_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [patient_email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Email failed: {e}")

            messages.success(request, 'Your appointment has been booked! We will contact you soon.')
            return redirect('clinic:booking_success')

        else:
            # Check if the specific time‑slot error exists
            slot_conflict = False
            if 'appointment_time' in form.errors:
                for err in form.errors['appointment_time']:
                    if 'taken' in err.lower():
                        slot_conflict = True
                        break

            print("Form errors:", form.errors)   # optional, helpful for debugging
            messages.error(request, 'Please correct the errors below.')

            return render(request, 'clinic/booking.html', {
                'form': form,
                'slot_conflict': slot_conflict
            })

    else:
        form = BookingForm()

    return render(request, 'clinic/booking.html', {'form': form})

def booking_success(request):
    return render(request, 'clinic/booking_success.html')

# ========== CONTACT ==========
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message_text = request.POST.get('message')

        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=f"Contact from {name}",
            message=message_text
        )

        full_message = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message_text}"
        try:
            send_mail(
                f"New Contact Message from {name}",
                full_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent successfully!')
        except Exception as e:
            messages.error(request, 'There was an error sending your message. Please try again later.')

        return redirect('clinic:contact')

    return render(request, 'clinic/contact.html')



from .models import Review
from .forms import ReviewForm

def reviews(request):
    all_reviews = Review.objects.all()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your review!')
            return redirect('clinic:reviews')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ReviewForm()

    return render(request, 'clinic/reviews.html', {
        'reviews': all_reviews,
        'form': form
    })