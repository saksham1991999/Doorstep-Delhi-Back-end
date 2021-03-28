from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from payment.models import Payment, Transaction
from payment.serializers import PaymentSerializer, TransactionSerializer


# Create your views here.
class TransactionViewset(viewsets.ModelViewSet):
    permission_classes = []
    serializer_class = TransactionSerializer

    def get_queryset(self):
        transactions = Transaction.objects.all()
        return transactions

    @action(detail=False, methods=["get"])
    def my_transactions(self, request):
        try:
            my_transactions = Transaction.objects.filter(payment__order__user=request.user)
            serializer = TransactionSerializer(my_transactions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("ERROR !!!", status= status.HTTP_400_BAD_REQUEST)

    # Create a transaction maybe ???
