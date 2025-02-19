from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import F
from .models import User
from django.contrib import messages

from .models import Product

# Create your views here.
def home_view(request):
    reviews = [
        {
            "content": "DirectFarm has completely changed the way we buy produce. We love knowing exactly where our food is coming from, and everything we’ve ordered has been incredibly fresh. It feels great to support local farmers!", "author": "Customer"
        },
        {
            "content": "As someone who values sustainable food, DirectFarm is perfect. The produce is always top-quality, and I love that it’s farm-to-table. I’m never going back to the grocery store for vegetables!", "author": "Customer"
        },
        {
            "content": "The variety and quality of produce from DirectFarm is amazing! I can taste the difference, and I feel like I’m doing my part to support our local farmers. It’s fresh, fair, and reliable.", "author": "Customer"
        },
    ]
    context = {'reviews': reviews}

    return render(request, 'home.html', context)

def shop_view(request):
    products =Product.objects.annotate(final_price=F('price') - F('offer_price')).order_by('category')
    
    context = {
        'products' : products,
    }
    return render(request, 'shop.html', context)

def about_view(request):
    return render(request, 'about.html')

def farmers_view(request):
    return render(request, 'farmers.html')

def contact_view(request):
    return render(request, 'contact.html')

@login_required(login_url='/login/?next=/account/')
def account_view(request):
    return render(request, 'profile.html')

def orders_view(request):
    return render(request, 'orders.html')

@login_required(login_url='login')
def preferences_view(request):
    return render(request, 'preferences.html')

def confirm_logout_view(request):
    return render(request, 'logout.html')

def logout_view(request):
    if request.method == 'POST':
        print('Logging out')
        logout(request)
    return redirect(request.GET.get('next', '/'))

def cart_view(request):
    return render(request, 'cart.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        user_type = request.POST['user_type']
        gender = request.POST['gender']
        dob = request.POST['dob']
        phone = request.POST['phone']
        address = request.POST['address']
        location = request.POST['location']
        profile_picture = request.FILES.get('profile-picture')
        farm_name = request.POST.get('farm_name', '')
        farm_description = request.POST.get('farm_description', '')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
        else:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                user_type=user_type,
                gender=gender,
                dob=dob,
                phone=phone,
                address=address,
                location=location,
                farm_name=farm_name,
                farm_description=farm_description,
                profile_picture=profile_picture
            )
            user.save()
            login(request, user)
            messages.success(request, 'Account created successfully')
            return redirect('home')

    return render(request, 'signup.html', {'messages': messages.get_messages(request)})

def login_view(request):
    next_url = request.GET.get('next', '/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully')
            return redirect(request.POST.get('next', next_url))
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html', {'next': next_url, 'messages': messages.get_messages(request)})

def how_it_works_view(request):
    return render(request, 'how-it-works.html')
