from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    TemplateView,
    CreateView,
    FormView,
)
from django.utils import timezone
from django.contrib import messages
from .forms import *
from product.models import SpecialOffer, Products


class HomeView(TemplateView):
    template_name = 'root/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected_products"] = Products.objects.all().order_by(
            "-total_favorites"
        )[:4]
        context["discounted_products"] = Products.objects.filter(
            discount_price__gt=0
        ).order_by("-discount_price")[:100]
        context["popular_products"] = Products.objects.all().order_by(
            "-total_views"
        )[:4]
        context["best_selling_products"] = Products.objects.all().order_by(
            "-total_sold"
        )[:12]
        special_offers = SpecialOffer.objects.filter(
            start_date__lte=timezone.now(), end_date__gte=timezone.now()
        ).order_by("-product__discount_price")
        special_offers_list = list(special_offers)
        for l in special_offers_list:
            l.remaining = l.remaining_time()
        context["special_offers"] = special_offers_list
        # context['blogs'] = Blog.objects.filter(status=True).order_by(
            # '-created_at'
        # )[:3]
        context["special_offers"] = special_offers
        return context


class ContactUsView(CreateView):
    model = ContactUs
    fields = ['fullname', 'email', 'phone', 'subject', 'message']
    template_name = 'root/contact.html'
    success_url = '/contactus/'

    def form_valid(self, form):
        messages.success(
            self.request,
            'پیام شما با موفقیت دریافت شد . بزودی با شما تماس خواهیم گرفت',
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, 'خطا در ارسال اطلاعات . لطفا دوباره تلاش کنید'
        )
        return super().form_invalid(form)


class AboutUsView(TemplateView):
    template_name = 'root/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team'] = Team.objects.all()
        return context


class FaqView(TemplateView):
    template_name = 'root/faq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faqs'] = Faq.objects.filter(status=True)
        return context
