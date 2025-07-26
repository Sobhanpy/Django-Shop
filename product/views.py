from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    TemplateView,
    CreateView,
    FormView,
    ListView,
    DetailView,
)
from product.models import *
from product.forms import *
from accounts.models import Profile, User
from django.contrib import messages
from django.db.models import Q
from product.forms import *


# Create your views here.
class ProductsView(ListView):
    model = Products
    template_name = 'product/products.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["last_products"] = self.model.objects.all().order_by(
            '-created_at'
        )[:3]
        context["product_count"] = self.model.objects.all().count()
        return context


class ProductsList(ListView):
    model = Products
    template_name = 'product/products-list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["last_products"] = self.model.objects.all().order_by(
            '-created_at'
        )[:3]
        context["product_count"] = self.model.objects.all().count()
        return context

    def get_queryset(self):
        if self.request.GET.get('search'):
            return Products.objects.filter(
                name__contains=self.request.GET.get('search')
            )
        categories = self.request.GET.getlist(
            'category'
        )
        category_detail = self.request.GET.get('detail-category')
        if categories:
            query = Q()
            for category in categories:
                query |= Q(category__id=category)
                query |= Q(
                    category__parent__id=category
                )  
                query |= Q(category__parent__parent__id=category)

            return Products.objects.filter(query)
        if category_detail:
            return Products.objects.filter(category__name=category_detail)

        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price and max_price:
            try:
                min_price = int(min_price)
                max_price = int(max_price)
                return Products.objects.filter(
                    price__gte=min_price, price__lte=max_price
                )
            except ValueError:
                pass  # در صورتی که مقدار نامعتبر باشد، فیلتر اعمال نشود
        guarantee = self.request.GET.get('guarantee')
        if guarantee == 'true':
            return Products.objects.filter(has_guarantee=True)

        return Products.objects.all()


class ProductDetailView(DetailView):
    template_name = 'product/product.html'
    model = Products
    context_object_name = "product"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.total_views += 1
        self.object.save()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object.category.name
        context["same_products"] = self.model.objects.filter(
            category__name=category
        ).order_by('created_at')[:50]
        return context


class ProductCommentView(CreateView):
    form_class = ProductCommentForm

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Products, pk=kwargs['pk'])
        return redirect(f'products/detail/{product.pk}')

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(self.request, 'ابتدا وارد شوید')
            return redirect('accounts:login')
        product = get_object_or_404(Products, pk=kwargs['pk'])
        user = request.user
        email = user.email
        profile = Profile.objects.get(user=user)
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.name = profile
            comment.email = email
            comment.save()
            messages.success(
                request,
                'کامنت شما دریافت شد . در صورت تایید مدیر سایت نمایش داده می شود',
            )
            return redirect('product:product-detail', pk=product.pk)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'خطا در ارسال کامنت')
        return super().form_invalid(form)


class ProductReplayView(CreateView):
    form_class = ProductReplayForm

    def get(self, request, *args, **kwargs):
        comment = get_object_or_404(ProductComment, pk=kwargs['pk'])
        product = comment.product
        return redirect(f'products/detail/{product.pk}')

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(self.request, 'ابتدا وارد شوید')
            return redirect('accounts:login')
        comment = get_object_or_404(ProductComment, pk=kwargs['pk'])
        user = request.user
        email = user.email
        profile = Profile.objects.get(user=user)
        form = self.get_form()
        if form.is_valid():
            replay = form.save(commit=False)
            replay.comment = comment
            replay.name = profile
            replay.email = email
            replay.save()
            messages.success(
                request,
                'پاسخ شما دریافت شد . در صورت تایید مدیر سایت نمایش داده می شود',
            )
            return redirect('product:product-detail', pk=comment.product.pk)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'خطا در ارسال پاسخ')
        return super().form_invalid(form)
