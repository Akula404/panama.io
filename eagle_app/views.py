import requests 
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from eagle_app.credentials import LipanaMpesaPpassword, MpesaAccessToken
from django.contrib.auth.decorators import login_required
from .models import Contact
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def portfolio(request):
    return render(request, 'portfolio.html')

def service_details(request):
    return render(request, 'service-details.html')

def portfolio_details(request):
    return render(request, 'portfolio-details.html')

@login_required(login_url='accounts_app:login_page')
def contact(request):
    """ To push data to db """
    # Check if it is a POST request
    if request.method == 'POST':
        # Create a variable to pick the input fields
        contact = Contact(
            # Input fields
            name=request.POST['name'],
            email=request.POST['email'],
            subject=request.POST['subject'],
            quantity=request.POST['quantity'],
            location=request.POST['location'],
        )
        
        # Save the variables
        contact.save()

        # Redirect to a page
        return redirect('eagle_app:show_contact')
    else:
        return render(request, 'contact.html')

def retrieve_contact(request):
    """Retrieve all contacts"""
    contacts = Contact.objects.all()  # Retrieve all contacts
    if contacts.exists():
        context = {'contacts': contacts}
        return render(request, 'show_contact.html', context)
    else:
        messages.error(request, "No contacts available.")
        return redirect('eagle_app:home')


def delete_contact(request, id):
    """ Deleting """
    contact = Contact.objects.get(id=id)  # Fetch a particular contact by its ID
    contact.delete()  # Actual action of deleting
    return redirect('eagle_app:show_contact')  # Just remain on the same page

@login_required(login_url='accounts_app:login_page')
def update_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)  # Ensure user ownership
    if request.method == 'POST':
        contact.name = request.POST.get('name')
        contact.email = request.POST.get('email')
        contact.subject = request.POST.get('subject')
        contact.quantity = request.POST.get('quantity')
        contact.location = request.POST.get('location')
        contact.save()
        return redirect('show_contact')
    return render(request, 'update_contact.html', {'contact': contact})  # Corrected this line




# Adding the mpesa functions

#Display the payment form
def pay(request):
   """ Renders the form to pay """
   return render(request, 'pay.html')


# Generate the ID of the transaction
def token(request):
    """ Generates the ID of the transaction """
    consumer_key = 'qvQFfRUmIIMKcLutXyGEdAbkKtYN7RzIjVKiMz8Ma94qQt4q'
    consumer_secret = 'HRSVAAGk1AEG4ZATjzWmqYSTpGluFG6Erf8gRab85NEepozIGSmTPmR6k2Cu9Ivr'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})


# Send the stk push
def stk(request):
    """ Sends the stk push prompt """
    if request.method =="POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "Carlos LTD",
            "TransactionDesc": "Web Development Charges"
        }
        response = requests.post(api_url, json=request, headers=headers)
        return HttpResponse("Successfully sent")

