from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.registerUser, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('rooms/<str:pk>/',views.room, name = "room"),
    path('create-room/', views.create_room, name="create_room"),
    path('update-room/<int:pk>', views.update_room, name="update_room"),
    path('delete-room/<int:pk>', views.delete_room, name="delete_room"),
    path('delete-message/<int:pk>', views.delete_message, name="delete_message"),

    
]