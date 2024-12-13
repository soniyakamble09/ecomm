from django.urls import path

from ecomm import settings
from . import views
#from ecomm_app import views
from .views import SimpleView
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
    path('about', views.about),
    path('contact', views.contact),
    path('delete/<rid>', views.delete),
    path('addition/<x>/<y>', views.addition),
    path('myview', views.SimpleView.as_view()),
    path('hello', views.hello),
    path('', views.home),
    path('product/<pid>', views.product),
    path('register', views.register),
    path('login', views.user_login),
    path('logout',views.user_logout),
    path('catfilter/<cv>',views.catfilter),
    path('sort/<sv>',views.sort),
    path('range',views.range),
    path('addtocart/<pid>',views.addtocart),
    path('viewcart',views.viewcart),
    path('remove/<cid>',views.remove),
    path('updateqty/<cid>/<qv>',views.updateqty),
    path('placeorder',views.placeorder),
    path('removeorder/<oid>',views.removeorder),
    path('makepayment',views.makepayment),
    path('sendmail',views.sendusermail)
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)