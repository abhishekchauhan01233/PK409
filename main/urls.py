from django.urls import path
from . import views
from SIH import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.home, name='homepage'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('accounts/login/', views.login, name='login'),
    path('contact/', views.contact, name='contact'),
    path('farmer/', views.farmer, name='farmer'),
    path('claim/', views.claim, name='claim'),
    path('profile/', views.profile, name='profile'),
    path('feedback/', views.feedback, name='feedback'),
    path('scientist/', views.scientist, name='scientist'),
    path('thanks/', views.thanks, name='thanks'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)