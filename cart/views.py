from django.shortcuts import redirect, get_object_or_404
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

class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'carts/cart.html'

    def get(self, request, *args, **kwargs):
        cart = request.session.get('cart', {})
        if len(cart) > 0:
            total_price = sum(
                [
                    item['price'] * int(item['quantity'])
                    for item in cart.values()
                ]
            )
            total_discount = sum(
                [
                    int(
                        item['product_discount_price'] * int(item['quantity'])
                    )
                    for item in cart.values()
                ]
            )
            total_discount_price = total_price - total_discount
            request.session['total_price'] = total_price
            request.session['total_discount_price'] = total_discount_price
            request.session['payment_price'] = (
                request.session['total_price']
                - request.session['total_discount_price']
            )
            request.session.modified = True
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', {})
        product_list = []
        for key, value in cart.items():
            product = get_object_or_404(Products, id=value['pid'])
            product_list.append(product)
        category_list = [product.category.name for product in product_list]
        products = Products.objects.filter(category__name__in=category_list)
        context['products'] = products
        return context


class AddToCartView(TemplateView):
    def get(self, request, *args, **kwargs):
        pid = request.GET.get('pid')
        g_mount = request.GET.get('g_mount')
        color = (
            request.GET.get("color")
            if request.GET.get("color") != ''
            else 'تک رنگ'
        )
        if not pid:
            messages.error(request, 'محصول نامعتبر است.')
            return redirect("product:products")

        # get product info
        product = get_object_or_404(Products, id=pid)

        # get guarantee info
        guarantee = (
            get_object_or_404(Guarantee, mounts=g_mount)
            if g_mount != '0'
            else 0
        )

        # Calciulate price depend on disscount
        increase_price_with_guarantee = (
            (product.price * guarantee.price_increase / 100)
            if guarantee != 0
            else 0
        )
        price_with_discount = product.get_discounted_price()
        product_price = int(increase_price_with_guarantee) + int(
            price_with_discount
        )
        cart = request.session.get('cart', {})
        found = False
        for key, item in cart.items():
            if type(item) == dict and item.get('pid'):
                if (
                    item['pid'] == int(pid)
                    and item['color'] == color
                    and item['guarantee'] == g_mount
                ):
                    cart[key]['quantity'] += 1
                    cart[key]['final_price'] = (
                        cart[key]['quantity'] * product_price
                    )
                    found = True
                    break

        if not found:
            unique_id = str(uuid.uuid4())[:8]
            cart[unique_id] = {
                'pid': product.id,
                'title': product.name, 
                'image': product.image.url if product.image else None,
                'price': product.price,
                'final_price': product_price,
                'quantity': 1,
                'guarantee': g_mount,
                'color': color,
                'product_discount': int(product.discount_price),
                'product_discount_price': int(price_with_discount),
            }

        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, 'محصول به سبد خرید شما اضافه شد')
        return redirect("product:product-detail", pk=pid)


class UpdateCartView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        messages.error(request, 'درخواست نا مناسب')
        return redirect("cart:cart")

    def post(self, request, *args, **kwargs):
        cart = request.session.get('cart', {})

        for uid_post, quantity_post in request.POST.items():
            for uuid in cart.keys():
                if uid_post == uuid:
                    cart[uuid]['quantity'] = quantity_post
                    product = get_object_or_404(
                        Products, id=cart[uuid]['pid']
                    )
                    guarantee = (
                        get_object_or_404(
                            Guarantee, mounts=cart[uuid]['guarantee']
                        )
                        if cart[uuid]['guarantee'] != '0'
                        else 0
                    )
                    increase_price_with_guarantee = (
                        (product.price * guarantee.price_increase / 100)
                        if guarantee != 0
                        else 0
                    )
                    price_with_discount = product.get_discounted_price()
                    product_price = increase_price_with_guarantee + int(
                        price_with_discount
                    )
                    cart[uuid]['final_price'] = (
                        int(cart[uuid]['quantity']) * product_price
                    )
                    break
        request.session['cart'] = cart
        total_price = sum(
            [item['price'] * int(item['quantity']) for item in cart.values()]
        )
        total_discount = sum(
            [
                int(item['product_discount_price'] * int(item['quantity']))
                for item in cart.values()
            ]
        )
        total_discount_price = total_price - total_discount
        request.session['total_price'] = total_price
        request.session['total_discount_price'] = total_discount_price
        request.session['payment_price'] = (
            request.session['total_price']
            - request.session['total_discount_price']
        )
        request.session.modified = True
        messages.success(request, 'سبد خرید شما با موفقیت بروزرسانی شد')
        return redirect("cart:cart")


class DeleteCartItemView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        uid = kwargs.get('uid')
        cart = request.session.get('cart', {})
        if uid in cart:
            del cart[uid]
            request.session['cart'] = cart
            request.session.modified = True
            if len(cart) == 0:
                request.session['total_price'] = 0
                request.session['total_discount_price'] = 0
                request.session['payment_price'] = 0
            messages.success(request, 'محصول از سبد خرید شما حذف شد')
        else:
            messages.error(request, 'محصول در سبد خرید شما وجود ندارد')
        return redirect("cart:cart")

    def post(self, request, *args, **kwargs):
        messages.error(request, 'درخواست نا مناسب')
        return redirect("cart:cart")


class CleanCartItemView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        request.session['cart'] = {}
        request.session['total_price'] = 0
        request.session['total_discount_price'] = 0
        request.session['payment_price'] = 0
        request.session.modified = True
        messages.success(request, 'سبد خرید شما خالی شد')
        return redirect("cart:cart")

    def post(self, request, *args, **kwargs):
        messages.error(request, 'درخواست نا مناسب')
        return redirect("cart:cart")


class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = "carts/checkout.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, user=self.request.user)
        try:
            address = UserAddress.objects.filter(profile=profile).order_by(
                '-created_at'
            )[0]
        except:
            address = None
        context['address'] = address
        return context
