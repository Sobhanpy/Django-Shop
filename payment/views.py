from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    TemplateView,
    CreateView,
    FormView,
    ListView,
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from product.models import *
import uuid
from accounts.models import Profile, UserAddress
from cart.models import Cart, OrderItems, Status
from config import settings
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()


if settings.SAND_BOX:
    ZARINPAL_REQUEST = (
        'https://sandbox.zarinpal.com/pg/v4/payment/request.json'
    )
    ZARINPAL_STARTPAY = 'https://sandbox.zarinpal.com/pg/StartPay/'
    ZARINPAL_VERIFY = 'https://sandbox.zarinpal.com/pg/v4/payment/verify.json'
    MERCHANT_ID = "1344b5d4-0048-11e8-94db-005056a205be"
    CALLBACK_URL = "http://127.0.0.1:8000/payment/verify/"

else:
    ZARINPAL_REQUEST = 'https://api.zarinpal.com/pg/v4/payment/request.jsonn'
    ZARINPAL_STARTPAY = 'https://www.zarinpal.com/pg/StartPay/'
    ZARINPAL_VERIFY = 'https://api.zarinpal.com/pg/v4/payment/verify.json'
    MERCHANT_ID = os.environ.get('MERCHANT_ID')


class PaymentView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        cart = request.session.get('cart')
        status = Status.objects.get(id=1)
        profile = Profile.objects.get(user=request.user)
        if cart:
            cart_order = Cart.objects.create(
                profile=profile,
                status=status,
                total_price=request.session['total_price'],
                total_discount=request.session['total_discount_price'],
                total_payment=request.session['payment_price'],
            )

            request.session['cart_id'] = cart_order.id
            request.session.modified = True

            for detail in cart.values():
                OrderItems.objects.create(
                    cart=cart_order,
                    product=Products.objects.get(id=detail['pid']),
                    quantity=detail['quantity'],
                    color=detail['color'],
                    guarantee=detail['guarantee'],
                )
            data = {
                "merchant_id": MERCHANT_ID,
                "amount": request.session['payment_price'],
                "callback_url": CALLBACK_URL,
                "description": "افزایش اعتبار کاربر شماره ۱۱۳۴۶۲۹",
            }
            response = requests.post(ZARINPAL_REQUEST, data=data)
            response = response.json()
            data = response.get('data')
            if data:
                if data['code'] == 100 and data['message'] == 'Success':
                    # print (response.get('data')['authority'])
                    return redirect(ZARINPAL_STARTPAY + data['authority'])
                else:
                    messages.error(request, "خطا در اتصال به درگاه پرداخت")
                    return redirect("cart:checkout")
            else:
                messages.error(
                    request, "لطفا از خاموش بودن وی پی ان اطمینان حاصل کنید"
                )
                return redirect("cart:checkout")

        else:
            messages.error(request, 'سبد خریدی جهت ارجاع به درگاه موجود نیست')
            return redirect("product:products")


class FactorView(LoginRequiredMixin, TemplateView):
    template_name = 'payment/factor-view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.request.GET.get('pk')
        user = self.request.user
        profile = Profile.objects.get(user=user)
        if id:
            try:
                cart = Cart.objects.get(profile=profile, is_paid=True, id=id)
            except:
                cart = None
        else:
            try:
                cart = Cart.objects.filter(profile=profile, is_paid=True)[0]
            except:
                cart = None

        try:
            address = UserAddress.objects.filter(profile=profile).order_by(
                '-created_at'
            )[0]
        except:
            address = None
        context['cart'] = cart
        context['address'] = address
        return context


class FactorsView(LoginRequiredMixin, ListView):
    template_name = 'payment/factors.html'
    model = Cart
    context_object_name = 'carts'


class VerifyView(LoginRequiredMixin, TemplateView):
    template_name = 'payment/thankyou.html'

    def get(self, request, *args, **kwargs):
        status = request.GET['Status']
        authority = request.GET['Authority']
        if status == 'OK':
            data = {
                "merchant_id": MERCHANT_ID,
                "amount": request.session['payment_price'],
                "authority": authority,
            }
            response = requests.post(ZARINPAL_VERIFY, data=data)
            status = response.json()['data']
            cart_id = request.session.get('cart_id')
            if status['code'] == 100 or status['code'] == 101:
                cart_id = request.session.get('cart_id')
                cart = Cart.objects.get(id=cart_id)
                cart.is_paid = True
                cart.cart_hash = status['card_hash']
                cart.cart_pan = status['card_pan']
                cart.ref_id = status['ref_id']
                cart.save()
                url = f'payment-accept/?cart_id={cart_id}'
                request.session['cart'] = {}
                request.session['total_price'] = 0
                request.session['total_discount_price'] = 0
                request.session['payment_price'] = 0
                request.session['cart_id'] = 0
                request.session.modified = True
                return redirect(url)
            else:
                messages.error(request, f"{status['errors']}")
                return redirect("cart:checkout")
        else:
            messages.error(request, f"پرداخت ناموفق")
            return redirect("cart:checkout")


class PaymentAcceptView(LoginRequiredMixin, TemplateView):
    template_name = 'payment/thankyou.html'

    def get(self, request, *args, **kwargs):
        id = request.GET.get('cart_id', None)
        if id:
            user = request.user
            profile = Profile.objects.get(user=user)
            try:
                cart = Cart.objects.get(id=id, profile=profile)
                return render(
                    request, self.template_name, context={'cart': cart}
                )
            except:
                messages.error(request, f"درخواست نامعتبر")
                return redirect("cart:checkout")

        return super().get(request, *args, **kwargs)
