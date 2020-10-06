from django.conf.urls import url,include,re_path
from rest_framework import routers
from .views import UserView, UserCreateList, Login


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

router = routers.DefaultRouter()
router.register(r'users', UserView)

urlpatterns = [
    # url('',include(router.urls)),
    url('login',Login.as_view(),name="user-login"),
    re_path(r'^genericUser$',UserCreateList.as_view(),name="UserCreateList"),
    re_path(r'^genericUser/(?P<id>[0-9]+)/$', UserCreateList.as_view(), name='Update'),
]