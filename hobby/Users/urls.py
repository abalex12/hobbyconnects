# urls.py
from django.urls import path
from . import views

app_name = 'Users'


urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('confession/create/', views.create_confession, name='create_confession'),
    path('confessions/', views.confession_list, name='confession_list'),
    path('requestsend/<int:receiver_id>', views.send_crush_request, name='send_crush_request'),
    path('crush/list/', views.crush_request_list, name='crush_request_list'),
    path('crush/accept/<int:request_id>/', views.accept_crush_request, name='accept_crush_request'),
    path('crush/deny/<int:request_id>/', views.deny_crush_request, name='deny_crush_request'),
    path('message/send/<int:receiver_id>/', views.send_message, name='send_message'),
    path('message/conversation/<int:receiver_id>/', views.conversation, name='conversation'),
    path('', views.home, name='home'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('notifications/', views.notifications, name='notifications'),
    path('userlist',views.user_list, name='userlist'),
    path('matched/',views.matched_users,name='matched'),
    # Add other URL patterns here
]