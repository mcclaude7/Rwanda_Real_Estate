from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
import uuid
from .models import Payment
from .serializers import PaymentSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Payments.
    - list: GET /api/v1/payments/payments/
    - retrieve: GET /api/v1/payments/payments/{id}/
    - mtn_momo: POST /api/v1/payments/payments/mtn_momo/
    - calculate_emi: POST /api/v1/payments/payments/calculate_emi/
    """
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='mtn-momo')
    def mtn_momo(self, request):
        """POST /api/v1/payments/payments/mtn-momo/ - Initiate MTN MoMo payment"""
        phone = request.data.get('phone')
        amount = request.data.get('amount')
        purpose = request.data.get('purpose', 'listing-fee')
        if not phone or not amount:
            return Response({'error': 'phone and amount required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                payment = Payment.objects.create(
                    user=request.user, amount=amount, currency='RWF',
                    payment_method='mtn-momo', purpose=purpose,
                    momo_phone=phone, transaction_id=str(uuid.uuid4()),
                    status='initiated'
                )
            return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'], url_path='calculate-emi')
    def calculate_emi(self, request):
        """POST /api/v1/payments/payments/calculate-emi/ - Calculate EMI"""
        loan_amount = float(request.data.get('loan_amount', 0))
        interest_rate = float(request.data.get('interest_rate', 0)) / 100
        tenure_years = int(request.data.get('tenure_years', 1))
        monthly_rate = interest_rate / 12
        total_months = tenure_years * 12
        if monthly_rate == 0:
            emi = loan_amount / total_months
        else:
            emi = loan_amount * monthly_rate * (1 + monthly_rate) ** total_months / ((1 + monthly_rate) ** total_months - 1)
        return Response({
            'monthly_emi': round(emi, 2),
            'total_payment': round(emi * total_months, 2),
            'total_interest': round((emi * total_months) - loan_amount, 2),
        })