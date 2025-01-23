from django.urls import path
from .views import index, register_user, login_user, mood_page, songs, songpost, add_to_fav, fav_songs,logout_user,singer_list,search_songs,upload_song,upload_karaoke,karaoke_list,karaoke_play,edit_karaoke,delete_karaoke,delete_song,mood_songs,admin_dashboard,edit_song

urlpatterns = [
    path('', index, name="home"),
    path('songs', songs, name='songs'),
    path('songs/<int:id>', songpost, name='songpost'),
    path('delete_song/<int:song_id>/', delete_song, name='delete_song'),
    path('mood', mood_page, name="mood_page"),
    path('mood/<str:mood_type>/', mood_songs, name="mood_songs"),
    path('register', register_user, name="register"),
    path('login', login_user, name='login'),
    path('add_fav_songs/<int:id>/', add_to_fav, name='add_to_fav'),
    path('fav_songs/', fav_songs, name='fav_songs'),
    path('logout/', logout_user, name='logout'),
    path('singers/', singer_list, name='singers'), 
    path('search/', search_songs, name='search_songs'),
    path('upload/', upload_song, name='upload_song'),
    path('karaoke/upload/', upload_karaoke, name='upload_karaoke'),
    path('karaoke/', karaoke_list, name='karaoke_list'),
    path('karaoke/play/<int:karaoke_id>/', karaoke_play, name='karaoke_play'),
    path('karaoke/edit/<int:karaoke_id>/', edit_karaoke, name='edit_karaoke'),
    path('karaoke/delete/<int:karaoke_id>/', delete_karaoke, name='delete_karaoke'),
    path('admin-dashboard/',admin_dashboard, name='admin_dashboard'),
    path('edit_song/<int:song_id>/', edit_song, name='edit_song'),
    
]
