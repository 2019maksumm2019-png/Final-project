import os
import requests
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from main.models import Recipe, RecipeStep, Comment

class Command(BaseCommand):
    help = 'Заповнює базу даних рецептами з красивими фотографіями'

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(username='chef_admin')
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Створено шеф-кухаря: chef_admin'))

        # Очищаємо старі рецепти
        Recipe.objects.all().delete()

        # Рецепти з посиланнями на якісні фото
        recipes_data = [
            {
                'title': 'Класичний Український Борщ',
                'category': 'lunch',
                'difficulty': 'medium',
                'cooking_time': 120,
                'description': 'Ароматний, наваристий та дуже смачний український борщ із пампушками.',
                'ingredients': "- Свинина або яловичина: 500г\n- Картопля: 4 шт\n- Буряк: 2 шт\n- Капуста: 300г\n- Морква: 1 шт\n- Цибуля: 1 шт\n- Томатна паста: 2 ст. л.\n- Часник, зелень, сіль, перець",
                'image_url': 'https://images.unsplash.com/photo-1547592166-23ac45744acd?auto=format&fit=crop&w=800&q=80',
                'steps': [
                    {"number": 1, "desc": "Зваріть насичений м'ясний бульйон протягом 1.5 годин."},
                    {"number": 2, "desc": "Наріжте картоплю та опустите у киплячий бульйон."},
                    {"number": 3, "desc": "Зробіть зажарку з цибулі, моркви, буряка та томатної пасти."},
                    {"number": 4, "desc": "Додайте капусту та зажарку, варіть 15 хвилин до готовності."}
                ]
            },
            {
                'title': 'Пишні Панкейки на Молоці',
                'category': 'breakfast',
                'difficulty': 'easy',
                'cooking_time': 20,
                'description': 'Ніжні, духмяні американські млинці до сніданку з медом та ягодами.',
                'ingredients': "- Борошно: 200г\n- Молоко: 200мл\n- Яйце: 1 шт\n- Цукор: 2 ст. л.\n- Розпушувач: 1 ч. л.\n- Вершкове масло: 30г",
                'image_url': 'https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?auto=format&fit=crop&w=800&q=80',
                'steps': [
                    {"number": 1, "desc": "Збийте яйце з цукром та тепленьким молоком."},
                    {"number": 2, "desc": "Додайте борошно з розпушувачем та розтоплене масло."},
                    {"number": 3, "desc": "Випікайте на сухій розігрітій пательні з обох боків."}
                ]
            },
            {
                'title': 'Паста Карбонара',
                'category': 'dinner',
                'difficulty': 'medium',
                'cooking_time': 25,
                'description': 'Традиційна італійська паста з ніжним соусом та хрустким беконом.',
                'ingredients': "- Спагеті: 250г\n- Бекон: 150г\n- Яєчні жовтки: 3 шт\n- Пармезан: 60г\n- Оливкова олія, чорний перець",
                'image_url': 'https://images.unsplash.com/photo-1612874742237-6526221588e3?auto=format&fit=crop&w=800&q=80',
                'steps': [
                    {"number": 1, "desc": "Відваріть спагеті у підсоленій воді до стану al dente."},
                    {"number": 2, "desc": "Обсмажте бекон до хрусткої скоринки."},
                    {"number": 3, "desc": "Збийте жовтки з натертим пармезаном та перцем."},
                    {"number": 4, "desc": "Змішайте пасту з беконом та яєчно-сирною сумішшю."}
                ]
            },
            {
                'title': 'Соковитий Яловичий Бургер',
                'category': 'lunch',
                'difficulty': 'medium',
                'cooking_time': 30,
                'description': 'Домашній крафтовий бургер із котлетою, чедером та соковитими овочами.',
                'ingredients': "- Булочки: 2 шт\n- Яловичий фарш: 350г\n- Сир Чедер: 2 скибочки\n- Помідор, солоний огірок, салат",
                'image_url': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=800&q=80',
                'steps': [
                    {"number": 1, "desc": "Сформуйте котлети та обсмажте по 4 хвилини з кожного боку."},
                    {"number": 2, "desc": "Підрум'яньте булочки та змастіть соусом."},
                    {"number": 3, "desc": "Зберіть бургер: булочка, соус, салат, котлета з сиром, овочі."}
                ]
            },
            {
                'title': 'Шоколадний Брауні',
                'category': 'dessert',
                'difficulty': 'medium',
                'cooking_time': 40,
                'description': 'Американський десерт із багатим шоколадним смаком та вологою серединкою.',
                'ingredients': "- Чорний шоколад: 200г\n- Вершкове масло: 150г\n- Яйця: 3 шт\n- Цукор: 150г\n- Борошно: 100г",
                'image_url': 'https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=800&q=80',
                'steps': [
                    {"number": 1, "desc": "Розтопіть шоколад із вершковим маслом на водяній бані."},
                    {"number": 2, "desc": "Збийте яйця з цукром, з'єднайте з шоколадом та борошном."},
                    {"number": 3, "desc": "Випікайте при 180°C протягом 25 хвилин."}
                ]
            },
            {
                'title': 'Освіжаючий Безалкогольний Мохіто',
                'category': 'drinks',
                'difficulty': 'easy',
                'cooking_time': 10,
                'description': 'Прохолодний напій із соковитим лаймом, ароматною м\'ятою та льодом.',
                'ingredients': "- Лайм: 0.5 шт\n- Свіжа м'ята: 10 листочків\n- Sprite / содова: 200мл\n- Цукор: 2 ч. л., лід",
                'image_url': 'https://images.unsplash.com/photo-1551024709-8f23befc6f87?auto=format&fit=crop&w=800&q=80',
                'steps': [
                    {"number": 1, "desc": "Розімніть у склянці м'яту, лайм та цукор."},
                    {"number": 2, "desc": "Засипте льодом і залийте содовою."}
                ]
            }
        ]

        for data in recipes_data:
            steps_data = data.pop('steps')
            image_url = data.pop('image_url')
            
            recipe = Recipe.objects.create(author=user, **data)

            # Завантажуємо зображення
            try:
                response = requests.get(image_url, timeout=10)
                if response.status_code == 200:
                    file_name = f"recipe_{recipe.pk}.jpg"
                    recipe.image.save(file_name, ContentFile(response.content), save=True)
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Не вдалося завантажити фото для {recipe.title}: {e}"))

            for step in steps_data:
                RecipeStep.objects.create(
                    recipe=recipe,
                    step_number=step['number'],
                    description=step['desc']
                )

            Comment.objects.create(
                recipe=recipe,
                author=user,
                text="Дуже смачна страва! Всім рекомендую спробувати."
            )

        self.stdout.write(self.style.SUCCESS('Базу успішно наповнено рецептами разом із фотографіями!'))