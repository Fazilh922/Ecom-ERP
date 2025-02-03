from rest_framework import status, views
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import json
from .serializers import LoginSerializer  # Move this import to the top

import logging
logger = logging.getLogger(__name__)

# Renaming the view that used to be called login to avoid conflict
def login_view(request):
    return render(request, 'login.html')

class UserCreateView(views.APIView):
    def post(self, request):
        # The serializer is already imported at the top
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(views.APIView):
    def post(self, request):
        # The serializer is already imported at the top
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = serializer.validated_data['tokens']

            return Response({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                },
                'tokens': tokens,
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @csrf_protect  # Use csrf_protect instead of csrf_exempt
def register(request):
    if request.method == 'POST':
        # Handle the POST request (form submission)
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not name or not email or not password or not confirm_password:
            return JsonResponse({'error': 'All fields are required.'}, status=400)

        if password != confirm_password:
            return JsonResponse({'error': 'Passwords do not match.'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email is already registered.'}, status=400)

        user = User.objects.create(
            username=name,
            email=email,
            password=make_password(password),
            first_name=name,
        )

        return JsonResponse({'message': 'Registration successful. Please log in.'}, status=201)

    # Handle GET request to show registration form
    return render(request, 'register.html')



def forgot_password(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier')  # Phone number or email
        code = request.POST.get('code')  # Verification code (optional)
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Validate identifier
        if not identifier or not new_password or not confirm_password:
            messages.error(request, "All fields are required.")
            return redirect('forgot_password')

        try:
            if '@' in identifier:  # Email validation
                user = User.objects.get(email=identifier)
            else:  # Phone number validation (assuming phone stored in `User.profile.phone`)
                user = User.objects.get(profile__phone=identifier)
        except User.DoesNotExist:
            messages.error(request, "No user found with this information.")
            return redirect('forgot_password')

        # Check password match
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('forgot_password')

        # Update password
        user.set_password(new_password)
        user.save()

        # Optionally send a confirmation email
        send_mail(
            'Password Reset Successful',
            'Your password has been successfully reset.',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        messages.success(request, "Password reset successfully. You can now log in.")
        return redirect('login')  # Redirect to login page

    return render(request, 'forgot.html')

def index(request):
    return render(request, 'index.html')

@csrf_exempt  # Consider removing CSRF exemption if possible
def reset_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        identifier = data.get('identifier')
        code = data.get('code')
        new_password = data.get('new_password')

        if identifier and code and new_password:
            # Your logic to validate the reset request goes here
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid input data'})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})
