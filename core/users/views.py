from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm
from django.http import HttpResponseForbidden


@login_required(login_url='login')
def profile_view(request):
    return render(request, 'ticket/profile.html')


@login_required
def edit_profile(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлён!")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'ticket/edit_profile.html', {'form': form})


