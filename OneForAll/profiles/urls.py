from django.urls import path
from .views import ProfileDetailsView, accept_request, decline_request, profile_view, remove_connection, requests_received_view,request_profiles_list_view,ProfileListView,send_requests

app_name = 'profiles'

urlpatterns = [
    path('', ProfileListView.as_view(), name = 'allprofiles'),
    path('myprofile/', profile_view, name = 'myprofile'),
    path('my_requests/', requests_received_view, name = 'myrequests'),
    path('<slug>/',ProfileDetailsView.as_view(), name = 'profile_details'),
    path('/to-invite/', request_profiles_list_view, name = 'invite_profiles'),
    path('/send_request/', send_requests, name = 'send_request'),
    path('/remove_connection/', remove_connection, name = 'remove_connection'),
    path('my_requests/accept_request/', accept_request, name = 'accept_request'),
    path('my_requests/decline_request/', decline_request, name = 'decline_request'),
]