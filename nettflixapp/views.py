from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Movie, Show, UserList, Movielist
from django.contrib.auth.models import User,auth
from django.contrib import messages 
import random
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import re


# Create your views here.
@login_required(login_url='login')
def index(request):
    # Get all movies
    movies = Movie.objects.all()
    featured_movies=movies[len(movies)-1]
    
    # Get a random movie for the featured section
    featured_movie = None
    if movies.exists():
        featured_movie = random.choice(movies)
    
    context = {
        'movies': movies,
        'featured_movie': featured_movie,
    }
    return render(request, 'index.html', context)

@login_required(login_url='login')
def movie(request, pk):
    movie_uuid = pk
    movie_details = get_object_or_404(Movie, id=movie_uuid)
    
    context = {
        'movie_details': movie_details
    }
    return render(request, 'movie.html', context)
@login_required(login_url='login')
def my_list(request):
    movie_list = Movielist.objects.filter(user=request.user)
    user_movie_list = []

    for movie_item in movie_list:
        user_movie_list.append(movie_item.movie)

    context = {
        'movies': user_movie_list
    }
    return render(request, 'my_list.html', context)

@login_required(login_url='login')
def movies_by_genre(request, genre):
    movies = Movie.objects.filter(genre=genre)
    
    context = {
        'movies': movies,
        'genre': genre
    }
    return render(request, 'genre.html', context)


@login_required(login_url='login')
def search(request):
    if request.method == 'POST':  # Missing colon after if condition
        search_term = request.POST.get('search_term')
        movies = Movie.objects.filter(title__icontains=search_term)
        
        context = {
            'movies': movies,
            'search_term': search_term
        }
        return render(request, 'search.html', context)
    else:
        return redirect('/')

@login_required(login_url='login')
@require_POST
def add_to_list(request):
    """
    Add a movie to the user's list.
    Expects a POST request with either 'movie_id' or 'item_id' in the request body.
    """
    try:
        # Try to get movie_id first, then fall back to item_id
        movie_id = request.POST.get('movie_id') or request.POST.get('item_id')
        
        if not movie_id:
            return JsonResponse({
                'status': 'error',
                'message': 'Movie ID is required'
            }, status=400)
        
        try:
            # Convert movie_id to integer
            movie_id = int(movie_id)
            movie = Movie.objects.get(id=movie_id)
            
            # Try to create the list item
            movie_list, created = Movielist.objects.get_or_create(
                user=request.user,
                movie=movie
            )
            
            if created:
                return JsonResponse({
                    'status': 'success',
                    'message': 'Movie added successfully'
                })
            else:
                return JsonResponse({
                    'status': 'success',
                    'message': 'Movie already in list'
                })
                
        except (ValueError, TypeError):
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid movie ID'
            }, status=400)
        except Movie.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Movie not found'
            }, status=404)
        except Exception as e:
            print(f"Error adding movie to list: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': 'Server error occurred'
            }, status=500)
            
    except Exception as e:
        print(f"Error in add_to_list view: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'Server error occurred'
        }, status=500)




def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid username or password')
            return redirect('login')
            
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        # Debug information
        print(f"[DEBUG] Attempting signup with email: {email}, username: {username}")
        
        # First check if passwords match
        if password != password2:
            print("[DEBUG] Passwords do not match")
            messages.info(request, 'Passwords do not match')
            return redirect('signup')
        
        try:
            # Then check if email exists (case-insensitive)
            email_exists = User.objects.filter(email__iexact=email).exists()
            print(f"[DEBUG] Email exists in database: {email_exists}")
            
            if email_exists:
                print(f"[DEBUG] Email {email} is already registered")
                messages.info(request, f'Email {email} is already registered')
                return redirect('signup')
            
            # Then check if username exists
            username_exists = User.objects.filter(username=username).exists()
            print(f"[DEBUG] Username exists in database: {username_exists}")
            
            if username_exists:
                print(f"[DEBUG] Username {username} is already taken")
                messages.info(request, f'Username {username} is already taken')
                return redirect('signup')
            
            # If we get here, both email and username are available
            print("[DEBUG] Creating new user...")
            new_user = User.objects.create_user(username=username, email=email, password=password)
            new_user.save()
            print(f"[DEBUG] User created successfully: {new_user.username}, {new_user.email}, ID: {new_user.id}")
            
            # Log the user in
            print("[DEBUG] Attempting to log in new user...")
            user_login = auth.authenticate(username=username, password=password)
            if user_login is not None:
                auth.login(request, user_login)
                print(f"[DEBUG] User logged in successfully: {user_login.username}")
                return redirect('/')
            else:
                print("[DEBUG] Failed to authenticate new user")
                messages.info(request, 'Failed to log in after signup')
                return redirect('login')
                
        except Exception as e:
            print(f"[DEBUG] Error during signup: {str(e)}")
            messages.info(request, f'Error during signup: {str(e)}')
            return redirect('signup')
        
    return render(request, 'signup.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required
@require_POST
def remove_from_list(request):
    """
    Remove a movie from the user's list.
    Expects a POST request with 'movie_id' in the request body.
    """
    try:
        movie_id = request.POST.get('movie_id')
        
        if not movie_id:
            return JsonResponse({
                'status': 'error',
                'message': 'Movie ID is required'
            }, status=400)
        
        try:
            # Convert movie_id to integer
            movie_id = int(movie_id)
            movie = Movie.objects.get(id=movie_id)
            
            # Try to remove the list item
            try:
                movie_list = Movielist.objects.get(
                    user=request.user,
                    movie=movie
                )
                movie_list.delete()
                return JsonResponse({
                    'status': 'success',
                    'message': 'Movie removed successfully'
                })
            except Movielist.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Movie not in list'
                }, status=404)
                
        except (ValueError, TypeError):
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid movie ID'
            }, status=400)
        except Movie.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Movie not found'
            }, status=404)
        except Exception as e:
            print(f"Error removing movie from list: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': 'Server error occurred'
            }, status=500)
            
    except Exception as e:
        print(f"Error in remove_from_list view: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'Server error occurred'
        }, status=500)


