from django.apps import AppConfig
from django.db.models.signals import post_migrate
from faker import Faker

fake = Faker()

def populate(sender, **kwargs):
    from store.models import Dish
    
    if not Dish.objects.exists():
        for _ in range(10):
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
        post_migrate.connect(populate, sender=self)