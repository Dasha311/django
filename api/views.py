from api.serializers import DishSerializer, CourierSerializer, RestaurantSerializer, MenuSerializer, OrderItemSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from store.models import Dish, Courier, Restaurant, Menu, OrderItem
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.utils import timezone
import django_filters

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10  
    page_size_query_param = 'page_size'  
    max_page_size = 100  


class DishList(ListAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, OrderingFilter)
    filterset_fields = ['name', 'is_available']  
    ordering_fields = ['name', 'price']  
    ordering = ['name']  


class DishDetailView(RetrieveAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [IsAuthenticated]


class CourierDetailView(RetrieveAPIView):
    queryset = Courier.objects.all()
    serializer_class = CourierSerializer
    permission_classes = [IsAuthenticated]
    

class RestaurantFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label="Restaurant Name (partial)")
    open_from = django_filters.NumberFilter(field_name='open_from', lookup_expr='lte', label="Open From (Hour)")
    open_until = django_filters.NumberFilter(field_name='open_until', lookup_expr='gte', label="Open Until (Hour)")

    class Meta:
        model = Restaurant
        fields = ['name', 'open_from', 'open_until']

    def filter_open_hours(self, queryset, name, value):
        if value is not None:
            return queryset.filter(Q(open_from__lte=value) & Q(open_until__gt=value))
        return queryset
       
 
class AllRestaurantsView(ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filterset_class = RestaurantFilter  
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, OrderingFilter)
    ordering_fields = ['name', 'open_from']  
    ordering = ['name']  


class CurrentlyOpenRestaurantsView(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        current_hour = timezone.now().hour
        open_restaurants = Restaurant.objects.filter(open_from__lte=current_hour, open_until__gte=current_hour)
        paginator = self.pagination_class()
        paginated_restaurants = paginator.paginate_queryset(open_restaurants, request)
        serializer = RestaurantSerializer(paginated_restaurants, many=True)
        return paginator.get_paginated_response(serializer.data)

    
class RestaurantDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]
    
    
class MenuDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination  

    def get(self, request, *args, **kwargs):
        menu = self.get_object()
        dishes = Dish.objects.filter(menu=menu)
        paginator = self.pagination_class()
        paginated_dishes = paginator.paginate_queryset(dishes, request)
        dish_serializer = DishSerializer(paginated_dishes, many=True)
        return paginator.get_paginated_response(dish_serializer.data)


class OrderDetailView(RetrieveAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]


class OrderCreateView(ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination  
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, OrderingFilter)
    filterset_fields = ['order__status', 'dish__name']  
    ordering_fields = ['created_at', 'dish__name']  
    ordering = ['created_at']  
