from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Category, Service, Feedback, Item
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import FeedbackForm
from django.contrib.auth.models import User
from booking.models import Booking
from booking.forms import BookingForm
# Create your views here.

def service_about(request):
    return render(request, 'account/about.html')

def service_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    services = Service.objects.all()
    if request.method=='POST':
        feed_form = FeedbackForm(request.POST)
        if feed_form.is_valid():
            cd = feed_form.cleaned_data
            username = request.user.username
            user = User.objects.get(username=username)
            Feedback.objects.create(name=user, text=cd['text'])
    else:
        feed_form = FeedbackForm()



    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        services = services.filter(category=category)
    paginator = Paginator(services, 6)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request,
            'shop/product/list.html',{'category':category,'categories':categories, 'services':services, 'page':page,
                'feed_form':feed_form })


def category_list(request, category_slug):
    services = Service.objects.all()
    category = get_object_or_404(Category, slug=category_slug)
    services = services.filter(category=category)
    bookings = Booking.objects.all()
    username = request.user.username
    user = User.objects.get(username = username)
    booked_services = bookings.filter(name=user)

    return render(request, 'shop/product/services.html', {'category':category, 'services':services, 'booked_services':booked_services})

def service_detail(request, id, slug):
    item = Item.objects.all()
    service = get_object_or_404(Service, id=id, slug=slug)
    items = item.filter(category=service)
    if request.method == 'POST':
        form =BookingForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = request.user.username
            service = cd['service']
            item =cd['item']
            item_picked = Item.objects.get(name=item)
            service_picked = Service.objects.get(name=service)
            user = User.objects.get(username=username)
            Booking.objects.create(name=user, service=service_picked, item=item_picked, description=cd['description'], telephone=cd['telephone'], email=cd['email'], location=cd['location'], )
    else:
        form = BookingForm()


    return render(request, 'shop/product/detail.html', {'service': service, 'form':form, 'items':items})

