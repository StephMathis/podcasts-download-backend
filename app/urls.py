"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from tastypie.api import Api

from .api.user_resource import UserResource
from .api.podcast_resource import PodcastResource
from .api.podcast_item_resource import PodcastItemResource

v1_api = Api(api_name='v1')
v1_api.register(PodcastResource())
v1_api.register(PodcastItemResource())
v1_api.register(UserResource())

urlpatterns = [
    # The normal jazz here...
    url(r'^api/', include(v1_api.urls)),
]
