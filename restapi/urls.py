from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from restapi.views import user_view_set, Category_View_Set, GROUP_VIEW_SET, EXPENSES_VIEW_SET, index, logout, balance, \
    logProcessor


router = DefaultRouter()
router.register('users', user_view_set)
router.register('categories', Category_View_Set)
router.register('groups', GROUP_VIEW_SET)
router.register('expenses', EXPENSES_VIEW_SET)

urlpatterns = [
    path('', index, name='index'),
    path('auth/logout/', logout),
    path('auth/login/', views.obtain_auth_token),
    path('balances/', balance),
    path('process-logs/', logProcessor)
]

urlpatterns += router.urls
