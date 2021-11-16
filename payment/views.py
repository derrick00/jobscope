from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Category, Service, Feedback
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import FeedbackForm
from django.contrib.auth.models import User
from booking.models import Booking
from booking.forms import BookingForm
# Create your views here.

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
    service = get_object_or_404(Service, id=id, slug=slug)
    if request.method == 'POST':
        form =BookingForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = request.user.username
            service = cd['service']
            service_picked = Service.objects.get(name=service)
            user = User.objects.get(username=username)
            Booking.objects.create(name=user, service=service_picked, description=cd['description'], telephone=cd['telephone'], email=cd['email'], location=cd['location'], )
    else:
        form = BookingForm()


    return render(request, 'shop/product/detail.html', {'service': service, 'form':form})

def payment_process(request):
    #order_id = request.session.get('order_id')
    #order = get_object_or_404(Order, id=order_id)
    price = order.get_total_cost()

    if request.method == 'POST':
        nonce = request.POST.get('payment_method_nonce', None)
        #create and submit transaction
        result = gateway.transaction.sale({'amount':f'{price:.2f}',
            'payment_method_nonce': nonce,
            'options':{'submit_for_settlement':True}})
        if result.is_success:
            #mark the order as paid
            booking.paid = True
            #store the unique transaction id 
            booking.braintree_id = result.transaction.id
            booking.save()
            #launch asychronous task
            payment_completed.delay(booking.id)
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        #generate token
        client_token = gateway.client_token.generate()
        return render(request, 'payment/process.html', {'booking':booking,
            'client_token':client_token})



