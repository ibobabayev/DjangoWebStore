from django.core.management import BaseCommand
from catalog.models import Catalog,Product,Contact
import json

class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        with open('fixtures/data.json','r',encoding='UTF-8') as f:
            data = json.load(f)
        return data

    def handle(self, *args, **options):
        Catalog.objects.all().delete()
        Product.objects.all().delete()
        Contact.objects.all().delete()

        catalog_for_create = []
        contact_for_create = []

        # Обходим все значения категорий из фиктсуры для получения информации об одном объекте
        for catalog in Command.json_read_categories():
            if catalog["model"] == "catalog.catalog":
                catalog_for_create.append(Catalog(**catalog['fields']))

        # Создаем объекты в базе с помощью метода bulk_create()
        Catalog.objects.bulk_create(catalog_for_create)

        products=[{"name": "Iphone15","description": "Новая модель","photo": "",'category':catalog_for_create[0],"price": 1000},
                  {"name": "Iphone14","description": "Предпоследняя модель","photo": "","category":catalog_for_create[0],"price": 900},
                  {"name": "Война и Мир","description": "Бедный Балконский...","photo": "","category":catalog_for_create[1],"price": 25},
                  {"name": "Преступление и наказание","description": "Так и надо этой процентщице!","photo": "","category":catalog_for_create[1],"price": 30},
                  {"name": "Кроссовки","description": "От Nike","photo": "","category":catalog_for_create[2],"price": 50},
                  {"name": "Костюм от Валентино","description": "Оно ещё не ваше","photo": "","category":catalog_for_create[2],"price": 100}
                  ]

        for product in products:
            Product.objects.create(**product)

        contacts = [{'name':'BakMilStore','number':'(+90)555-300-20-10','email':'pasha@mail.com'}]
        for contact in contacts:
            Contact.objects.create(**contact)