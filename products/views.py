# products/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product, Category, Feedback
from .forms import FeedbackForm, UserRegistrationForm, UserLoginForm
from django.core.management import call_command
from django.http import HttpResponse
from django.conf import settings

def run_migrations(request):
    if settings.DEBUG or request.GET.get('secret') == os.getenv('MIGRATION_SECRET'):
        try:
            call_command('makemigrations')
            call_command('migrate')
            return HttpResponse("Migrations completed")
        except Exception as e:
            return HttpResponse(f"Migration failed: {str(e)}", status=500)
    return HttpResponse("Unauthorized", status=401)

def home(request):
    featured_products = Product.objects.filter(is_available=True)[:8]
    categories = Category.objects.all()[:6]
    latest_products = Product.objects.filter(is_available=True)[:4]
    return render(request, 'products/home.html', {
        'featured_products': featured_products,
        'categories': categories,
        'latest_products': latest_products
    })

def product_list(request):
    products = Product.objects.filter(is_available=True)
    category_id = request.GET.get('category')
    search_query = request.GET.get('search')
    
    if category_id:
        products = products.filter(category_id=category_id)
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
        'search_query': search_query
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_available=True)
    feedbacks = product.feedbacks.all()[:10]
    related_products = Product.objects.filter(
        category=product.category, 
        is_available=True
    ).exclude(pk=product.pk)[:4]
    
    # Calculate average rating
    total_feedbacks = product.feedbacks.count()
    if feedbacks:
        avg_rating = sum([f.rating for f in feedbacks]) / len(feedbacks)
        avg_rating = round(avg_rating, 1)
    else:
        avg_rating = 0
    
    # WhatsApp message
    whatsapp_message = f"Hi! I'm interested in {product.name} - Price: Rs.{product.price}"
    whatsapp_number = "+923010041290"  # Client ka number yahan dalein
    
    return render(request, 'products/product_detail.html', {
        'product': product,
        'feedbacks': feedbacks,
        'related_products': related_products,
        'avg_rating': avg_rating,
        'total_feedbacks': total_feedbacks,
        'whatsapp_message': whatsapp_message,
        'whatsapp_number': whatsapp_number
    })

def category_products(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products = Product.objects.filter(category=category, is_available=True)
    
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    return render(request, 'products/category_products.html', {
        'products': products,
        'category': category
    })

# Authentication Views
def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Check if user already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists!')
                return render(request, 'auth/register.html', {'form': form})
            
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('user_login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'auth/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                next_page = request.GET.get('next', 'home')
                return redirect(next_page)
            else:
                messages.error(request, 'Invalid username or password!')
    else:
        form = UserLoginForm()
    
    return render(request, 'auth/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('home')

# Feedback Views
def add_feedback(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login to add feedback!')
        return redirect(f'/login/?next=/product/{pk}/feedback/')
    
    product = get_object_or_404(Product, pk=pk)
    
    # Check if user already gave feedback
    existing_feedback = Feedback.objects.filter(product=product, user=request.user).first()
    if existing_feedback:
        messages.info(request, 'You have already given feedback for this product!')
        return redirect('product_detail', pk=product.pk)
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.product = product
            feedback.user = request.user
            feedback.save()
            messages.success(request, 'Your feedback has been added successfully!')
            return redirect('product_detail', pk=product.pk)
    else:
        form = FeedbackForm()
    
    return render(request, 'products/add_feedback.html', {
        'form': form,
        'product': product
    })

def all_feedbacks(request, pk):
    product = get_object_or_404(Product, pk=pk)
    feedbacks = product.feedbacks.all()
    
    paginator = Paginator(feedbacks, 10)
    page_number = request.GET.get('page')
    feedbacks = paginator.get_page(page_number)
    
    return render(request, 'products/all_feedbacks.html', {
        'product': product,
        'feedbacks': feedbacks
    })
def contact(request):
    return render(request, 'products/contact.html', {'whatsapp_number': '+923010041290'})  # Replace with actual number