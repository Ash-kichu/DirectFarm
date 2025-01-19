from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

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
    products = Product.objects.all().order_by('category')
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

@login_required(login_url='/login')
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
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # return redirect(request.POST.get('next', request.GET.get('next', '/')))
    return render(request, 'login.html')

def how_it_works_view(request):
    return render(request, 'how-it-works.html')
