from rest_framework import generics, permissions
from reviews_app.models import Review
from .serializers import ReviewSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter

class ReviewFilter(filters.FilterSet):
    rating = filters.NumberFilter(field_name="rating", lookup_expr="gte")
    updated_at = filters.DateTimeFilter(field_name="updated_at", lookup_expr="gte")

    class Meta:
        model = Review
        fields = ['rating', 'updated_at']


class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ReviewFilter
    search_fields = ['description']
    ordering_fields = ['updated_at', 'rating']
    ordering = ['-updated_at']
    pagination_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        business_user_id = self.request.query_params.get('business_user_id')
        reviewer_id = self.request.query_params.get('reviewer_id')

        if business_user_id:
            queryset = queryset.filter(business_user_id=business_user_id)
        if reviewer_id:
            queryset = queryset.filter(reviewer_id=reviewer_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

class IsReviewerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.reviewer == request.user or request.user.is_staff

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsReviewerOrAdmin]

    def perform_update(self, serializer):
        serializer.save()
