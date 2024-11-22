from django.apps import AppConfig
from faker import Faker

fake = Faker()

def populate(n):
    from store.models import Dish
    
    for _ in range(n):
        Dish.objects.create(
            name=fake.name(),
            description=fake.text(),
            price=fake.pyint(100, 6000),
            is_available=fake.boolean()
        )

class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'
    
    def ready(self):
        populate(1)