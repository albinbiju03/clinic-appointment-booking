from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'clinic'

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('team/', views.team, name='team'),
    path('contact/', views.contact, name='contact'),
    path('booking/', views.booking, name='booking'),
    path('booking/success/', TemplateView.as_view(template_name='clinic/booking_success.html'), name='booking_success'),

    # 14 individual service detail pages
    path('services/cleaning/', TemplateView.as_view(template_name='clinic/services/cleaning.html'), name='service_cleaning'),
    path('services/whitening/', TemplateView.as_view(template_name='clinic/services/whitening.html'), name='service_whitening'),
    path('services/orthodontics/', TemplateView.as_view(template_name='clinic/services/orthodontics.html'), name='service_orthodontics'),
    path('services/implants/', TemplateView.as_view(template_name='clinic/services/implants.html'), name='service_implants'),
    path('services/pediatric/', TemplateView.as_view(template_name='clinic/services/pediatric.html'), name='service_pediatric'),
    path('services/veneers/', TemplateView.as_view(template_name='clinic/services/veneers.html'), name='service_veneers'),
    path('services/root-canal/', TemplateView.as_view(template_name='clinic/services/root_canal.html'), name='service_root_canal'),
    path('services/oral-surgery/', TemplateView.as_view(template_name='clinic/services/oral_surgery.html'), name='service_oral_surgery'),
    path('services/periodontics/', TemplateView.as_view(template_name='clinic/services/periodontics.html'), name='service_periodontics'),
    path('services/cosmetic-bonding/', TemplateView.as_view(template_name='clinic/services/cosmetic_bonding.html'), name='service_cosmetic_bonding'),
    path('services/dentures/', TemplateView.as_view(template_name='clinic/services/dentures.html'), name='service_dentures'),
    path('services/emergency-care/', TemplateView.as_view(template_name='clinic/services/emergency_care.html'), name='service_emergency_care'),
    path('services/same-day-crowns/', TemplateView.as_view(template_name='clinic/services/same_day_crowns.html'), name='service_same_day_crowns'),
    path('services/sedation-dentistry/', TemplateView.as_view(template_name='clinic/services/sedation_dentistry.html'), name='service_sedation_dentistry'),

    path('services/<slug:service_slug>/', views.service_detail, name='service_detail'),
path('reviews/', views.reviews, name='reviews'),


]