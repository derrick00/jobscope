from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from service.models import Category, Service, Feedback
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from booking.models import Booking
from booking.forms import BookingForm
from django.conf import settings
import braintree
# Create your views here.
#instantiate braintree payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)

def payment_process(request, id):
    booking = get_object_or_404(Booking, id=id)
    price = booking.item.price

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
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        #generate token
        client_token = gateway.client_token.generate()
        return render(request, 'payment/process.html', {'booking':booking,
            'client_token':client_token})

def payment_done(request):
    return render(request, 'payment/done.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')

