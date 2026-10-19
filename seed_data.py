import os
import django
from urllib.request import urlopen
from django.core.files.base import ContentFile

# Налаштування середовища Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Final_project.settings')
django.setup()

from django.contrib.auth.models import User
from main.models import Recipe, RecipeStep, Comment

def seed_database():
    print("🧹 Очищення старої бази даних...")
    Comment.objects.all().delete()
    RecipeStep.objects.all().delete()
    Recipe.objects.all().delete()

    # Створюємо або отримуємо автора
    user, created = User.objects.get_or_create(
        username="chef_admin",
        defaults={"email": "admin@example.com"}
    )
    if created:
        user.set_password("admin12345")
        user.save()
        print("👤 Створено адміністратора: chef_admin")

    recipes_data = [
        {
            "title": "Гарбузовий Крем-Суп",
            "description": "Оксамитовий зігріваючий суп із ніжним вершковим смаком.",
            "category": "lunch",
            "difficulty": "easy",
            "cooking_time": 35,
            "image_url": "https://images.unsplash.com/photo-1547592166-23ac45744acd",
            "ingredients": "Гарбуз - 500г\nВершки - 100мл\nЦибуля - 1 шт\nЧасник - 2 зубчики\nСіль, перець - за смаком",
            "steps": ["Нарізати гарбуз та цибулю кубиками.", "Обсмажити овочі на олії до м'якості.", "Залити водою і варити 20 хвилин.", "Збити блендером, додати вершки та спеції."]
        },
        {
            "title": "Класичний Український Борщ",
            "description": "Наваристий, духмяний український борщ із м'ясом та пампушками.",
            "category": "lunch",
            "difficulty": "medium",
            "cooking_time": 120,
            "image_url": "https://images.unsplash.com/photo-1547592166-23ac45744acd",
            "ingredients": "Яловичина - 400г\nБуряк - 2 шт\nКапуста - 300г\nКартопля - 3 шт\nТоматна паста - 2 ст.л.",
            "steps": ["Зварити м'ясний бульйон.", "Додати нашинковану картоплю та капусту.", "Зробити засмажку з буряка, моркви та цибулі з томатом.", "З'єднати все, додати зелень і часник перед подачею."]
        },
        {
            "title": "Вівсяна Каша з Карамелізованими Яблуками",
            "description": "Ніжна вівсяна каша з ароматними яблуками та корицею.",
            "category": "breakfast",
            "difficulty": "easy",
            "cooking_time": 15,
            "image_url": "https://images.unsplash.com/photo-1517673132405-a56a62b18caf",
            "ingredients": "Вівсяні пластівці - 1 склянка\nМолоко - 2 склянки\nЯблуко - 1 шт\nЦукор/мед - 1 ст.л.\nКориця - дрібка",
            "steps": ["Залити вівсянку молоком і варити 7-10 хвилин.", "Нарізати яблуко кубиками та обсмажити з цукром і корицею.", "Викласти карамелізовані яблука зверху на кашу."]
        },
        {
            "title": "Класичний Французький Омлет",
            "description": "Ніжний кремовий омлет без скоринки з травами.",
            "category": "breakfast",
            "difficulty": "easy",
            "cooking_time": 10,
            "image_url": "https://images.unsplash.com/photo-1510693206972-df098062cb71",
            "ingredients": "Яйця - 3 шт\nВершкове масло - 20г\nСіль, перець - за смаком\nЗелена цибуля - пучок",
            "steps": ["Збити яйця виделкою до однорідності.", "Розтопити масло на розігрітій пательні.", "Постійно помішуючи лопаткою, готувати до кремової текстури."]
        },
        {
            "title": "Куряче Філе з Овочами-Гриль",
            "description": "Соковите куряче м'ясо з ароматними хрусткими овочами.",
            "category": "lunch",
            "difficulty": "easy",
            "cooking_time": 25,
            "image_url": "https://images.unsplash.com/photo-1532550907401-a500c9a57435",
            "ingredients": "Куряче філе - 2 шт\nКабачок - 1 шт\nБолгарський перець - 1 шт\nСпеції для курки\nОливкова олія",
            "steps": ["Замаринувати філе у спеціях та олії.", "Нарізати овочі великими шматочками.", "Обсмажити на грилі або пательні до готовності."]
        },
        {
            "title": "Паста Карбонара",
            "description": "Традиційна італійська паста з беконом та вершковим соусом.",
            "category": "lunch",
            "difficulty": "medium",
            "cooking_time": 20,
            "image_url": "https://images.unsplash.com/photo-1612874742237-6526221588e3",
            "ingredients": "Спагеті - 250г\nБекон - 150г\nЯєчні жовтки - 3 шт\nСир Пармезан - 50г",
            "steps": ["Відварити спагеті до стану аль денте.", "Обсмажити шматочки бекону до хрусткості.", "Змішати жовтки з тертим пармезаном.", "Змішати гарячу пасту з беконом та яєчною сумішшю."]
        },
        {
            "title": "Лосось на Грилі з Лимоном",
            "description": "Ніжний червоний рибний стейк із пряними травами.",
            "category": "dinner",
            "difficulty": "medium",
            "cooking_time": 20,
            "image_url": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2",
            "ingredients": "Стейк лосося - 2 шт\nЛимон - 1 шт\nОливкова олія\nРозмарин, сіль",
            "steps": ["Збризнути рибу лимонним соком та олією.", "Посипати спеціями та гілочками розмарину.", "Запікати в духовці або на грилі 15 хвилин."]
        },
        {
            "title": "Грецький Салат",
            "description": "Свіжі овочі, сир фета та оливки під оливковою заправкою.",
            "category": "lunch",
            "difficulty": "easy",
            "cooking_time": 10,
            "image_url": "https://images.unsplash.com/photo-1540420773420-3366772f4999",
            "ingredients": "Помідори - 3 шт\nОгірки - 2 шт\nСир Фета - 100г\nОливки - 50г\nОливкова олія",
            "steps": ["Крупно нарізати помідори та огірки.", "Додати оливки та кубики феті.", "Заправити оливковою олією та орегано."]
        },
        {
            "title": "Цезар із Курячим Філе",
            "description": "Хрусткий салат із фірмовим соусом, гренками та пармезаном.",
            "category": "lunch",
            "difficulty": "medium",
            "cooking_time": 20,
            "image_url": "https://images.unsplash.com/photo-1550304943-4f24f54ddde9",
            "ingredients": "Салат айсберг - 1 пучок\nКуряче філе - 200г\nСухарики - 50г\nСоус Цезар\nПармезан",
            "steps": ["Обсмажити куряче філе і нарізати слайсами.", "Порвати листя салату, додати сухарики та соус.", "Викласти курку та посипати тертим сиром."]
        },
        {
            "title": "Шоколадний Брауні",
            "description": "Вологий та насичений шоколадний десерт.",
            "category": "dessert",
            "difficulty": "medium",
            "cooking_time": 35,
            "image_url": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c",
            "ingredients": "Чорний шоколад - 200г\nВершкове масло - 150г\nЦукор - 150г\nЯйця - 3 шт\nБорошно - 100г",
            "steps": ["Розтопити шоколад із маслом.", "Збити яйця з цукром і з'єднати з шоколадною масою.", "Додати борошно, перемішати та випікати 20 хвилин."]
        },
        {
            "title": "Сирники Традиційні",
            "description": "Пишні домашні сирники зі сметаною та ягодами.",
            "category": "breakfast",
            "difficulty": "easy",
            "cooking_time": 20,
            "image_url": "https://images.unsplash.com/photo-1598214886806-c87b84b7078b",
            "ingredients": "Домашній сир - 400г\nЯйце - 1 шт\nБорошно - 3 ст.л.\nЦукор - 2 ст.л.",
            "steps": ["Розім'яти сир виделкою, додати яйце і цукор.", "Всипати борошно і сформувати кульки.", "Обсмажити на пательні до золотистої скоринки з обох боків."]
        },
        {
            "title": "Млинці з Сиром",
            "description": "Тонкі золотисті млинці з ніжною солодкою сирною начинкою.",
            "category": "breakfast",
            "difficulty": "medium",
            "cooking_time": 30,
            "image_url": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445",
            "ingredients": "Молоко - 500мл\nБорошно - 200г\nЯйця - 2 шт\nСир - 300г\nЦукор",
            "steps": ["Приготувати тісто для млинців та посмажити їх.", "Змішати сир із цукром та ваніллю для начинки.", "Загорнути сир у млинці конвертиками."]
        },
        {
            "title": "Овочі на Пару",
            "description": "Легкий та корисний гарнір із броколі, моркви та цвітної капусти.",
            "category": "dinner",
            "difficulty": "easy",
            "cooking_time": 15,
            "image_url": "https://images.unsplash.com/photo-1540420773420-3366772f4999",
            "ingredients": "Броколі - 150г\nМорква - 1 шт\nЦвітна капуста - 150г\nСіль, зелень",
            "steps": ["Розділити капусту на суцвіття, нарізати моркву.", "Помістити в пароварку на 15 хвилин.", "Подавати з краплею оливкової олії."]
        },
        {
            "title": "Курячий Бульйон із Локшиною",
            "description": "Легкий золотистий суп із домашньою локшиною та зеленню.",
            "category": "lunch",
            "difficulty": "easy",
            "cooking_time": 40,
            "image_url": "https://images.unsplash.com/photo-1547592166-23ac45744acd",
            "ingredients": "Курячі крила/гомілки - 500г\nЛокшина - 100г\nМорква - 1 шт\nЗелень",
            "steps": ["Зварити насичений курячий бульйон.", "Додати нарізану моркву та локшину.", "Варити ще 7 хвилин до готовності локшини."]
        },
        {
            "title": "Різотто з Грибами",
            "description": "Вершковий італійський рис із печерицями та пармезаном.",
            "category": "dinner",
            "difficulty": "hard",
            "cooking_time": 35,
            "image_url": "https://images.unsplash.com/photo-1633964913295-ceb43826e7c9",
            "ingredients": "Рис Арборіо - 200г\nПечериці - 200г\nБульйон - 600мл\nВершкове масло\nПармезан",
            "steps": ["Обсмажити гриби з цибулею.", "Додати рис і поступово вливати гарячий бульйон, помішуючи.", "Заправити маслом та пармезаном перед подачею."]
        },
        {
            "title": "Авокадо-Тост із Яйцем Пашот",
            "description": "Хрусткий тост із пюре з авокадо та ніжним яйцем.",
            "category": "breakfast",
            "difficulty": "medium",
            "cooking_time": 15,
            "image_url": "https://images.unsplash.com/photo-1525351484163-7529414344d8",
            "ingredients": "Хліб тостерний - 2 шт\nАвокадо - 1 шт\nЯйце - 2 шт\nЛимонний сік",
            "steps": ["Підсушити хліб у тостері.", "Розім'яти авокадо з соком лимона та сіллю, намазати на хліб.", "Зварити яйце пашот і викласти зверху."]
        },
        {
            "title": "Піца Маргарита",
            "description": "Класична італійська піца з томатним соусом, моцарелою та базиліком.",
            "category": "dinner",
            "difficulty": "medium",
            "cooking_time": 30,
            "image_url": "https://images.unsplash.com/photo-1604382355076-af4b0eb60143",
            "ingredients": "Тісто для піци - 1 шт\nТоматний соус - 100г\nСир Моцарела - 150г\nСвіжий базилік",
            "steps": ["Розкачати тісто і змастити томатним соусом.", "Викласти шматочки сиру моцарела.", "Випікати в розігрітій духовці 12 хвилин."]
        },
        {
            "title": "Мексиканські Тако з Куркою",
            "description": "Хрусткі тортильї з соковитою куркою, овочами та соусом сальса.",
            "category": "dinner",
            "difficulty": "easy",
            "cooking_time": 25,
            "image_url": "https://images.unsplash.com/photo-1565299585323-38d6b0865b47",
            "ingredients": "Тако (коржі) - 4 шт\nКуряче філе - 200г\nКукурудза - 100г\nСоус сальса",
            "steps": ["Обсмажити шматочки курки зі спеціями.", "Підігріти коржі тако.", "Наповнити коржі куркою, кукурудзою та сальсою."]
        },
        {
            "title": "Яєчня з Томатами та Беконом",
            "description": "Ситний традиційний сніданок для гарного початку дня.",
            "category": "breakfast",
            "difficulty": "easy",
            "cooking_time": 10,
            "image_url": "https://images.unsplash.com/photo-1525351484163-7529414344d8",
            "ingredients": "Яйця - 2 шт\nБекон - 50г\nПомідори чері - 5 шт\nЗелень",
            "steps": ["Обсмажити бекон до хрусткості на пательні.", "Додати помідори чері та злегка обсмажити.", "Вбити яйця і готувати до бажаного стану жовтка."]
        },
        {
            "title": "Спагеті Болоньєзе",
            "description": "Апетитна паста з м'ясним фаршем та томатним соусом.",
            "category": "lunch",
            "difficulty": "medium",
            "cooking_time": 30,
            "image_url": "https://images.unsplash.com/photo-1551183053-bf91a1d81141",
            "ingredients": "Спагеті - 250г\nМ'ясний фарш - 300г\nТомати у власному соку - 200г\nЦибуля, часник",
            "steps": ["Обсмажити фарш із цибулею та часником.", "Додати томати та тушкувати соус 15 хвилин.", "Змішати з відвареними спагеті."]
        },
        {
            "title": "Осінній Овочевий Салат",
            "description": "Мікс свіжої зелені, запечених гарбузових кубиків та насіння.",
            "category": "lunch",
            "difficulty": "easy",
            "cooking_time": 20,
            "image_url": "https://images.unsplash.com/photo-1540420773420-3366772f4999",
            "ingredients": "Мікс салат - 100г\nЗапечений гарбуз - 150г\nНасіння гарбуза - 2 ст.л.\nОливкова олія",
            "steps": ["Викласти зелень на тарілку.", "Додати шматочки запеченого гарбуза.", "Посипати насінням і заправити олією."]
        },
        {
            "title": "Панкейки на Молоці",
            "description": "Пишні американські млинці, які чудово смакують із медом чи шоколадом.",
            "category": "breakfast",
            "difficulty": "easy",
            "cooking_time": 20,
            "image_url": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445",
            "ingredients": "Борошно - 200г\nМолоко - 200мл\nЯйце - 1 шт\nЦукор - 2 ст.л.\nРозпушувач - 1 ч.л.",
            "steps": ["Змішати всі інгредієнти до консистенції густої сметани.", "Смажити на сухій розігрітій пательні без олії до появи бульбашок.", "Перевернути і смажити ще хвилину."]
        },
        {
            "title": "Курячі Нагетси Домашні",
            "description": "Хрусткі шматочки курячого філе в панірувальних сухарях.",
            "category": "dinner",
            "difficulty": "easy",
            "cooking_time": 25,
            "image_url": "https://images.unsplash.com/photo-1562967914-608f82629710",
            "ingredients": "Куряче філе - 300г\nЯйце - 1 шт\nСухарі для панірування - 100г\nСпеції",
            "steps": ["Нарізати філе на невеликі шматочки.", "Вмочити у збите яйце, потім обваляти в сухарях.", "Запікати в духовці або обсмажити до скоринки."]
        },
        {
            "title": "Фруктовий Салат із Йогуртом",
            "description": "Легкий та вітамінний мікс із сезонних фруктів під йогуртовою заправкою.",
            "category": "dessert",
            "difficulty": "easy",
            "cooking_time": 10,
            "image_url": "https://images.unsplash.com/photo-1519996529931-28324d5a630e",
            "ingredients": "Банан - 1 шт\nЯблуко - 1 шт\nКіві - 2 шт\nЙогурт натуральний - 150мл",
            "steps": ["Очистити і нарізати всі фрукти однаковими кубиками.", "Змішати у салатниці.", "Заправити натуральним йогуртом перед подачею."]
        }
    ]

    print(f"📦 Починаємо заповнення бази даних ({len(recipes_data)} рецептів із завантаженням фото)...")

    for i, data in enumerate(recipes_data, start=1):
        recipe = Recipe(
            title=data["title"],
            description=data["description"],
            category=data["category"],
            difficulty=data["difficulty"],
            cooking_time=data["cooking_time"],
            ingredients=data["ingredients"],
            author=user
        )

        # Автоматично завантажуємо картинку за посиланням та зберігаємо як файл
        try:
            response = urlopen(data["image_url"])
            file_name = f"recipe_{i}.jpg"
            recipe.image.save(file_name, ContentFile(response.read()), save=False)
        except Exception as e:
            print(f"⚠️ Не вдалося завантажити картинку для '{data['title']}': {e}")

        recipe.save()

        # Додаємо кроки приготування
        for index, step_desc in enumerate(data["steps"], start=1):
            RecipeStep.objects.create(
                recipe=recipe,
                step_number=index,
                description=step_desc
            )

        # Додаємо тестовий коментар
        Comment.objects.create(
            recipe=recipe,
            author=user,
            text="Чудовий рецепт! Вийшло дуже смачно з першого разу."
        )

    print(f"🎉 Успішно! Базу наповнено {len(recipes_data)} рецептами із реальними медіа-файлами картинок!")

if __name__ == '__main__':
    seed_database()