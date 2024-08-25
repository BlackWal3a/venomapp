from django.urls import path
from . import views

urlpatterns = [
    path('', views.landingpage_view, name='landingpage'),
    path('overview/', views.overview, name='overview'),
    path('cartographie/', views.cartographie, name='cartographie'),
    path('especes/', views.especes, name='especes'),
    path('medecin/', views.medecin, name='medecin'),
    path('urgence/', views.urgence, name='urgence'),
    path('geography/', views.geo_view, name='geography'),
    path('timeline/',views.time_view, name='timeline'),
    path('aircrafts/', views.aircrafts_view, name='aircrafts'),
    path('sign-in/', views.signin_view, name='sign-in'),
    path('change-password/', views.change_password, name='change_password'),
    path('rtl/', views.prevision_view, name='rtl'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('forecasting/', views.forecasting_view, name='forecasting'),
    path('country_details/', views.country_details, name='country_details'),
    path('about/', views.about_view, name='about'),
    path('submit-rate-and-notes/', views.submit_rate_and_notes, name='submit_rate_and_notes'),
    path('signup/', views.signup, name='signup'),
    path('loginn/', views.loginn, name='loginn'),
    path('report_bite_api/', views.report_bite_api, name='report_bite_api'),


]
