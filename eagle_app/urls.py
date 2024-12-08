from django.urls import path
from .import views

app_name = 'eagle_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('portfolio_details/', views.portfolio_details, name='portfolio_details'),
    path('service_details/', views.service_details, name='service_details'),
    path('show_contact/', views.retrieve_contact,name = 'show_contact'),
    path('delete/<int:id>/', views.delete_contact, name ='delete_contact'),
    path('update_contact/<int:contact_id>/', views.update_contact, name = 'update_contact'),
    
    

    path('pay/', views.pay, name='pay'),  # view the payment form
    path('stk/', views.stk, name='stk'),  # send the stk push prompt
    path('token/', views.token, name='token'),  # generate the token for that particular transaction
]
