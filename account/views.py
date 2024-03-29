from django.contrib import messages
from store.models import Product
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from store.models import Product
from orders.views import user_orders
from orders.models import Order

from .forms import RegistrationForm, UserEditForm, UserAddressForm
from .models import Customer, Address
from .token import account_activation_token

@login_required
def wishlist(request):
    product = Product.objects.filter(users_wishlist=request.user)
    return render(request, 'account/dashboard/user_wish_list.html', {"wishlist": product})

@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)   
    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
        messages.success(request, product.title + " has been removed from your wish list")
    else:
        product.users_wishlist.add(request.user)
        messages.success(request, "Added " + product.title + " to your wish list")
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def dashboard(request):
    orders = user_orders(request)
    return render(request,
                  'account/dashboard/dashboard.html',
                  {'section': 'profile', 'orders': orders})


@login_required
def edit_details(request):
    if request.method == 'POST':
        print("got the post")
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user = Customer.objects.get(email=request.user.email)
            user.name = user_form.cleaned_data['first_name']
            user.save()
            return redirect('account:dashboard')
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request,
                  'account/dashboard/edit_details.html', {'user_form': user_form})


@login_required
def delete_user(request):
    user = Customer.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')


def account_register(request):

    if request.user.is_authenticated:
        return redirect('account:dashboard')

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            blacklistedaccounts = Customer.objects.filter(is_blacklisted=True, email=registerForm.cleaned_data['email'])
            if not blacklistedaccounts.exists():
                user = registerForm.save(commit=False)
                user.email = registerForm.cleaned_data['email']
                user.name = registerForm.cleaned_data['user_name']
                user.set_password(registerForm.cleaned_data['password'])
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                subject = 'Activate your Account'
                message = render_to_string('account/registration/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                user.email_user(subject=subject, message=message)
                return render(request, 'account/registration/register_confirm.html')
            else:
                return HttpResponse("Error handler content", status=400)
    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': registerForm})


def account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        print(user)
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')

# Addresses

@login_required
def view_address(request):
    addresses = Address.objects.filter(customer=request.user)
    return render(request, "account/dashboard/addresses.html", {"addresses": addresses})


@login_required
def add_address(request):
    if request.method == "POST":
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address_form = UserAddressForm()
    return render(request, "account/dashboard/edit_addresses.html", {"form": address_form})

@login_required
def edit_address(request, id):
    if request.method == "POST":
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address)
    return render(request, "account/dashboard/edit_addresses.html", {"form": address_form})

@login_required
def delete_address(request, id):
    address = Address.objects.filter(pk=id, customer=request.user).delete()
    return redirect("account:addresses")

@login_required
def set_default(request, id):
    Address.objects.filter(customer=request.user, default=True).update(default=False)
    Address.objects.filter(pk=id, customer=request.user).update(default=True)
    previous_url = request.META.get("HTTP_REFERER")

    if "delivery_address" in previous_url:
        return redirect("checkout:delivery_address")

    return redirect("account:addresses")

@login_required
def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return render(request, "account/dashboard/user_orders.html", {"orders": orders})

@login_required
def recently_viewed(request):
    user = get_object_or_404(Customer, id=request.user.id)
    viewhistory = user.viewhistory
    print(viewhistory)
    try:
        viewhistory_list = [int(s) for s in viewhistory.split(',')]
        viewhistory_list.reverse()
        products = Product.objects.filter(id__in=viewhistory_list)
        print(products)
    except:
        products = ""
    return render(request, "account/dashboard/recently_viewed.html", {"products": products})
