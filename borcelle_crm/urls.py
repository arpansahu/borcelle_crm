"""borcelle_crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
import time
from django.urls import re_path

from send_email_app.views import (
    ScheduleMail,
    WebSocketSendMail,
)

from account.views import (
    CustomPasswordResetView,
    RegistrationView,
    LogoutView,
    LoginView,
    AccountView, activate,
)

from manager.views import (
    HomeView,
    search_phone, search_name, search_country_code, search_gst, search_email,
    ContactsCreateView, ContactsView, ContactDetailView, ContactsUpdateView, ContactsDeleteView
)

def trigger_error(request):
    division_by_zero = 1 / 0

def large_resource(request):
   time.sleep(4)
   return HttpResponse("Done!")

urlpatterns = [
    path('admin/', admin.site.urls),

    re_path(r'^celery-progress/', include('celery_progress.urls')),
    path('schedule_mail/', ScheduleMail.as_view(), name="schedule_mail"),
    path('web-socket-send-mail/', WebSocketSendMail.as_view(), name="web_socket_send_mail"),
    path('celery-progress/', include('celery_progress.urls')),

    path('', HomeView.as_view(), name='home'),
    path('contact/', ContactsView.as_view(), name='contact'),
    path('contact/add/', ContactsCreateView.as_view(), name='contact-create'),
    path('contact/<pk>/', ContactDetailView.as_view(), name='contact-detailed'),
    path('contact/<pk>/update', ContactsUpdateView.as_view(), name='contact-update'),
    path('contact/<pk>/delete', ContactsDeleteView.as_view(), name='contact-delete'),
    # autocomplete views
    path('search-user-email/', search_email, name='search-user-email'),
    path('search-user-gst/', search_gst, name='search-user-gst'),
    path('search-user-phone/', search_phone, name='search-user-phone'),
    path('search-user-name/', search_name, name='search-user-name'),
    path('search-country-code/', search_country_code, name='search-country-code'),

    path('register/', RegistrationView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('account/', AccountView.as_view(), name='account'),
    re_path(r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,40})/', 
            activate, name='account_activate'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
         name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
         name='password_change'),

    path('password_reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_change.html'),
         name='password_reset_confirm'),

    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
    # sentry test view 
    path('sentry-debug/', trigger_error),
    path('large_resource/', large_resource)
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'borcelle_crm.views.handler404'
handler500 = 'borcelle_crm.views.handler500'
handler403 = 'borcelle_crm.views.handler404'
handler400 = 'borcelle_crm.views.handler500'