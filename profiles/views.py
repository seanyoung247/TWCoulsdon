from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import UserProfile
from .forms import UserInfoForm, UserProfileForm


@login_required
def profile(request):
    """ A View to show a logged in user their own profile """
    # Get the current user's profile
    profile = get_object_or_404(UserProfile, user=request.user)


    # Construct the user's forms
    user_form = UserInfoForm(instance=profile.user)
    profile_form = UserProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        #'orders': orders,
    }

    return render(request, 'profiles/profile.html', context)