from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Profile
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.http import JsonResponse

from .models import Product, Cart, CartItem, Order, OrderItem, Review, Category, Record

# Home page view
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

# Shop page view
def shop_view(request):
    try:
        products = Product.objects.all().order_by('created_at')
        categories = Category.objects.filter(parent__isnull=True)

        category_id = request.GET.get('category')
        if category_id:
            products = products.filter(category_id=category_id)

        delivery_region = request.GET.get('delivery_region')
        if delivery_region:
            products = products.filter(farmer__location=delivery_region)

        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        if min_price and max_price:
            products = products.filter(price__gte=min_price, price__lte=max_price)

        rating = request.GET.get('rating')
        if rating:
            products = products.filter(rating__gte=rating)

        farmer = request.GET.get('farmer')
        if farmer:
            products = products.filter(farmer_id=farmer)

        sort_by = request.GET.get('sort_by')
        if sort_by == 'price':
            products = products.order_by('offer_price')
        elif sort_by == 'rating':
            products = products.order_by('-rating')
        else:
            products = products.order_by('-created_at')

        farmers = Profile.objects.filter(user_type='Farmer')

        context = {
            'products': products,
            'farmers': farmers,
            'categories': categories
        }
        return render(request, 'shop.html', context)
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
        return redirect('shop')

def shop_view_by_farmer(request, farmer_id):
    products = Product.objects.filter(farmer_id=farmer_id).order_by('created_at')
    context = {
        'products': products,
    }
    return render(request, 'shop.html', context)

def shop_view_by_category(request, category):
    products = Product.objects.filter(category=category).order_by('created_at')
    context = {
        'products': products,
    }
    return render(request, 'shop.html', context)

# About page view
def about_view(request):
    return render(request, 'about.html')

# Farmers page view
def farmers_view(request):
    farmers = Profile.objects.filter(user_type='Farmer')
    context = {'farmers': farmers}
    return render(request, 'farmers.html', context)

# Contact page view
def contact_view(request):
    return render(request, 'contact.html')

# Account page view
@login_required(login_url='/login/?next=/account/')
def account_view(request):
    profile = Profile.objects.get(user=request.user)
    profile.dob = profile.dob.strftime('%Y-%m-%d') if profile.dob else ''
    context = {'profile': profile}
    return render(request, 'profile.html', context)

# Update profile view
@login_required(login_url='/login/?next=/account/')
def update_profile_view(request):
    try:
        if request.method == 'POST':
            user = request.user
            profile = Profile.objects.get(user=user)

            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            profile.phone = request.POST['phone']
            profile.address = request.POST['address']
            profile.location = request.POST['location']
            profile.dob = request.POST['dob']
            profile.user_type = request.POST['user_type']

            if profile.user_type == 'Farmer':
                profile.farm_name = request.POST.get('farm_name', '')
                profile.farm_description = request.POST.get('farm_description', '')
            else:
                profile.farm_name = ''
                profile.farm_description = ''

            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']

            user.save()
            profile.save()

            messages.success(request, 'Profile updated successfully')
            return redirect('account')

        return render(request, 'profile.html', {'profile': profile})
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
        return redirect('account')

# Orders page view
@login_required(login_url='/login/?next=/account/')
def orders_view(request):
    orders = Order.objects.filter(user=request.user.profile)
    context = {'orders': orders}
    return render(request, 'orders.html', context)

# Products page view
@login_required(login_url='/login/?next=/account/')
def products_view(request):
    if request.user.profile.user_type != 'Farmer':
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('account')
    
    products = Product.objects.filter(farmer=request.user.profile)
    context = {'products': products}
    return render(request, 'products.html', context)

def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)
        price = request.POST.get('price')
        stock_quantity = request.POST.get('stock_quantity')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        offer_price = request.POST.get('offer_price') or price
        offer_percentage = request.POST.get('offer_percentage') or 0

        if not all([name, category, price, stock_quantity, description, image]):
            messages.error(request, 'All fields are required.')
            return render(request, 'add_product.html', {'categories': Category.objects.all()})

        try:
            price = float(price)
            stock_quantity = int(stock_quantity)
            offer_percentage = int(offer_percentage) if offer_percentage else None
        except ValueError:
            messages.error(request, 'Invalid price, stock quantity, offer price, or offer percentage.')
            return render(request, 'add_product.html', {'categories': Category.objects.all()})

        product = Product(
            name=name,
            category=category,
            price=price,
            stock_quantity=stock_quantity,
            description=description,
            image=image,
            offer_price=offer_price,
            offer_percentage=offer_percentage,
            farmer=request.user.profile
        )

        try:
            product.full_clean()
            product.save()
            messages.success(request, 'Product added successfully.')
            return redirect('products')
        except ValidationError as e:
            messages.error(request, e.message_dict)
            return render(request, 'add_product.html', {'categories': Category.objects.all()})

    return render(request, 'add_product.html', {'categories': Category.objects.all()})

@login_required(login_url='/login/?next=/account/')
def edit_product(request, product_id):
    product = Product.objects.get(id=product_id, farmer=request.user.profile)
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)
        price = request.POST.get('price')
        stock_quantity = request.POST.get('stock_quantity')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        offer_price = request.POST.get('offer_price') or price
        offer_percentage = request.POST.get('offer_percentage') or 0

        if not all([name, category, price, stock_quantity, description]):
            messages.error(request, 'All fields except image are required.')
            return render(request, 'edit_product.html', {'product': product})

        try:
            price = float(price)
            stock_quantity = int(stock_quantity)
            offer_percentage = int(offer_percentage) if offer_percentage else None
        except ValueError:
            messages.error(request, 'Invalid price, stock quantity, offer price, or offer percentage.')
            return render(request, 'edit_product.html', {'product': product})

        product.name = name
        product.category = category
        product.price = price
        product.stock_quantity = stock_quantity
        product.description = description
        product.offer_price = offer_price
        product.offer_percentage = offer_percentage
        if image:
            product.image = image

        try:
            product.full_clean()
            product.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('products')
        except ValidationError as e:
            messages.error(request, e.message_dict)
            return render(request, 'edit_product.html', {'product': product})
    context = {
        'product': product,
        'categories': Category.objects.all(),
    }
    return render(request, 'edit_product.html', context)

@login_required(login_url='/login/?next=/account/')
def delete_product(request, product_id):
    product = Product.objects.get(id=product_id, farmer=request.user.profile)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('products')
    return render(request, 'confirm_delete_product.html', {'product': product})

# Single product page view
def product_detail_view(request, product_id):
    product = Product.objects.get(id=product_id)
    similar_products = Product.objects.filter(category=product.category).exclude(id=product_id)[:4]

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        Review.objects.create(product=product, user=request.user, rating=rating, comment=comment)
        product.update_rating()
        messages.success(request, 'Review added successfully!')
        return redirect('product_detail', product_id=product_id)

    context = {
        'product': product,
        'similar_products': similar_products
    }
    return render(request, 'product_detail.html', context)

# Confirm logout view
def confirm_logout_view(request):
    return render(request, 'logout.html')

# Logout view
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Logged out successfully!')
    return render(request, 'home.html', {'messages': messages.get_messages(request)})

# Cart view
@login_required(login_url='/login/?next=/cart/')
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user.profile)
    cart_items = CartItem.objects.filter(cart=cart)
    context = {'cart_items': cart_items}
    return render(request, 'cart.html', context)

@login_required(login_url='/login/?next=/cart/')
def add_to_cart_view(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        if request.user.profile.user_type == 'Farmer' and product.farmer == request.user.profile:
            messages.error(request, 'You cannot add your own product to the cart.')
            return redirect(request.META.get('HTTP_REFERER', 'shop'))
        cart, created = Cart.objects.get_or_create(user=request.user.profile)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        messages.success(request, f'{product.name} added to cart.')
        return redirect(request.META.get('HTTP_REFERER', 'shop'))
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
        return redirect('shop')

@login_required(login_url='/login/?next=/cart/')
def remove_from_cart_view(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id, cart__user=request.user.profile)
    cart_item.delete()
    messages.success(request, f'{cart_item.product.name} removed from cart.')
    return redirect('cart')

@login_required(login_url='/login/?next=/cart/')
def increment_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

@login_required(login_url='/login/?next=/cart/')
def decrement_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('cart')

@login_required(login_url='/login/?next=/checkout/')
def checkout_view(request):
    cart = get_object_or_404(Cart, user=request.user.profile)
    cart_items = CartItem.objects.filter(cart=cart)
    
    if request.method == 'POST':
        total_price = sum(item.product.offer_price * item.quantity for item in cart_items)
        order = Order.objects.create(user=request.user.profile, total_price=total_price)
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.offer_price
            )
        cart_items.delete()
        messages.success(request, 'Order placed successfully!')
        return redirect('orders')
    
    context = {'cart_items': cart_items}
    return render(request, 'checkout.html', context)

# Checkout view
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

        # Validate date of birth format
        try:
            datetime.strptime(dob, '%Y-%m-%d')
        except ValueError:
            messages.error(request, 'Invalid date format. It must be in YYYY-MM-DD format.')
            return render(request, 'signup.html', {'messages': messages.get_messages(request)})

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
        elif Profile.objects.filter(phone=phone).exists():
            messages.error(request, 'Phone number already exists')
        else:
            try:
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password
                )
                Profile.objects.create(
                    user=user,
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
                login(request, user)
                messages.success(request, 'Account created successfully')
                return redirect('home')
            except IntegrityError:
                messages.error(request, 'Username already exists')

    return render(request, 'signup.html', {'messages': messages.get_messages(request)})

# Login view
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

# Forgot password view
def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            # Logic to send password reset email goes here
            messages.success(request, 'Password reset email sent successfully.')
        except User.DoesNotExist:
            messages.error(request, 'No account found with that email address.')
    return render(request, 'forgot-password.html', {'messages': messages.get_messages(request)})

# How it works view
def how_it_works_view(request):
    return render(request, 'how-it-works.html')

def custom_404(request, exception):
    return render(request, '404.html', status=404)

@require_POST
@login_required(login_url='/login/?next=/checkout/')
def buy_now_view(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        if request.user.profile.user_type == 'Farmer' and product.farmer == request.user.profile:
            messages.error(request, 'You cannot buy your own product.')
            return redirect(request.META.get('HTTP_REFERER', 'shop'))
        cart, created = Cart.objects.get_or_create(user=request.user.profile)
        cart.cartitem_set.all().delete()  # Clear the cart
        CartItem.objects.create(cart=cart, product=product, quantity=1)
        return redirect('checkout')
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
        return redirect('shop')

@login_required(login_url='/login/?next=/account/')
def customer_orders_view(request):
    if request.user.profile.user_type != 'Farmer':
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('account')

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = Order.objects.filter(id=order_id, orderitem__product__farmer=request.user.profile).distinct().first()
        if order:
            order.status = 'Completed'
            order.save()
            messages.success(request, f'Order {order_id} marked as completed.')
        else:
            messages.error(request, 'Order not found or you do not have permission to update this order.')

    orders = Order.objects.filter(orderitem__product__farmer=request.user.profile).distinct()
    context = {'orders': orders}
    return render(request, 'customer_orders.html', context)

@login_required(login_url='/login/?next=/account/')
def categories_view(request):
    if request.user.profile.user_type != 'Farmer':
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('account')

    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'categories.html', context)

@login_required(login_url='/login/?next=/account/')
def add_category_view(request):
    if request.user.profile.user_type != 'Farmer':
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('account')

    if request.method == 'POST':
        name = request.POST.get('name')
        parent_id = request.POST.get('parent')
        parent = Category.objects.get(id=parent_id) if parent_id else None

        Category.objects.create(name=name, parent=parent)
        messages.success(request, 'Category added successfully.')
        return redirect('categories')

    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'add_category.html', context)

def records_view(request):
    records_list = Record.objects.all().order_by('-date')
    paginator = Paginator(records_list, 10)  # Show 10 records per page
    page_number = request.GET.get('page')
    records = paginator.get_page(page_number)

    # Convert records to a list of dictionaries for JSON serialization
    records_data = json.dumps(
        list(records_list.values('product__id', 'product__name', 'farmer__user__username', 'price', 'date')),
        cls=DjangoJSONEncoder
    )

    products = Product.objects.all()

    context = {'records': records, 'records_data': records_data, 'products': products}
    return render(request, 'records.html', context)

def get_filtered_records(request):
    product_id = request.GET.get('product_id')
    if (product_id):
        records_list = Record.objects.filter(product_id=product_id).order_by('date')
    else:
        records_list = Record.objects.all().order_by('date')

    records_data = list(records_list.values('product__id', 'product__name', 'farmer__user__username', 'price', 'date'))
    return JsonResponse(records_data, safe=False)

