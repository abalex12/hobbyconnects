from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.http import HttpResponseForbidden

from .forms import (
    CustomUserCreationForm,
    ConfessionForm,
    MessageForm,
    CustomUserForm
)
from .models import (
    Confession,
    CrushRequest,
    Notification,
    CustomUser,
    Message
)
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('Users:login')

# Authentication views
def signup_view(request):
    # Handles user registration
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('Users:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

from django.contrib import messages

def login_view(request):
    # Handles user login
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('Users:home')
        else:
            # Send message with appropriate information when form is invalid
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# Confession views
@login_required
def create_confession(request):
    # Allows authenticated users to create confessions
    if request.method == 'POST':
        form = ConfessionForm(request.POST)
        if form.is_valid():
            confession = form.save(commit=False)
            if not confession.is_anonymous:
                confession.author = request.user
            confession.save()
            return redirect('Users:confession_list')
    else:
        form = ConfessionForm()
    return render(request, 'confession/create_confession.html', {'form': form})

def confession_list(request):
    # Displays a list of all confessions
    confessions = Confession.objects.all().order_by('-created_at')
    return render(request, 'confession/confession_list.html', {'confessions': confessions})

# Crush request views
@login_required
def send_crush_request(request, receiver_id):
    # Allows authenticated users to send crush requests
        try:
            receiver = CustomUser.objects.get(id=receiver_id)
            if receiver == request.user:
                messages.error(request, "You cannot send a crush request to yourself.")
                return redirect('Users:userlist')
            
            crush_request, created = CrushRequest.objects.get_or_create(
                sender=request.user,
                receiver=receiver
            )
            
            if created:
                Notification.objects.create(
                    user=receiver,
                    text=f"You have a new crush request from {request.user.username}"
                )
                messages.success(request, "Crush request sent successfully.")
                return redirect('Users:crush_request_list')
            else:
                messages.error(request, "You've already sent a crush request to this user.")
                return redirect('Users:userlist')
        except CustomUser.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('Users:userlist')


@login_required
def crush_request_list(request):
    # Displays a list of received and sent crush requests for the authenticated user
    received_requests = CrushRequest.objects.filter(receiver=request.user, is_matched=False)
    sent_requests = CrushRequest.objects.filter(sender=request.user)
    return render(request, 'confession/crush_request_list.html', {
        'received_requests': received_requests,
        'sent_requests': sent_requests
    })

@login_required
def accept_crush_request(request, request_id):
    # Allows users to accept crush requests
    crush_request = get_object_or_404(CrushRequest, id=request_id, receiver=request.user)
    crush_request.is_matched = True
    crush_request.save()
    Notification.objects.create(
        user=crush_request.sender,
        text=f"{request.user.username} has accepted your crush request!"
    )
    return redirect('Users:crush_request_list')
@login_required
def deny_crush_request(request, request_id):
    crush_request = get_object_or_404(CrushRequest, id=request_id,receiver=request.user)
    crush_request.is_denied = True
    crush_request.save()
    return redirect('Users:home')

   
# Message views
@login_required
def send_message(request, receiver_id):
    # Allows authenticated users to send messages to matched users
    receiver = get_object_or_404(CustomUser, id=receiver_id)
    
    # Check if users are matched and not sending to themselves
    if receiver == request.user:
        return HttpResponseForbidden("You cannot send a message to yourself.")
    
    is_matched = CrushRequest.objects.filter(
        (Q(sender=request.user, receiver=receiver) | Q(sender=receiver, receiver=request.user)),
        is_matched=True
    ).exists()
    
    if not is_matched:
        return HttpResponseForbidden("You can only send messages to matched users.")
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            Notification.objects.create(
                user=receiver,
                text=f"You have a new message from {request.user.username}"
            )
            return redirect('Users:conversation', receiver_id=receiver_id)
    else:
        form = MessageForm()
    return render(request, 'messages/send_message.html', {'form': form, 'receiver': receiver})

@login_required
def conversation(request, receiver_id):
    # Displays a conversation between the authenticated user and another user
    receiver = get_object_or_404(CustomUser, id=receiver_id)
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=receiver) | 
        Q(sender=receiver, receiver=request.user)
    ).order_by('timestamp')
    return render(request, 'messages/conversation.html', {'messages': messages, 'receiver': receiver})

@login_required
def matched_users(request):
    # Displays a list of users matched with the authenticated user
    matched_users = CustomUser.objects.filter(
        Q(sent_requests__receiver=request.user, sent_requests__is_matched=True) |
        Q(received_requests__sender=request.user, received_requests__is_matched=True)
    ).distinct()
    return  matched_users

# User profile views
@login_required
def user_profile(request, user_id):
    # Displays a user's profile
    user = get_object_or_404(CustomUser, id=user_id)
    is_own_profile = request.user == user
    return render(request, 'users/user_profile.html', {'profile_user': user, 'is_own_profile': is_own_profile})

@login_required
def edit_profile(request):
    # Allows authenticated users to edit their own profile
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('Users:user_profile', user_id=request.user.id)
    else:
        form = CustomUserForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})

# Notification views
@login_required
def notifications(request):
    # Displays and marks as read all notifications for the authenticated user
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    unread = notifications.filter(read=False)
    for notification in unread:
        notification.read = True
        notification.save()
    return render(request, 'messages/notifications.html', {'notifications': notifications})

# Home view
@login_required
def home(request):
    # Displays the home page with recent confessions, crush requests, and notifications
    recent_confessions = Confession.objects.order_by('-created_at')[:10]
    crush_requests = CrushRequest.objects.filter(
        Q(receiver=request.user) &
        Q(is_matched=False) &
        Q(is_denied=False)
    ).order_by('-date_sent')[:5]


    notifications = Notification.objects.filter(user=request.user, read=False)[:5]
    
    context = {
        
        'recent_confessions': recent_confessions,
        'crush_requests': crush_requests,
        'notifications': notifications,
        'matched_users' : matched_users(request),
    }
    return render(request, 'users/home.html', context)



@login_required
def user_list(request):
    # Displays a list of all users except the current user
    users = CustomUser.objects.exclude(id=request.user.id).order_by('username')
    return render(request, 'users/user_list.html', {'users': users})

# In your app's views.py
def custom_404(request, exception):
    return render(request, 'users/404.html', status=404)