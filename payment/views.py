from django.shortcuts import render, get_list_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from payment.models import Payment, Transaction
from payment.serializers import PaymentSerializer, TransactionSerializer
from payment.permissions import IsPaymentOwnerOrAdmin, IsTransactionOwnerOrAdmin


class PaymentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsPaymentOwnerOrAdmin]
    serializer_class = PaymentSerializer

    def get_queryset(self):
        payments = Payment.objects.all()
        if not self.request.user.is_superuser:
            payments = payments.filter(order__user=self.request.user)
        return payments

    @action(detail=True, methods=["GET"], permission_classes=[IsPaymentOwnerOrAdmin,])
    def transactions(self, request, pk=None):
        payment = self.get_object()
        transactions = get_list_or_404(Transaction, payment=payment)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsTransactionOwnerOrAdmin]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        transactions = Transaction.objects.all()
        if not self.request.user.is_superuser:
            transactions = transactions.filter(payment__order__user=self.request.user)
        return transactions
