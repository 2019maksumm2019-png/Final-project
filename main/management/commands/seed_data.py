import os
import requests
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from main.models import Recipe, RecipeStep, Comment

class Command(BaseCommand):
    help = 'Заповнює базу даних великим меню рецептів із красивими фотографіями'

    def handle(self, *args, **options):
        # 1. Створюємо шеф-користувача
        user, created = User.objects.get_or_create(username='chef_admin')
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Створено шеф-кухаря: chef_admin'))

        # Очищаємо старі рецепти перед наповненням
        Recipe.objects.all().delete()

        # 2. Великий список з 15 рецептів
        recipes_data = [
            # --- СНІДАНКИ ---
            {
                'title': 'Пишні Панкейки на Молоці',
                'category': 'breakfast',
                'difficulty': 'easy',
                'cooking_time': 20,
                'description': 'Ніжні, духмяні американські млинці до сніданку з медом та свіжими ягодами.',
                'ingredients': "- Борошно: 200г\n- Молоко: 200мл\n- Яйце: 1 шт\n- Цукор: 2 ст. л.\n- Розпушувач: 1 ч. л.\n- Вершкове масло: 30г",
                'image_url': 'https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?auto=format&fit=crop&w=800&q=80',
                'steps': [
                    {"number": 1, "desc": "Збийте яйце з цукровим піском та тепленьким молоком."},
                    {"number": 2, "desc": "Додайте просіяне борошно з розпушувачем та розтоплене масло."},
                    {"number": 3, "desc": "Випікайте на сухій розігрітій антипригарній пательні з обох боків до золотавості."}
                ]
            },
            {
                'title': 'Ніжні Ванільні Сирники',
                'category': 'breakfast',
                'difficulty': 'easy',
                'cooking_time': 25,
                'description': 'Класичні сирники із хрусткою скоринкою та ніжною текстурою всередині.',
                'ingredients': "- Кисломолочний сир (9%): 400г\n- Яйце: 1 шт\n- Борошно: 3 ст. л.\n- Цукор: 2 ст. л.\n- Ванільний цукор: 1 ч. л.",
                'image_url': 'https://images.unsplash.com/photo-1590301157890-4810ed352733?auto=format&fit=crop&w=800&q=80',
                'steps': [
                    {"number": 1, "desc": "Розминаємо сир із яйцем, цукром та ваніллю до однорідної маси."},
                    {"number": 2, "desc": "Формуємо крулі сирники та легенько обвалюємо у борошні."},
                    {"number": 3, "desc": "Обсмажуємо на вершковому маслі на середньому вогні до золотавої скоринки."}
                ]
            },
            {
                'title': 'Авокадо Тост з Яйцем Пашот',
                'category': 'breakfast',
                'difficulty': 'medium',
                'cooking_time': 15,
                'description': 'Поживній та корисний сніданок з хрустким хлібом, пюре з авокадо та рідким жовтком.',
                'ingredients': "- Цільнозерновий хліб: 2 скибочки\n- Авокадо стигле: 1 шт\n- Яйця: 2 шт\n- Лимонний сік: 1 ч. л.\n- Оливкова олія, сіль, кунжут",
                'image_url': 'https://images.unsplash.com/photo-1525351484163-7529414344d8?auto=format&fit=crop&w=800&q=80',
                'steps': [
                    {"number": 1, "desc": "Підсушіть скибочки хліба в тостері або на сухій пательні."},
                    {"number": 2, "desc": "Розімніть авокадо виделкою із лимонним соком, сіллю та перцем."},
                    {"number": 3, "desc": "Зваріть яйце пашот у слабо киплячій воді з оцтом 3 хвилини та викладіть зверху."}
                ]
            },

            # --- ОБІДИ ТА СУПИ ---
            {
                'title': 'Класичний Український Борщ',
                'category': 'lunch',
                'difficulty': 'medium',
                'cooking_time': 120,
                'description': 'Наваристий, духмяний український борщ із м\'ясом та пампушками.',
                'ingredients': "- Свинина або яловичина: 500г\n- Картопля: 4 шт\n- Буряк: 2 шт\n- Капуста: 300г\n- Морква: 1 шт\n- Цибуля: 1 шт\n- Томатна паста: 2 ст. л.\n- Часник, зелень",
                'image_url': 'https://images.unsplash.com/photo-1547592166-23ac45744acd?auto=format&fit=crop&w=800&q=80',
                'steps': [
                    {"number": 1, "desc": "Зваріть насичений м'ясний бульйон протягом 1.5 годин."},
                    {"number": 2, "desc": "Наріжте картоплю та опустіть у киплячий бульйон."},
                    {"number": 3, "desc": "Зробіть зажарку з цибулі, моркви, буряка та томатної пасти."},
                    {"number": 4, "desc": "Додайте капусту та зажарку, варіть 15 хвилин до готовності."}
                ]
            },
            {
                'title': 'Гарбузовий Крем-Суп',
                'category': 'lunch',
                'difficulty': 'easy',
                'cooking_time': 35,
                'description': 'Оксамитовий зігріваючий суп із ніжним вершковим смаком та гарбузовим насінням.',
                'ingredients': "- Гарбуз очищений: 600г\n- Морква: 1 шт\n- Цибуля: 1 шт\n- Вершки (20%): 150мл\n- Оливкова олія, мускатний горіх",
                'image_url': 'https://images.unsplash.com/photo-1547592166-23ac45744acd?auto=format&fit=crop&w=800&q=80',
                'steps': [
                    {"number": 1, "desc": "Запечіть або обсмажте кубики гарбуза, моркви та цибулі у каструлі."},
                    {"number": 2, "desc": "Залийте овочевим бульйоном або водою та варіть 20 хвилин до м'якості."},
                    {"number": 3, "desc": "Збийте занурювальним блендером, влийте вершки та прогрійте 2 хвилини."}
                ]
            },
            {
                'title': 'Соковитий Яловичий Бургер',
                'category': 'lunch',
                'difficulty': 'medium',
                'cooking_time': 30,
                'description': 'Крафтовий соковитий бургер із котлетою з яловичини, розплавленим чедером та соусом.',
                'ingredients': "- Булочки: 2 шт\n- Яловичий фарш: 350г\n- Сир Чедер: 2 скибочки\n- Помідор, солоний огірок, салат",
                'image_url': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=800&q=80',
                'steps': [
                    {"number": 1, "desc": "Сформуйте котлети та обсмажте по 4 хвилини з кожного боку."},
                    {"number": 2, "desc": "Підрум'яньте булочки та змастіть соусом."},
                    {"number": 3, "desc": "Зберіть бургер: булочка, соус, салат, котлета з сиром, овочі."}
                ]
            },

            # --- ВЕЧЕРІ ---
            {
                'title': 'Паста Карбонара',
                'category': 'dinner',
                'difficulty': 'medium',
                'cooking_time': 25,
                'description': 'Традиційна італійська паста з ніжним яєчно-сирним соусом та хрустким беконом.',
                'ingredients': "- Спагеті: 250г\n- Бекон / гуанчале: 150г\n- Яєчні жовтки: 3 шт\n- Пармезан: 60г\n- Оливкова олія, чорний перець",
                'image_url': 'https://images.unsplash.com/photo-1612874742237-6526221588e3?auto=format&fit=crop&w=800&q=80',
                'steps': [
                    {"number": 1, "desc": "Відваріть спагеті у підсоленій воді до стану al dente."},
                    {"number": 2, "desc": "Обсмажте бекон до хрусткої скоринки."},
                    {"number": 3, "desc": "Збийте жовтки з натертим пармезаном та перцем."},
                    {"number": 4, "desc": "Змішайте пасту з беконом та яєчно-сирною сумішшю."}
                ]
            },
            {
                'title': 'Піца Маргарита',
                'category': 'dinner',
                'difficulty': 'medium',
                'cooking_time': 40,
                'description': 'Класична піца на тонкому дріжджовому тісті з томатним соусом та моцарелою.',
                'ingredients': "- Борошно: 250г\n- Дріжджі сухі: 1 ч. л.\n- Томатний соус: 4 ст. л.\n- Сир Моцарела: 150г\n- Свіжий базилік",
                'image_url': 'https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?auto=format&fit=crop&w=800&q=80',
                'steps': [
                    {"number": 1, "desc": "Замісіть дріжджове тісто та дайте йому піднятися 30 хвилин."},
                    {"number": 2, "desc": "Розкачайте основа, змастіть томатним соусом та викладіть моцарелу."},
                    {"number": 3, "desc": "Випікайте при 230°C 10-12 хвилин, прикрасьте базиліком."}
                ]
            },
            {
                'title': 'Запечений Лосось із Лимоном',
                'category': 'dinner',
                'difficulty': 'easy',
                'cooking_time': 25,
                'description': 'Ніжне соковите філе лосося, запечене з розмарином, лимоном та оливковою олією.',
                'ingredients': "- Філе лосося: 400г\n- Лимон: 1 шт\n- Оливкова олія: 2 ст. л.\n- Часник: 2 зубки\n- Свіжий розмарин, сіль, перець",
                'image_url': 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=800&q=80',
                'steps': [
                    {"number": 1, "desc": "Промийте та обсушіть філе стейків лосося."},
                    {"number": 2, "desc": "Натріть сіллю, перцем, подрібненим часником та оливковою олією."},
                    {"number": 3, "desc": "Викладіть скибочки лимона зверху та запікайте при 190°C 15-18 хвилин."}
                ]
            },
            {
                'title': 'Куряче Карі з Рисом Басматі',
                'category': 'dinner',
                'difficulty': 'medium',
                'cooking_time': 35,
                'description': 'Ароматне індійське куряче карі у ніжному кокосово-томатному соусі.',
                'ingredients': "- Куряче філе: 500г\n- Кокосове молоко: 250мл\n- Томатне пюре: 150г\n- Паста Карі / приправа: 2 ч. л.\n- Рис Басматі: 200г",
                'image_url': 'https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?auto=format&fit=crop&w=800&q=80',
                'steps': [
                    {"number": 1, "desc": "Обсмажте шматочки курки з цибулею та імбиром до золотистого кольору."},
                    {"number": 2, "desc": "Додайте спецію карі, томати та влийте кокосове молоко. Тушкуйте 20 хвилин."},
                    {"number": 3, "desc": "Подавайте гарячим разом із розсипчастим відвареним рисом басматі."}
                ]
            },

            # --- ДЕСЕРТИ ---
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
                'title': 'Класичний Італійський Тірамісу',
                'category': 'dessert',
                'difficulty': 'hard',
                'cooking_time': 30,
                'description': 'Вишуканий холодний десерт із печивом Савоярді, кремом з Маскарпоне та кавою.',
                'ingredients': "- Печиво Савоярді: 200г\n- Сир Маскарпоне: 350г\n- Яйця: 3 шт\n- Цукрова пудра: 80г\n- Міцна кава Еспресо: 200мл\n- Какао-порошок",
                'image_url': 'https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?auto=format&fit=crop&w=800&q=80',
                'steps': [
                    {"number": 1, "desc": "Збийте жовтки з цукровою пудрою, додайте Маскарпоне та збиті білки."},
                    {"number": 2, "desc": "Занурюйте печиво в охолоджену каву на 1 секунду та викладайте у форму."},
                    {"number": 3, "desc": "Перешаруйте кремом, охолодіть 4 години та посипте какао перед подачею."}
                ]
            },
            {
                'title': 'Ягідний Чізкейк',
                'category': 'dessert',
                'difficulty': 'medium',
                'cooking_time': 50,
                'description': 'Ніжний сирний чізкейк із пісочною основою та свіжою полуницею.',
                'ingredients': "- Печиво пісочне: 200г\n- Вершкове масло: 80г\n- Вершковий сир: 500г\n- Вершки 33%: 150мл\n- Свіжі ягоди",
                'image_url': 'https://images.unsplash.com/photo-1533134242443-d4fd215305ad?auto=format&fit=crop&w=800&q=80',
                'steps': [
                    {"number": 1, "desc": "Подрібніть печиво в крихту, змішайте з вершковим маслом і утрамбуйте у форму."},
                    {"number": 2, "desc": "Збийте вершковий сир із цукром та вершками, викладіть на основу."},
                    {"number": 3, "desc": "Запікайте на водяній бані при 160°C 50 хвилин, прикрасьте ягодами."}
                ]
            },

            # --- НАПОЇ ---
            {
                'title': 'Освіжаючий Безалкогольний Мохіто',
                'category': 'drinks',
                'difficulty': 'easy',
                'cooking_time': 10,
                'description': 'Прохолодний літній напій із соковитим лаймом, ароматною м\'ятою та льодом.',
                'ingredients': "- Лайм: 0.5 шт\n- Свіжа м'ята: 10 листочків\n- Sprite / содова: 200мл\n- Цукор: 2 ч. л., лід",
                'image_url': 'https://images.unsplash.com/photo-1551024709-8f23befc6f87?auto=format&fit=crop&w=800&q=80',
                'steps': [
                    {"number": 1, "desc": "Розімніть у склянці м'яту, лайм та цукор."},
                    {"number": 2, "desc": "Засипте льодом і залийте содовою."}
                ]
            },
            {
                'title': 'Густий Полунично-Банановий Смузі',
                'category': 'drinks',
                'difficulty': 'easy',
                'cooking_time': 5,
                'description': 'Вітамінний та позивний коктейль із стиглого банана, полуниці та натурального йогурту.',
                'ingredients': "- Заморожена або свіжа полуниця: 150г\n- Банан: 1 шт\n- Грецький йогурт: 150мл\n- Мед: 1 ч. л.",
                'image_url': 'https://images.unsplash.com/photo-1553530666-ba11a7da3888?auto=format&fit=crop&w=800&q=80',
                'steps': [
                    {"number": 1, "desc": "Покладіть у чашу блендера ягоди, шматочки банана, йогурт та ложку меду."},
                    {"number": 2, "desc": "Збийте на високій швидкості протягом 1-2 хвилин до однорідної консистенції."}
                ]
            }
        ]

        # 3. Створення записів та завантаження фотографій
        for data in recipes_data:
            steps_data = data.pop('steps')
            image_url = data.pop('image_url')
            
            recipe = Recipe.objects.create(author=user, **data)

            # Скачування зображення
            try:
                response = requests.get(image_url, timeout=10)
                if response.status_code == 200:
                    file_name = f"recipe_{recipe.pk}.jpg"
                    recipe.image.save(file_name, ContentFile(response.content), save=True)
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Не вдалося завантажити фото для {recipe.title}: {e}"))

            # Створення кроків приготування
            for step in steps_data:
                RecipeStep.objects.create(
                    recipe=recipe,
                    step_number=step['number'],
                    description=step['desc']
                )

            # Додавання коментаря
            Comment.objects.create(
                recipe=recipe,
                author=user,
                text="Чудовий рецепт! Вийшло дуже смачно з першого разу."
            )

        self.stdout.write(self.style.SUCCESS(f'Базу успішно наповнено {len(recipes_data)} смачними рецептами!'))