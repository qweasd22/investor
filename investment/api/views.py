from rest_framework import viewsets
from core.models import Client, Security, Investment, Deposit, QuoteHistory
from .serializers import (
    ClientSerializer, 
    SecuritySerializer,
    InvestmentSerializer,
    DepositSerializer,
    QuoteHistorySerializer
)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filterset_fields = ['ownership_type']

class SecurityViewSet(viewsets.ModelViewSet):
    queryset = Security.objects.all()
    serializer_class = SecuritySerializer
    search_fields = ['code', 'name']

class InvestmentViewSet(viewsets.ModelViewSet):
    queryset = Investment.objects.select_related('client', 'security')
    serializer_class = InvestmentSerializer

class DepositViewSet(viewsets.ModelViewSet):
    queryset = Deposit.objects.select_related('client')
    serializer_class = DepositSerializer

class QuoteHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = QuoteHistorySerializer
    
    def get_queryset(self):
        return QuoteHistory.objects.filter(
            security_id=self.kwargs['security_pk']
        )