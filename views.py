from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import SignUpForm, LoginForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import CartItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login


@login_required
def profile(request):
    # Get the logged-in user data
    user_data = request.user

    if request.method == 'POST':
        # Handle profile update
        if 'update_profile' in request.POST:
            # Updating profile data
            username = request.POST.get('username')
            email = request.POST.get('emailprofile')
            confirm_password = request.POST.get('confirm_passwordprofile')

            # Confirm password match
            if not request.user.check_password(confirm_password):
                messages.error(request, "Password confirmation does not match")
                return redirect('profile')

            # Update username and email
            user_data.username = username
            user_data.email = email
            user_data.save()

            messages.success(request, "Profile updated successfully")
            return redirect('profile')

        # Handle profile deletion
        if 'delete_profile' in request.POST:
            user_data.delete()
            messages.success(request, "Your account has been deleted.")
            return redirect('index')  # Redirect to the homepage or login page after deletion

    # Get user's cart items (you can fetch from a cart model if you have one)
    # Assuming you have a Cart model or similar, replace with actual cart fetching logic
    cart_items_from_db = []  # Replace with your logic to get cart items from the database

    context = {
        'user_data': user_data,
        'cart_items_from_db': cart_items_from_db
    }

    return render(request, 'profile.html', context)

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('index')


# Index Route
def index(request):
    return render(request, 'index.html')

def profile(request):
    # Add your logic here, e.g., get user data and display it
    return render(request, 'profile.html')

# About Route
def about(request):
    return render(request, 'about.html')

# Contact Route
def contact(request):
    return render(request, 'contact.html')

# Shop Route
def shop(request):
    import json
    with open('data/products.json') as f:
        products = json.load(f)
    return render(request, 'shop.html', {'company': products})

# Signup View
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Create the user manually
            user = User.objects.create_user(username=username, email=email, password=password)

            # You can optionally log the user in after they sign up:
            # login(request, user)

            return redirect('index')  # Redirect to the login page or another page

    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

# Login View
def login(request):
    if request.method == 'POST':
        email = request.POST.get('username')  # You named your input 'username' in the form
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)  # Get user by email
            user = authenticate(request, username=user.username, password=password)  # Authenticate using username
            if user is not None:
                auth_login(request, user)
                messages.success(request, "Successfully logged in!")
                return redirect('index')
            else:
                messages.error(request, "Invalid email or password.")
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password.")
    
    return render(request, 'index')


# Checkout Route
def checkout(request):
    return JsonResponse({'message': 'Checkout successful'})

# Update Quantity Route
def update_quantity(request):
    return JsonResponse({'message': 'Quantity updated successfully'})


def remove_item(request, item_id):
    if request.method == 'DELETE':
        try:
            cart_item = CartItem.objects.get(id=item_id)
            cart_item.delete()
            return JsonResponse({'success': True})
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False}, status=404)
    return JsonResponse({'success': False}, status=400)


def add_item_to_cart(user_id, name, imgSrc, quantity, price):
    user = User.objects.get(id=user_id)
    cart_item = CartItem.objects.create(
        user=user,
        name=name,
        imgSrc=imgSrc,
        quantity=quantity,
        price=price
    )
    return cart_item

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('index')