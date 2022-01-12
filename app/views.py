from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from app.forms import NewImageForm, UpdateProfileForm
from .models import Comment, Image, Profile, Likes
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def loginPage(request):
    context = {

    }

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = Profile.objects.get(username = username)
        except:
            messages.error(request, 'user does not exist')

        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist')
        
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')


def registerUser(request):
    form = UserCreationForm()
    context = {
        'form':form
    }

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'An error occurred during registration')
   
    return render(request, 'registration.html', context)

@login_required(login_url='login')
def home(request):
    images = Image.objects.all()  

    context = {
        'images':images
    }

    return render(request, 'home.html', context)

@login_required(login_url='login')
def new_image(request):
    current_user = request.user
    image = Image.objects.filter(user=request.user).last()
    if request.method == 'POST':
        form = NewImageForm(request.POST, request.FILES, instance= image)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = current_user
            data.save()
        return redirect('home')
    else:
        form = NewImageForm()
        context = {
            'form':form
        }
        return render(request, 'new_image.html', context)

def image(request, id):
    try:
        image = Image.objects.get(id=id)
    except ObjectDoesNotExist:
        raise Http404()
    comments = image.comment_set.all()

    if request.method == 'POST':
        comment = Comment.objects.create (
            user = request.user,
            image = image,
            comment_content = request.POST.get('comment_content')
        )

        return redirect('home')
    context = {
        'image':image,
        'comments': comments
    }
    return render(request, 'image.html', context)

@login_required(login_url='login')
def search_results(request):
    if 'profile' in request.GET and request.GET['profile']:
        search_query = request.GET.get('profile')
        searched_profiles = Profile.search_profile(search_query)
        message = f'{search_query}'
        context = {
           'message':message,
           'searched_profiles':searched_profiles
        }

        return render (request, 'search.html', context)
    else:
        message = 'You havent searched for any profile'
        return render(request, 'search.html', {'message':message})


@login_required(login_url='login')
def like_image(request, id):
    likes = Likes.objects.filter(image_id=id).first()
    if Likes.objects.filter(image_id=id, user_id=request.user.id).exists():
        likes.delete()
        image = Image.objects.get(id=id)
        if image.total_likes == 0:
            image.total_likes = 0
            image.save()
        else:
            image.total_likes += 1
            image.save()
        return redirect('home')
    else:
        likes = Likes(image_id=id, user_id=request.user.id)
        likes.save()
        image = Image.objects.get(id = id)
        image.total_likes = image.total_likes +1
        image.save()
        return redirect('home')

@login_required(login_url='login')
def view_profile(request, id):
    try:
        profile = Profile.objects.get(id = id)
        context = {
            'profile': profile,                       
        }
        return render(request, 'profile.html', context)
    except:
        messages.warning(request, 'Sorry, but it seems the profile is not set up')
        return redirect('home')
  

@login_required(login_url='login')
def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        context = {
            'form': form
        }
        if form.is_valid():
            form.save()
            return redirect(reverse('view_profile', kwargs={"id": request.user.profile.id }))
        else:
            messages.warning(request, 'There was a problem updating your profile')
            return redirect('update_profile')
    else:
        form = UpdateProfileForm(instance=request.user.profile)
        return render(request, 'update_profile.html', {"form":form})



