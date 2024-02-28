from io import BytesIO
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from django.http import JsonResponse
from . import steganography
from PIL import Image
import base64
from .models import Encoding, Decoding
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError

def index(request):
    return render(request, 'steganography/index.html')


def encode_image(request):
    if request.method == "POST":
        message = request.POST.get('message')
        image_file = request.FILES.get('image')
        password = request.POST.get('password')

        try:
            uploaded_image = Image.open(image_file)

            # Convert the image to PNG format if it's not already in PNG format
            if uploaded_image.format != 'PNG':
                png_buffer = BytesIO()
                uploaded_image.save(png_buffer, format='PNG')
                uploaded_image = Image.open(png_buffer)

            new_image = uploaded_image.copy()
            if password:
                steganography.encode_data_with_password(new_image, message, password)
            else:
                steganography.encode_data_into_image(new_image, message)

            encoded_image_buffer = BytesIO()
            new_image.save(encoded_image_buffer, format='PNG')

            encoded_image_base64 = base64.b64encode(encoded_image_buffer.getvalue()).decode('utf-8')

            if request.user.is_authenticated:
                encoding = Encoding(user=request.user, message=message)
                encoding.image.save('encoded_image.png', ContentFile(encoded_image_buffer.getvalue()))
                encoding.save()

            return JsonResponse({'encoded_image': encoded_image_base64})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método inválido'}, status=405)


def decode_image(request):
    if request.method == "POST":
        image_file = request.FILES.get('image')
        password = request.POST.get('password')

        try:
            image = Image.open(image_file)

            has_password = steganography.has_password(image)
            
            if not password and has_password:
                # Password required but not provided, return error message
                return JsonResponse({'error': 'This image requires a password for decoding.'}, status=400)

            if password and has_password:
                message = steganography.decode_with_password(image, password)
            else:
                message = steganography.decode(image)

            if message is None:
                return JsonResponse({'error': 'Incorrect password'}, status=400)

            if request.user.is_authenticated:
                decoding = Decoding.objects.create(user=request.user, message=message, image=image_file)
                decoding.save()

            return JsonResponse({'message': message})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método inválido'}, status=405)



def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "steganography/login.html", {
                "message": "Invalid credentials."
            })
    else:
        return render(request, "steganography/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        
        if password != confirmation:
            return render(request, "steganography/register.html", {
                "message": "Passwords must match."
            })

        try:
            validate_password(password)
        except ValidationError as e:
            return render(request, "steganography/register.html", {
                "message": " ".join(e.messages)
            })
        

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "steganography/register.html", {
                "message": "Username already taken."
            })
        
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "steganography/register.html")


@login_required
def history_view(request):
    user = request.user

    history_type = request.GET.get('type')

    if history_type == 'encoding':
        history_entries = Encoding.objects.filter(user=user).order_by('-created_at')
    elif history_type == 'decoding':
        history_entries = Decoding.objects.filter(user=user).order_by('-created_at')
    else:
        encodings = Encoding.objects.filter(user=user).order_by('-created_at')
        decodings = Decoding.objects.filter(user=user).order_by('-created_at')
        history_entries = list(encodings) + list(decodings)

    paginator = Paginator(history_entries, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'steganography/history.html', {
        'history_type': history_type,
        'page': page
    })

