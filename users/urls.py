from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='default'),
    path('register/', register_view, name='register_view'),
    path('home/', home, name='home_view'),
    
    path('send-test-email',send_test_email, name="send_test_email"),

    path('refresh-generation-view-file',refresh_generation_view_file, name="refresh_generation_view_file"),
   
    path('generation-view-file/', generation_view_file, name='generation_view_file'),
    path('generation_view/', generation_view, name='generation_view'),
    path('generateBachelor/', generateBachelor, name='generateBachelor'),

    path('generateFullVersion/',genFullVersion, name='genFullVersion'),

    path('bachelors_store/', bachelors_store, name='bachelors_store'),
    path('download_full/', download_full, name='download_full'),
    path('download_MVP/', download_MVP, name='download_MVP'),

    path('dashboard/', dashboard, name='dashboard_view'),
    path('user_board/', user_board, name='user_board'),
    path('loginview/', login_view, name='login_view'),
    path('loginauth/', login_auth, name='login_auth'),
    path('logout/', logout_auth, name='logout_auth'),

    # path('save/', save_data_to_database, name='save_data'),
    path('creators/', creators_view, name='creators_view'),
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
    path('terms-of-use/', terms_of_use_view, name='terms_of_use_view'),
    path('cooperation/', cooperation_view, name='cooperation_view'),
]
