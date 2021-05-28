""" Defines the views for the profiles app """
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from boxoffice.models import Order

from .models import UserProfile
from .forms import UserInfoForm, UserProfileForm


@login_required
def profile(request):
    """ A View to show a logged in user their own profile """
    # Get the current user's profile
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        user_form = UserInfoForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile information has been updated successfully.')
        else:
            messages.error(request, 'Profile update failed. Please ensure your details are valid.')
    else:
        # Construct the user's forms
        user_form = UserInfoForm(instance=user_profile.user)
        profile_form = UserProfileForm(instance=user_profile)

    # Get the user's previous orders
    orders = user_profile.orders.all()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'orders': orders,
    }

    return render(request, 'profiles/profile.html', context)


def order_history(request, order_number):
    """ Renders a single previous order """
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, 'This is a past confirmation. A confirmation email \
                                was sent on the order date.')

    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, 'boxoffice/checkout_success.html', context)


# Retained for future use
# @require_POST
# @login_required
# def load_order_page(request, page):
#     pass
