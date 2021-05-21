from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Q
from datetime import date, datetime

from .serializers import (OrderSerializer, OrderLineSerializer, OrderEventSerializer,
                          InvoiceSerializers, GiftCardSerializers, VoucherSerializers,
                          SaleSerializers, CouponInputSerializers)
from .models import (Order, OrderLine, OrderEvent, Invoice, GiftCard, Voucher, Sale)
from accounts.models import Address
from payment.models import Payment, Transaction
from .permissions import IsAdminOrReadOnly
from . import checksum
from django.conf import settings
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin, IsOwnerReadOnlyOrAdmin


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsOwnerReadOnlyOrAdmin]

    def get_queryset(self):
        orders = Order.objects.all()
        if not self.request.user.is_superuser:
            orders = orders.filter(user = self.request.user)
        return orders

    @action(detail=True, methods=['get'])
    def invoice(self, request, pk=None):
        order = self.get_object()
        order.total_net_price = order.shipping_price + order.undiscounted_total_net_amount
        pass

    @action(detail=True, methods = ['post'])
    def coupon(self,request, pk=None):
        permission_classes = [IsAuthenticated]
        serializer = CouponInputSerializers(data = request.data)
        if serializer.is_valid():
            category = serializer.validated_data['category']
            if category=='giftcard':
                giftcard = get_object_or_404(GiftCard, code=serializer.validated_data['code'])
                if(giftcard.isactive):
                    giftcard.last_used_on = date.today()
                    order = self.get_object()
                    discount = 0
                    if giftcard.current_balance_amount > order.total_net_amount :
                        discount = order.total_net_amount
                        giftcard.current_balance_amount = giftcard.current_balance_amount - discount
                    else:
                        discount = giftcard.current_balance_amount
                        giftcard.current_balance_amount = 0
                        giftcard.is_active = False
                    order.total_net_amount = order.total_net_amount - discount
                    return order
                else:
                    return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
            else:
                voucher = get_object_or_404(Voucher, code=serializer.validated_data['code'])
                order = self.get_object()
                order.voucher = voucher
                voucher.used = voucher.user + 1
                if voucher.apply_once_per_customer == True:
                    pass
                if voucher.type == "shipping":
                    order.shipping_price = order.shipping_price - (order.shipping_price*(voucher.value/100))
                elif voucher.type == "entire_order":
                    order.total_net_amount = order.total_net_amount - (order.total_net_amount*(voucher.value/100))
                return order


    @action(detail=True, methods = ['post'])
    def payment(self, request, pk=None):
        order = self.get_object()
        user = get_object_or_404(Address, user=self.request.user)
        amount = order.total_net_amount
        name = user.full_name
        email = user.user.email

        # object of payment.transaction and payment.Payment is to be created

        # we have to send the param_dict to the frontend
        # these credentials will be passed to paytm order processor to verify the business account
        param_dict = {
            'MID': settings.PAYTM_MERCHANT_ID,
            'ORDER_ID': str(order.id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': settings.PAYTM_INDUSTRY_TYPE_ID,
            'WEBSITE': settings.PAYTM_WEBSITE,
            'CHANNEL_ID': settings.PAYTM_CHANNEL_ID,
            # 'CALLBACK_URL': '',
            # this is the url of handlepayment function, paytm will send a POST request to the fuction associated with this CALLBACK_URL
        }


        # create new checksum (unique hashed string) using our merchant key with every paytm payment
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, settings.PAYTM_MERCHANT_ID)
        # send the dictionary with all the credentials to the frontend
        return Response({'param_dict': param_dict})


    @action(detail=True, methods = ['post'])
    def handle_payment(self, request, pk=None):
            checksum = ""

            # the request.POST is coming from paytm
            form = request.POST

            response_dict = {}
            order = None  # initialize the order varible with None

            for i in form.keys():
                response_dict[i] = form[i]
                if i == 'CHECKSUMHASH':
                    # 'CHECKSUMHASH' is coming from paytm and we will assign it to checksum variable to verify our paymant
                    checksum = form[i]

                if i == 'ORDERID':
                    # we will get an order with id==ORDERID to turn isPaid=True when payment is successful
                    order = Order.objects.get(id=form[i])

            # we will verify the payment using our merchant key and the checksum that we are getting from Paytm request.POST
            verify = Checksum.verify_checksum(response_dict, settings.PAYTM_MERCHANT_ID, checksum)

            if verify:
                if response_dict['RESPCODE'] == '01':
                    # if the response code is 01 that means our transaction is successfull
                    print('order successful')
                    # after successfull payment we will make isPaid=True and will save the order
                    order.isPaid = True
                    order.save()
                    # we will render a template to display the payment status
                    return render(request, 'paytm/paymentstatus.html', {'response': response_dict})
                else:
                    print('order was not successful because' + response_dict['RESPMSG'])
                    return render(request, 'paytm/paymentstatus.html', {'response': response_dict})




    @action(detail=True, methods = ['post'])
    def return_request(self, request, pk=None):
        pass

    @action(detail=True, methods=['post'])
    def payment_status(self, request, pk=None):
        pass

    @action(detail=False, methods=['get'], permission_classes=[IsOwnerReadOnlyOrAdmin])
    def cart(self, request):
        cart = Order.objects.filter(user=self.request.user, status='draft')
        if cart.exists():
            cart = cart[0]
        else:
            cart = Order.objects.create(user=self.request.user, status="draft")
        serializer = OrderSerializer(cart, many=False)
        return serializer.data


class OrderEventViewSet(viewsets.ModelViewSet):
    serializer_class = OrderEventSerializer
    permission_classes = [IsOwnerReadOnlyOrAdmin]
    queryset = OrderEvent.objects.all()


class GiftCardViewset(viewsets.ModelViewSet):
    serializer_class = GiftCardSerializers
    permission_classes = [IsAdminOrReadOnly]
    queryset = GiftCard.objects.all()

class VoucherViewset(viewsets.ModelViewSet):
    serializer_class = VoucherSerializers
    permission_classes = [IsAdminOrReadOnly]
    queryset = Voucher.objects.all()

class SaleViewset(viewsets.ModelViewSet):
    serializer_class = SaleSerializers
    permission_class = [IsAdminOrReadOnly]
    queryset = Sale.objects.all()
