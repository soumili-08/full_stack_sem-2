from django.shortcuts import render, redirect
from .models import Playlist, PlaylistSong
 # Assuming you will create a form for the playlist
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from .models import UserFav, Song,Karaoke
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.utils import timezone



# Create your views here.
def index(request):
    song=Song.objects.all()
    user_favorites = UserFav.objects.filter(user=request.user) if request.user.is_authenticated else []
    return render(request,'user/index.html',{'song':song,'UserFav': user_favorites})

def mood_page(request):
    #moods = get_mood_data()
    return render(request, 'user/mood.html',{'moods': mood_page})

def mood_songs(request, mood_type):
    # Use __iexact for case-insensitive matching
    songs = Song.objects.filter(mood__iexact=mood_type)
    return render(request, 'user/mood_songs.html', {'songs': songs, 'mood': mood_type})


def songs(request):
    song=Song.objects.all()
    fav_songs = Song.objects.filter(id__in=UserFav.objects.filter(user=request.user).values_list('song_id', flat=True))
    return render(request,'user/songs.html',{'song':song,'fav_songs':fav_songs})

def songpost(request,id):
    song = Song.objects.filter(id=id).first()
    return render(request,'user/songpost.html',{'song':song})


def delete_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    song.delete()  # Deletes the song from the database
    return redirect('admin_dashboard')


def register_user(request):
    if request.method == 'POST':
        username= request.POST.get('username')
        password = request.POST.get('password')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        user = User.objects.create(username=username,email=username,first_name=firstname,last_name=lastname)
        user.set_password(password)
        user.save()
        return redirect('login')
    else:
        return render(request,'user/register.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        authenticated_user = authenticate(request,username=username,password=password)
        print(authenticated_user)
        if authenticated_user is not None:
            login(request,authenticated_user)
            return redirect('home')
    return render(request,'user/login.html')


def add_to_fav(request, id):
    song = get_object_or_404(Song, id=id)
    user = request.user

    if not UserFav.objects.filter(user=user, song=song).exists():
        UserFav.objects.create(user=user, song=song)
        print(f"Added song {song.name} to favorites for user {user.username}.")
    else:
        print(f"Song {song.name} already in favorites for user {user.username}.")

    return redirect('fav_songs')  # Redirect to the favorite songs page after adding


# Display the user's favorite songs
from django.shortcuts import render
from .models import UserFav  # Assuming your model is named UserFav

def fav_songs(request):
    user_favorites = UserFav.objects.filter(user=request.user)  # Fetch user's favorites
    print(user_favorites)
    context = {
        'UserFav': user_favorites
    }
    print(context)
    return render(request, 'user/fav_songs.html', context)


def songs(request):
    all_songs = Song.objects.all()
    fav_ids = UserFav.objects.filter(user=request.user).values_list('song_id', flat=True) if request.user.is_authenticated else []
    return render(request, 'user/songs.html', {'song': all_songs, 'fav_ids': fav_ids})


def logout_user(request):
    # Log out the user
    logout(request)
    # Redirect to the home page or any other page after logging out
    return redirect('home')


def singer_list(request):
    singers = Song.objects.values_list('singer', flat=True).distinct()
    return render(request, 'user/singers.html', {'singers': singers})


def search_songs(request):
    query = request.GET.get('q', '')  # Get the search query from the request
    results = Song.objects.filter(name__icontains=query) if query else Song.objects.all()
    return render(request, 'user/search_results.html', {'query': query, 'results': results})


def upload_song(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        singer = request.POST.get('singer')
        tags = request.POST.get('tags')
        movie = request.POST.get('movie')
        image = request.FILES.get('image')  # Handling image file
        song_file = request.FILES.get('song')  # Handling song file
        mood=request.POST.get('mood')

        # Create and save the new song
        new_song = Song(
            name=name,
            singer=singer,
            mood=mood,
            movie=movie,
            image=image,
            song=song_file
        )
        new_song.save()

        return redirect('songs')  # Redirect to the songs page to see the uploaded song

    return render(request, 'user/upload_song.html')  # Assuming you create this template



def upload_karaoke(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        lyrics = request.POST.get('lyrics')
        background_song = request.FILES.get('background_song')
        image = request.FILES.get('image')

        new_karaoke = Karaoke(
            name=name,
            lyrics=lyrics,
            background_song=background_song,
            image=image
        )
        new_karaoke.save()

        return redirect('karaoke_list')

    return render(request, 'user/upload_karaoke.html')


def karaoke_list(request):
    karaoke_songs = Karaoke.objects.all()
    return render(request, 'user/karaoke_list.html', {'karaoke_songs': karaoke_songs})


def karaoke_play(request, karaoke_id):
    karaoke = get_object_or_404(Karaoke, id=karaoke_id)
    return render(request, 'user/karaoke_play.html', {'karaoke': karaoke})


def edit_karaoke(request, karaoke_id):
    karaoke = get_object_or_404(Karaoke, id=karaoke_id)
    if request.method == 'POST':
        karaoke.name = request.POST['name']
        karaoke.lyrics = request.POST['lyrics']
        if 'background_song' in request.FILES:
            karaoke.background_song = request.FILES['background_song']
        if 'image' in request.FILES:
            karaoke.image = request.FILES['image']
        karaoke.save()
        return redirect('karaoke_list')
    return render(request, 'user/edit_karaoke.html', {'karaoke': karaoke})


def delete_karaoke(request, karaoke_id):
    karaoke = get_object_or_404(Karaoke, id=karaoke_id)
    karaoke.delete()
    return redirect('karaoke_list')


def admin_dashboard(request):
    # Get the logged-in user
    user = request.user
    
    # Get all active users
    active_users = User.objects.filter(is_active=True)  # Get all active users
    
    all_songs = Song.objects.all()

    context = {
        'user': request.user,
        'active_users': active_users,
        'all_songs': all_songs,  # Include all songs in the context
    }
    return render(request, 'user/admin_dashboard.html', context)


def edit_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)

    if request.method == 'POST':
        song.name = request.POST.get('name')
        song.singer = request.POST.get('singer')
        if 'image' in request.FILES:
            song.image = request.FILES['image']
        if 'song' in request.FILES:
            song.song = request.FILES['song']
        song.save()
        return redirect('admin_dashboard')

    return render(request, 'user/edit_song.html', {'song': song})
