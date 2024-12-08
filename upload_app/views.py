from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .models import UploadedImage

# @login_required 
# Create your views here.
def upload_app(request):
    """Upload image view"""
    if request.method == 'POST':
        # Retrieve data from the form
        title = request.POST['title']
        uploaded_file = request.FILES['image']
        # Save the file using the FileSystems storage
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)
        # Save file information to the database
        image = UploadedImage.objects.create(title=title, image=filename)
        image.save()
        return render(request, 'uploads/upload_successful.html', {'file_url': file_url})
    return render(request, 'uploads/upload_app.html')
