from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import MobileShop, PickUP, OfferImages
from django.shortcuts import get_object_or_404
from .forms import SchedulePickUpForm
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator,  EmptyPage, PageNotAnInteger
from django.http import JsonResponse
# Create your views here.

def index(request):
    offers = OfferImages.objects.all()
    context = {
        'offers': offers
    }
    return render(request, 'fixlyft/index.html', context)

def shops(request):
    shops = MobileShop.objects.all()
    return render(request, 'fixlyft/shops.html', {'shops': shops})

def offers(request):
    offers = OfferImages.objects.all()
    context = {
        'offers': offers
    }
    return render(request, 'fixlyft/offers.html', context)

def support(request):
    return render(request, 'fixlyft/support.html')

def delivery(request):
    return render(request, 'fixlyft/delivery.html')


class SchedulePickup(CreateView):
    model = PickUP
    form_class = SchedulePickUpForm
    template_name = 'fixlyft/form.html'
    success_url = reverse_lazy('schedule')

    slug = None

    def get_object(self, slug):
        return MobileShop.objects.get(slug=self.slug)

    def get_initial(self):
        self.mobileshop = get_object_or_404(MobileShop, slug=self.kwargs.get('slug'))
        return {'mobileshop':self.mobileshop,}

    def form_valid(self, form):
        super().form_valid(form)
        return JsonResponse({
            'status': 'ok',
            'details': 'done'
        })

    def get(self, request, *args, **kwargs):
        return redirect('schedule')


class MobileShopSearch(ListView):
    model = MobileShop
    template_name = 'fixlyft/schedule-pickup.html'
    context_object_name = 'shops'

    def get_queryset(self):
        query = self.request.GET.get('search', '')
        if query:
            object_list = MobileShop.objects.filter(Q(pincode__icontains=query))

            paginator = Paginator(object_list, 2)  # Show 5 shops per page
            page = self.request.GET.get('page')
            try:
                object_list = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                object_list = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 999), deliver last page of results.
                object_list = paginator.page(paginator.num_pages)
        else:


            object_list = None
        return object_list