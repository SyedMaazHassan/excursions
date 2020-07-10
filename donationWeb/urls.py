from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login, name="login"),
    path('signup', views.signup, name="signup"),
    path('logout', views.logout, name="logout"),
    path('members', views.index, name="members"),
    path('profile', views.profile, name="profile"),
    path('excursions', views.all_excursions, name="excursions"),
    path('excursion/<int:id>', views.particular_ex, name="excursion"),
    path('authentication', views.authentication, name='authentication'),

]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
