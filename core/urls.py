
from django.urls import path 
from .views import *

urlpatterns = [
    path('', login_page , name='login_page'),
    path('logout/',logout_user, name='logout'),
    path('signup/',signup , name='signup'), 
    path('dashboard/', dashboard , name='dashboard'),
    path('add_trans/', add_trans, name='add_transaction'),
    path('delete-transaction/<int:pk>/', delete_transaction, name='delete_transaction'),
    path('forgot-password/', forget_password, name='forget_password'),
    path('validate-login/', validate_login, name='validate_login'),
    path('check-email/', check_email_exists, name='check_email'),
    path('financial_reports/', financial_reports, name='financial_reports'),
    path('budgeting/', budgeting , name='budgeting'),
    path('budget/delete/<int:category_id>/', delete_budget, name='delete_budget'),
    path('resend-otp/', resend_otp, name='resend_otp'),


]


