from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import User

class UsersTestCase(APITestCase):

    def setUp(self):
        self.valid_payload = {
                              "first_name": "string",
                              "last_name": "string",
                              "email": "ss@ss.com",
                              "profile": {
                                 "role": "SUPER_ADMIN",
                                 "address": "109"
                              }
                            }

        self.invalid_payload = {
                              "first_name": "string",
                              "last_name": "string",
                              "email": "",
                              "profile": {
                                    "role": "SUPER_ADMINS",
                                    "address": "109"
                                }
                              }

        User.objects.create(username="sriraman", password="payoda@123")
        User.objects.create(username="jana", password="payoda@123")

    def test_get(self):
        """To get the User Count"""
        url = reverse('UserCreateList')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 2)

    def test_post(self):
        """Create Users"""
        url = reverse('UserCreateList')
        response = self.client.post(url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

        invalid_response = self.client.post(url, self.invalid_payload, format='json')
        self.assertEqual(invalid_response.status_code, status.HTTP_400_BAD_REQUEST)




# from typing import List, Optional
# import pytest
# from django.contrib.auth.models import User, Group, Permission
#
# @pytest.fixture
# def app_user_group(db) -> Group:
#     group = Group.objects.create(name="app_user")
#     change_user_permissions = Permission.objects.filter(
#         codename__in=["change_user", "view_user"],
#     )
#     group.permissions.add(*change_user_permissions)
#     return group
#
# @pytest.fixture
# def app_user_factory(db, app_user_group: Group):
#     # Closure
#     def create_app_user(
#         username: str,
#         password: Optional[str] = None,
#         first_name: Optional[str] = "first name",
#         last_name: Optional[str] = "last name",
#         email: Optional[str] = "foo@bar.com",
#         is_staff: str = False,
#         is_superuser: str = False,
#         is_active: str = True,
#         groups: List[Group] = [],
#     ) -> User:
#         user = User.objects.create_user(
#             username=username,
#             password=password,
#             first_name=first_name,
#             last_name=last_name,
#             email=email,
#             is_staff=is_staff,
#             is_superuser=is_superuser,
#             is_active=is_active,
#         )
#         user.groups.add(app_user_group)
#         # Add additional groups, if provided.
#         user.groups.add(*groups)
#         return user
#     return create_app_user
#
# @pytest.fixture
# def user_A(db, app_user_factory) -> User:
#     return app_user_factory("A")
#
# @pytest.fixture
# def user_B(db, app_user_factory) -> User:
#     return app_user_factory("B")
#
# def test_should_create_user_in_app_user_group(
#     user_A: User,
#     app_user_group: Group,
# ) -> None:
#     assert user_A.groups.filter(pk=app_user_group.pk).exists()
#
# def test_should_create_two_users(user_A: User, user_B: User) -> None:
#     assert user_A.pk != user_B.pk