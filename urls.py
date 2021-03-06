"""genealogie URL Configuration

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
import tree.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('timeline/<int:person_id>/<int:distance>', tree.views.tree, kwargs={'chart_type': 'timeline'}),
    path('descendants/<int:person_id>/<int:distance>', tree.views.tree, kwargs={'chart_type': 'descendants'}),
    path('ancestors/<int:person_id>/<int:distance>', tree.views.tree, kwargs={'chart_type': 'ancestors'}),
    path('get_json/', tree.views.get_json),
    path('get_json/<int:person_id>/<int:distance>', tree.views.get_partial),
    path('get_descendants/<int:person_id>/<int:distance>', tree.views.get_descendants),
    path('get_ancestors/<int:person_id>/<int:distance>', tree.views.get_ancestors),
    path('simpsons/', tree.views.simpsons),
]
