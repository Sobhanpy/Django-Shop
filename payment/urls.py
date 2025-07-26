from django.urls import path
from payment.views import *

app_name = 'payment'

urlpatterns = [
    path('', PaymentView.as_view(), name='payment'),
    path('factor-view/', FactorView.as_view(), name='factor-view'),
    path('factors/', FactorsView.as_view(), name='factors'),
    path('verify/', VerifyView.as_view(), name='verify'),
    path(
        'verify/payment-accept/', PaymentAcceptView.as_view(), name='accept'
    ),
]
