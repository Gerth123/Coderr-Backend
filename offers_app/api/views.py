from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from offers_app.models import Offer, OfferDetail
from .serializers import OfferSerializer, OfferDetailSerializer
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from .permissions import IsBusinessOwnerOrReadOnly

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 100

class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 6
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 100

class OfferFilter(filters.FilterSet):
    creator_id = filters.NumberFilter(field_name='user', lookup_expr='exact')
    max_delivery_time = filters.NumberFilter(method='filter_by_max_delivery_time')

    class Meta:
        model = Offer
        fields = ['creator_id', 'min_price', 'min_delivery_time']

    def filter_by_max_delivery_time(self, queryset, name, value):
        """
        Filters the queryset based on the max_delivery_time field.
        """
        return queryset.filter(min_delivery_time__lte=value)

class OfferListCreateView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = OfferFilter
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']
    ordering = ['updated_at']
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        '''
        Create a new offer.
        '''
        serializer.save(user=self.request.user.userprofile)
        
class SingleOfferView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsBusinessOwnerOrReadOnly]
    lookup_field = 'pk'

class OfferDetailView(generics.RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsBusinessOwnerOrReadOnly]

    def get_object(self):
        """
        Returns the object the view is displaying.
        """
        return super().get_object()