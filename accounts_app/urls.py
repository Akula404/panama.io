from django.urls import path
from .import views
app_name = 'accounts_app'

urlpatterns = [
    path('register_farmer/', views.register, name="register_farmer"), # Register
    path('login/', views.login_page, name="login_page"), # Login 
    path('harvests_list/', views.harvests_list, name="harvests_list"), # Harvest list

    path('logout/', views.logout_view, name='logout'), # Logout

    path('show_harvests_list/', views.retrieve_harvests_list,name = 'show_harvests_list'),
    path('delete/<int:id>/', views.delete_harvests_list, name ='delete_harvests_list'),
    path('edit/<int:harvests_list_id>/', views.update_harvests_list, name = 'update_harvests_list'),
    
]