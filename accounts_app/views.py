from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Harvests_list

from django.contrib.auth.decorators import login_required


# Create your views here.

# Login View
def login_page(request):
    """Login view"""
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You are now logged in!")
            
            # Redirect user after login
            
            return redirect("eagle_app:home")
        else:
            messages.error(request, "Invalid login credentials")
    return render(request, 'accounts/login_page.html')


# Register View
def register(request):
    """Registration view"""
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            try:
                user = User.objects.create_user(username=username, password=password)
                user.save()

                # Notify user and redirect to login page
                messages.success(request, "Account created successfully! Please log in.")
                return redirect('accounts_app:login_page')
            except Exception as e:
                messages.error(request, f"Registration failed: {str(e)}")
        else:
            messages.error(request, "Passwords do not match. Please try again.")

    return render(request, 'accounts/register_farmer.html')

# List harvests
@login_required(login_url='accounts_app:login')
def harvests_list(request): #Function to push the booking to the db
    """ Function to push the booking to the db """
    if request.method == 'POST':  
        # Create a new Booking object and save it
        harvests_list = Harvests_list(
            name = request.POST['name'],
            produce_name = request.POST['produce_name'],
            quantity = request.POST['quantity'],
            location = request.POST['location'],
        )
        harvests_list.save()
        # Redirect to the 'index_page' after successful form submission
        return redirect('accounts_app:show_harvests_list')  # Use URL pattern name, not file path
    else:
         
        return render(request, 'accounts/harvests_list.html') 
    

        #Retrieve all appointments
def retrieve_harvests_list(request):
    """Retrieve/fetch all harvests_list"""
    #create a variable to store these contacts
    harvests_list = Harvests_list.objects.all()
    context = {
        'harvests_list':harvests_list
    }
    return render(request, 'accounts/show_harvests_list.html',context)

    #Delete
def delete_harvests_list (request,id): 
    """ Deleting """
    harvests_list = Harvests_list.objects.get(id=id) #fetch a particular contact by its ID

    harvests_list.delete() # actual action of deleting

    return redirect('accounts_app:show_harvests_list') #just remain on the same page

    #update
def update_harvests_list(request,harvests_list_id):
    """Update the query"""
    
    harvests_list = get_object_or_404(Harvests_list, id= harvests_list_id)
    context = {'harvests_list': harvests_list}
    
    #put the condition for the form to update
    if request.method == 'POST':
       harvests_list.name = request.POST.get('name')
       harvests_list.produce_name = request.POST.get('produce_name')
       harvests_list.quantity = request.POST.get('quantity')
       harvests_list.location = request.POST.get('location')
       
       harvests_list.save()

       return redirect('accounts_app:show_harvests_list')
        
    else:
        return render(request,'accounts/update_harvests_list.html',context)
    
def logout_view(request):
    """ This is for the logout view"""
    logout(request)
    messages.success(request, "You have logged out successfully.")
    return redirect('eagle_app:home')
    

