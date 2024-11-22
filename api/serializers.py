from datetime import datetime
from decimal import Decimal
from rest_framework import serializers
from store.models import Customer, Courier, Restaurant, Dish, Order, OrderItem

class DishSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=512)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    is_available = serializers.BooleanField()

    def validate_price(self, price):
        if 100 <= price <= 100000:
            return price
        else:
            raise serializers.ValidationError("Price must be between 100 and 100000")

    def create(self, validated_data):
        return Dish.objects.create(**validated_data)


class CustomerSerializer(serializers.Serializer):
    user = serializers.CharField()
    address = serializers.CharField(max_length=300)


class CourierSerializer(serializers.Serializer):
    user = serializers.CharField()
    phone = serializers.CharField(max_length=100)
    vehicle_type = serializers.CharField(max_length=50)
    status = serializers.CharField(max_length=100)


class RestaurantSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=300)
    phone = serializers.CharField(max_length=100)
    open_from = serializers.IntegerField()
    open_until = serializers.IntegerField()
    
    def create(self, validated_data):
        return Restaurant.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.open_from = validated_data.get('open_from', instance.open_from)
        instance.open_until = validated_data.get('open_until', instance.open_until)
        instance.save()
        return instance


class MenuSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    restaurant = RestaurantSerializer()
    dishes = DishSerializer(many=True)
    
    def create(self, validated_data):
        dishes = validated_data.pop('dishes', [])
        menu = Menu.objects.create(**validated_data)
        menu.dishes.set(dishes)  
        return menu

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.restaurant = validated_data.get('restaurant', instance.restaurant)

        if 'dishes' in validated_data:
            dishes = validated_data.pop('dishes')
            instance.dishes.set(dishes)  

        instance.save()
        return instance


class OrderSerializer(serializers.Serializer):
    customer = CustomerSerializer()
    courier = CourierSerializer()
    restaurant = RestaurantSerializer()
    status = serializers.BooleanField(default=False)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    delivery_fee = serializers.DecimalField(max_digits=10, decimal_places=2)
    created_at = serializers.DateTimeField(default=datetime.now)


class OrderItemSerializer(serializers.Serializer):
    customer_name = serializers.CharField(source='order.customer.user.username')
    courier_name = serializers.CharField(source='order.courier.user.username')
    restaurant_name = serializers.CharField(source='order.restaurant.name')
    dish_name = serializers.CharField(source='dish.name')
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    created_at = serializers.DateTimeField(default=datetime.now)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    delivery_fee = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    def validate(self, data):
        print(data.get('order').get('customer'))
        customer_name = data.get('order').get('customer').get('user').get('username')
        courier_name = data.get('order').get('courier').get('user').get('username')
        restaurant_name = data.get('order').get('restaurant').get('name')
        dish_name = data.get('dish').get('name')

        try:
            data['customer'] = Customer.objects.get(user__username=customer_name)
        except Customer.DoesNotExist:
            raise serializers.ValidationError(f"Customer with username '{customer_name}' not found.")

        try:
            data['courier'] = Courier.objects.get(user__username=courier_name)
        except Courier.DoesNotExist:
            raise serializers.ValidationError(f"Courier with username '{courier_name}' not found.")

        try:
            data['restaurant'] = Restaurant.objects.get(name=restaurant_name)
        except Restaurant.DoesNotExist:
            raise serializers.ValidationError(f"Restaurant with name '{restaurant_name}' not found.")

        try:
            data['dish'] = Dish.objects.get(name=dish_name)
        except Dish.DoesNotExist:
            raise serializers.ValidationError(f"Dish with name '{dish_name}' not found.")

        return data

    def create(self, validated_data):
        order = Order.objects.create(
            customer=validated_data['customer'],
            courier=validated_data['courier'],
            restaurant=validated_data['restaurant'],
            total_amount=validated_data['price'] * validated_data['quantity'],
            delivery_fee=validated_data['price'] * Decimal('0.1'),
        )

        return OrderItem.objects.create(
            order=order,
            dish=validated_data['dish'],
            quantity=validated_data['quantity'],
            price=validated_data['price'],
        )
