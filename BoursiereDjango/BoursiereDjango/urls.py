"""BoursiereDjango URL Configuration

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
from django.urls import path
from Beer import views as BeerViews
from AJAXModule import views as AJAXModuleViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('beer_ordering/', BeerViews.beer_ordering_view, name='beer_ordering'),
    path('add_beer/', BeerViews.add_beer, name='add_beer'),
    path('', BeerViews.root),
    path('login/', BeerViews.login_page, name='login_page'),
    path('logout/', BeerViews.logout_page, name='logout_page'),
    path('calculate_price/', AJAXModuleViews.calculate_price, name='calculate_price'),
    path('make_order/', AJAXModuleViews.make_order, name='make_order'),
    path('delete_histo/', AJAXModuleViews.delete_histo, name='delete_histo'),
    path('update_price/', AJAXModuleViews.update_price, name='update_price'),
    path('stock_page/', BeerViews.stock_page, name='stock_page'),
]
