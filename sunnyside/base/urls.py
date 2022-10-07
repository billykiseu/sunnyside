from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.views.generic import View
from django.contrib import admin
from django.urls import include
from django.urls import re_path as url
# patterns
urlpatterns = [
    path('', views.explore.as_view(), name="explore"),
    path('explore', views.explore.as_view(), name="explore"),
    path('gsearch', views.globalsearch, name="gsearch"),
    path('music', views.musicfilter, name="music"),
    path('digitalart', views.digitalartfilter, name="digitalart"),
    path('code', views.codefilter, name="code"),
    path('login', views.loginUser.as_view(), name="login"),
    path('logout', views.logoutUser.as_view(), name="logout"),
    path('signup', views.signupUser.as_view(), name="signup"),
    path('recover/', views.recover.as_view(), name="recover"),
    path('recoverdone/', auth_views.PasswordResetDoneView.as_view(
        template_name="base/recoverdone.html"), name="recoverdone"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="base/reset.html"), name="password_reset_confirm"),
    path('recovercomplete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="base/recovercomplete.html"), name="password_reset_complete"),
    path('loginfail/', views.loginfail.as_view(), name="loginfail"),
    path('recoverfail/', views.recoverfail.as_view(), name="recoverfail"),
    path('search/', views.autocomplete, name="search"),
    path('explore/<str:name>', views.subfilter1, name="supercategory"),
    path('explore/<str:name>/<str:name2>', views.subfilter2, name="category"),
    path('explore/<str:name>/<str:name2>/<str:name3>',
         views.subfilter3, name="subcategory"),
    path('play', views.play.as_view(), name="play"),
    path('play/<str:name>', views.play.as_view(), name="play"),
    path('change-password/', views.ChangePasswordView.as_view(),
         name='change-password'),
    path('editprofile/', views.profile, name="editprofile"),
    path('analytics/', views.analytics, name="analytics"),

    # Errors
    path('loginfail/login', views.loginfail.as_view(), name="error"),

]
if settings.DEBUG:
    False
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
