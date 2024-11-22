from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from api import views

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=False,
   permission_classes=(permissions.IsAuthenticatedOrReadOnly,),
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('dishes/', views.DishList.as_view()),
    path('dishes/<int:pk>', views.DishDetailView.as_view()),
    path('couriers/<int:pk>', views.CourierDetailView.as_view()),
    path('restaurants/', views.AllRestaurantsView.as_view(), name='all_restaurants'),
    path('restaurants/<int:pk>/', views.RestaurantDetailView.as_view(), name='restaurant_detail'),
    path('restaurants/open-now/', views.CurrentlyOpenRestaurantsView.as_view(), name='open_restaurants'),
    path('menus/<int:pk>', views.MenuDetailView.as_view()),
    path('orders/', views.OrderCreateView.as_view()),
    path('orders/<int:pk>', views.OrderDetailView.as_view()),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
