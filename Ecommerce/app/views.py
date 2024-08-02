from django.contrib import messages
from django.utils.decorators import method_decorator
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from app.models import Profile  # Ensure to replace 'app' with your actual app name
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render
from .models import *
from django.shortcuts import redirect
from django.http import HttpResponse
import requests
from django.contrib.auth import authenticate
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Products, Cart
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Products, Cart
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.timezone import now, timedelta
from django.urls import reverse
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User, auth


def register(request):
    if request.method == "POST":
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'username already taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password1)
                user.is_active = False  # Deactivate account till it is confirmed
                user.save()

                # Send verification email
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                activation_link = reverse(
                    'activate', kwargs={'uidb64': uid, 'token': token})
                activation_url = f"http://{
                    current_site.domain}{activation_link}"

                message = render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': uid,
                    'token': token,
                })

                send_mail(mail_subject, message,
                          'ojugbelelateef2006@gmail.com', [email])

                # messages.info(
                #     request, 'Please confirm your email address to complete the registration')
                # return redirect('signup')
                return render(request, 'confirm.html', {})
                
        else:
            messages.info(request, 'password does not match')
            return redirect('signup')
    else:
        return render(request, 'register.html', {})


User = get_user_model()


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request, user)
        messages.success(
            request, 'Your account has been activated successfully.')
        return redirect('/')
    else:
        messages.warning(
            request, 'The activation link is invalid or has expired.')
        return redirect('signup')


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user_auth = authenticate(username=username, password=password)

        if user_auth is not None:
            auth.login(request, user_auth)
            return redirect('/')
        else:
            messages.info(request, "credentials incorrect")
            return redirect('login')

    return render(request, 'login.html', {})


def logout(request):
    auth.logout(request)
    return render(request, 'logout.html')

from django.core.paginator import Paginator

def product_list(request):
    items_per_page = 8
    category = Category.objects.all()
    products = Products.objects.filter(is_available=True)
    paginator = Paginator(products, items_per_page)
    page_number = request.GET.get('page')
    product = paginator.get_page(page_number)

    context = {
        'category': category,
        'product': product,

    }
    return render(request, 'list.html', context)


def list_category(request, pk):
    items_per_page = 8
    category_get = Category.objects.get(uu_id=pk)
    category = Category.objects.all()

    products = Products.objects.filter(is_available=True, category=category_get)
    paginator = Paginator(products, items_per_page)
    page_number = request.GET.get('page')
    product = paginator.get_page(page_number)

    context = {
        'product': product,
        'category': category,
        'category_get' : category_get

    }
    return render(request, 'list.html', context)





@login_required(login_url='login')
def list_details(request, pk):
    product = get_object_or_404(Products, uu_id=pk)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user, name=product, defaults={'size': None, 'color': None})

    if request.method == 'POST':
        if 'increment' in request.POST:
            if request.POST['increment'] == 'true':
                cart_item.quantity += 1
            else:
                # Ensure quantity doesn't go below 1
                cart_item.quantity = max(cart_item.quantity - 1, 1)

            # Handle size and color selections
            if 'size' in request.POST:
                size = get_object_or_404(Size, pk=request.POST['size'])
                cart_item.size = size  # Assuming Cart model has a size field

            if 'color' in request.POST:
                color = get_object_or_404(Color, pk=request.POST['color'])
                cart_item.color = color  # Assuming Cart model has a color field

            cart_item.save()
            return JsonResponse({'quantity': cart_item.quantity})

    sizes = product.sizes.all()
    colors = product.colors.all()

    context = {
        'product': product,
        'cart': cart_item,
        'sizes': sizes,
        'colors': colors
    }
    return render(request, 'details.html', context)

@login_required(login_url='login')
def profile(request):
    user = request.user
    try:
        # Use get() to retrieve a single instance
        profile = Profile.objects.get(user=user)
    except ObjectDoesNotExist:
        profile = None  # If no profile exists, set to None

    if request.method == 'POST':
        profile_pic = request.FILES.get("profile_pic")
        bio = request.POST.get("bio")
        contact_info = request.POST.get("contact_info")
        home_address = request.POST.get("home_address")
        phone_number = request.POST.get("phone_number")

        if profile:
            # Update existing profile
            if profile_pic:
                profile.profile_picture = profile_pic
            profile.bio = bio
            profile.contact_info = contact_info
            profile.home_address = home_address
            profile.phone_number = phone_number
        else:
            # Create new profile if not exists
            profile = Profile(
                user=user,
                profile_picture=profile_pic,
                bio=bio,
                contact_info=contact_info,
                home_address=home_address,
                phone_number=phone_number
            )

        profile.save()  # Save the profile (update if existing, create if new)
        return redirect("list")

    return render(request, 'profile_form.html', {'profile': profile})



@login_required(login_url='login')
def add_cart(request, id):
    product = Products.objects.get(id=id)
    carts, created = Cart.objects.get_or_create(
        user=request.user, name=product)

    carts.is_added = True
    carts.save()
    return render(request, 'add_cart_success.html', {'product': product})



# views.py
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
import requests
from .models import Transaction

@login_required(login_url='login')
def initiate_payment(request):
    cart = Cart.objects.filter(user=request.user, name__item_remaining__gt=0)
    amount = sum(int(item.name.priceTwo) * int(item.quantity) for item in cart)

    paystack_url = 'https://api.paystack.co/transaction/initialize'

    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json',
    }
    
    callback_url = request.build_absolute_uri(reverse('send_purchase_notification'))

    data = {
        'amount': amount * 100, 
        'email': request.user.email,
        'callback_url': callback_url

    }

    response = requests.post(paystack_url, headers=headers, json=data)
    response_data = response.json()

    if response_data['status']:
        authorization_url = response_data['data']['authorization_url']
        reference = response_data['data']['reference']

        # Save the transaction reference in the database
        Transaction.objects.create(user=request.user, reference=reference, amount=amount)

        return redirect(authorization_url)
    else:
        # Handle error
        return HttpResponse('An error occurred while initiating payment.')


@login_required(login_url='login')
def cart_list(request):
    cart = Cart.objects.filter(user=request.user)
    cart_items = Cart.objects.filter(user=request.user, name__item_remaining__gt=0)
    
    # Calculate the total price for the filtered items
    total_price = sum(item.name.priceTwo * item.quantity for item in cart_items)
    return render(request, 'cart_list.html', {'cart': cart, 'total_price': total_price})


@login_required(login_url='login')
def clear_cart(request):
    cart = Cart.objects.filter(user=request.user).delete()
    messages.info(request, f"cart sucessfully cleared")
    return render(request, 'cart_list.html', {})


@login_required(login_url='login')
def remove_cart(request, id):
    cart_get = Cart.objects.get(id=id)
    cart_get.delete()
    return redirect("cart_list")


@login_required(login_url='login')
def clear_wishlist(request):
    cart = Wishlist.objects.filter(user=request.user).delete()
    messages.info(request, f"wishlist sucessfully cleared")
    return render(request, 'wishlist.html', {})


@login_required(login_url='login')
def remove_wishlist(request, id):
    cart_get = Wishlist.objects.get(id=id)
    cart_get.delete()
    return redirect("wishlist")


def search(request):

    if request.method == 'POST':
        query = request.POST["search_term"]
        product = Products.objects.filter(
            Q(title__contains=query) | Q(description__contains=query))
        count = product.count()
        context = {
            'count': count,
            'query': query,
            'product': product
        }
        return render(request, 'base.html', context)
    else:
        return render(request, 'base.html')


@login_required
@login_required(login_url='login')
def send_purchase_notification_email(request):
    # product = Products.objects.get(uu_id = pk)

    purchase = Cart.objects.filter(user=request.user,  name__item_remaining__gt=0)
    profile = Profile.objects.filter(user=request.user)

    total_price = sum(int(item.name.priceTwo) *
                      item.quantity for item in purchase)
     # Reduce item_remaining and update is_available
    for item in purchase:
        product = item.name
        product.item_remaining -= item.quantity
        if product.item_remaining <= 0:
            product.item_remaining = 0
            product.is_available = False
        product.save()

    subject = 'New Purchase Notification'
    recipient_list = ['ojugbelelateef2006@gmail.com']
    context = {
        'product_name': purchase,
        # 'quantity': quantity,
        # 'amount': amount,
        'email': request.user.email,
        'username': request.user.username,
        'total_price': total_price,
        'profile': profile




    }
    email_content = render_to_string(
        'purchase_notification_email.html', context)

    # Send the email
    send_mail(subject, email_content, settings.EMAIL_HOST_USER,
              recipient_list, html_message=email_content,  fail_silently=False)
    # product.item_remaining -= 1
    # if product.item_remaining < 0:
    #     product.is_available = False
    # else:
    #     product.is_available = True
    # product.save()
    return render(request, 'product_email.html')


@login_required(login_url='login')
def cart_base(request):
    cart = Cart.objects.filter(user=request.user)
    count_cart = cart.count()
    return render(request, 'base.html', {'count_cart' : count_cart})
    







@login_required(login_url='login')
def wishlist(request, pk):
    product = Products.objects.get(uu_id=pk)
    wishlist, created = Wishlist.objects.get_or_create(
        name=product, user=request.user)
    context = {
        'product': product,
    }

    if created:
        wishlist.is_added = True
        wishlist.save()
        return render(request, 'wishlist_successful.html', context)
        
        # return HttpResponse(f" {product} sucessfully added to wishlist")
    else:
        # return HttpResponse(f"{product} is already in wishlist")
        return render(request, 'wishlist_successful_already.html', context)



@login_required(login_url='login')
def wishlist_list(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist': wishlist})
