from django.urls import path
from accounts.views import *

app_name = 'accounts'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('logout/', LogOut.as_view(), name='logout'),
    path('view-profile/', ViewProfile.as_view(), name='view-profile'),
    path(
        'edit-profile/<int:pk>/', EditProfile.as_view(), name='edit-profile'
    ),
    path('profile/addresses/', SetAddressView.as_view(), name='addresses'),
    path('reset-password/', ResetPassword.as_view(), name='reset-password'),
    path(
        'reset-password-done/',
        ResetPasswordDone.as_view(),
        name='reset-password-done',
    ),
    path(
        'reset-password-confirm/<str:token>/',
        ResetPasswordConfirm.as_view(),
        name='reset-password-confirm',
    ),
    path(
        'reset-password-complete/',
        ResetPasswordComplete.as_view(),
        name='reset-password-complete',
    ),
    path('profile/addresses/get-cities/', get_cities, name='get_cities'),
    path(
        'change-password/', ChangePassword.as_view(), name='change-password'
    ),
    path('compare/', CompareView.as_view(), name='user-compare'),
    path('create-compare/', create_compare, name='user-create-compare'),
    path('remove-compare/', remove_compare, name='user-remove-compare'),
    path('favorites/', FavoritesView.as_view(), name='user-favorties'),
    path('create-favorite/', create_faviorites, name='user-create-favorites'),
    path(
        'remove-favorite/<int:pk>/',
        remove_favorites,
        name='user-remove-favorites',
    ),
]
