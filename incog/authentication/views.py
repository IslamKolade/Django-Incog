from django.shortcuts import render, redirect, get_object_or_404
from authentication.forms import SignupForm, ChangePasswordForm, EditProfileForm, LoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, login, authenticate
from authentication.models import Profile, LoginAttempt
from django.utils.http import url_has_allowed_host_and_scheme
from django.template import loader
from django.http import HttpResponse
from urllib.parse import unquote
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
# Create your views here.
from django.contrib.auth import get_user_model

User = get_user_model()

def account_check(request):
    if request.method == 'POST':
        email_or_username = request.POST['email_or_username']
        try:
            user = User.objects.get(email=email_or_username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=email_or_username)
            except User.DoesNotExist:
                messages.info(request, 'Email or username provided is not registered.')
                return render(request, 'auth/account_check.html', {})
        email = user.email
        # Get the first and last parts of the email
        first_part, last_part = user.email.split('@')
        # Get the length of the first part
        first_part = '*' * len(first_part[:-4]) + first_part[-4:]
        messages.info(request, f"Your email is: {first_part}@{last_part}")
        messages.success(request, email)
        return redirect('password_reset')
    else:
        return render(request, 'auth/account_check.html')



def UserProfile(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)

	template = loader.get_template('profile.html')

	context = {
		'profile':profile,
	}

	return HttpResponse(template.render(context, request))


@sensitive_post_parameters()
@csrf_protect
@never_cache
def Login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # User is authenticated using the username and password
                login(request, user)
                next_url = request.GET.get("next")
                if next_url:
                    next_url = unquote(next_url)  # decode the next URL
                    allowed_hosts = ['incog.pythonanywhere.com']
                    if url_has_allowed_host_and_scheme(
                        url=next_url, allowed_hosts=allowed_hosts
                    ):
                        return redirect(next_url)
                    else:
                        messages.warning(request, "Invalid next URL")
                else:
                    messages.info(request, "Welcome back, " + user.username)
                    return redirect("home")
            else:
                # User is not authenticated using the username and password
                # Check if the username exists in the database
                try:
                    user = User.objects.get(username=username)
                    # Username exists in the database, check if the password is correct
                    if user.check_password(password):
                        # Password is correct, authenticate the user
                        user = authenticate(request, username=user.username, password=password)
                        login(request, user)
                        next_url = request.GET.get("next")
                        if next_url:
                            next_url = unquote(next_url)  # decode the next URL
                            allowed_hosts = ['incog.pythonanywhere.com']
                            if url_has_allowed_host_and_scheme(
                                url=next_url, allowed_hosts=allowed_hosts
                            ):
                                return redirect(next_url)
                            else:
                                messages.warning(request, "Invalid next URL")
                        else:
                            messages.info(request, "Welcome back, " + user.username)
                            return redirect("home")
                    else:
                        # Password is incorrect
                        messages.info(request, "Wrong Password. Please try again.")
                        LoginAttempt.objects.create(username=username)
                        return redirect('/user/login')
                except User.DoesNotExist:
                    # User does not exist in the database
                    # Check if the email exists in the database
                    try:
                        user = User.objects.get(email=username)
                        # Email exists in the database, check if the password is correct
                        if user.check_password(password):
                            # Password is correct, authenticate the user
                            user = authenticate(request, username=user.username, password=password)
                            login(request, user)
                            next_url = request.GET.get("next")
                            if next_url:
                                next_url = unquote(next_url)  # decode the next URL
                                allowed_hosts = ['incog.pythonanywhere.com']
                                if url_has_allowed_host_and_scheme(
                                    url=next_url, allowed_hosts=allowed_hosts
                                ):
                                    return redirect(next_url)
                                else:
                                    messages.warning(request, "Invalid next URL")
                            else:
                                messages.info(request, "Welcome back, " + user.username)
                                return redirect("home")
                        else:
                            # Password is incorrect
                            messages.info(request, "Wrong Password. Please try again.")
                            LoginAttempt.objects.create(username=username)
                            return redirect('/user/login')
                    except User.DoesNotExist:
                        # Email does not exist in the database
                        messages.info(request, "This email/username is not registered.")
                        LoginAttempt.objects.create(username=username)
                        return redirect('/user/login')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

def Signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            next_url = request.GET.get("next")
            if next_url:
                next_url = unquote(next_url)  # decode the next URL
                allowed_hosts = ['incog.pythonanywhere.com']
                if url_has_allowed_host_and_scheme(
                    url=next_url, allowed_hosts=allowed_hosts
                ):
                    return redirect(next_url)
                else:
                    messages.warning(request, "Invalid next URL")
            else:
                messages.info(request, "Welcome back, " + user.username)
                return redirect("home")
    else:
        form = SignupForm()

    context = {
        'form':form,
    }

    return render(request, 'signup.html', context)



@login_required
def PasswordChange(request):
	user = request.user
	if request.method == 'POST':
		form = ChangePasswordForm(request.POST)
		if form.is_valid():
			new_password = form.cleaned_data.get('new_password')
			user.set_password(new_password)
			user.save()
			update_session_auth_hash(request, user)
			return redirect('change_password_done')
	else:
		form = ChangePasswordForm(instance=user)

	context = {
		'form':form,
	}

	return render(request, 'change_password.html', context)

def PasswordChangeDone(request):
	return render(request, 'change_password_done.html')


@login_required
def EditProfile(request):
    user = request.user.id
    profile = Profile.objects.get(user__id=user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            if request.FILES.get('profile_picture') == None:
                profile_picture = profile.profile_picture
                profile.whatsapp_number = form.cleaned_data.get('whatsapp_number')
                profile.facebook_url = form.cleaned_data.get('facebook_url')
                profile.instagram_username = form.cleaned_data.get('instagram_username')
                profile.twitter_username = form.cleaned_data.get('twitter_username')
                profile.bio = form.cleaned_data.get('bio')
                profile.save()
                messages.info(request, 'Profile successfully updated.')
                return redirect('edit-profile')
            if request.FILES.get('profile_picture') is not None:
                profile.profile_picture = form.cleaned_data.get('profile_picture')
                profile.whatsapp_number = form.cleaned_data.get('whatsapp_number')
                profile.facebook_url = form.cleaned_data.get('facebook_url')
                profile.instagram_username = form.cleaned_data.get('instagram_username')
                profile.twitter_username = form.cleaned_data.get('twitter_username')
                profile.bio = form.cleaned_data.get('bio')
                profile.save()
                messages.info(request, 'Profile successfully updated.')
                return redirect('edit-profile')
    else:
        form = EditProfileForm()

    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'edit_profile.html', context)
