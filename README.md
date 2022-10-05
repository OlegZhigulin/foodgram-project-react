![finaltask](https://github.com/OlegZhigulin/foodgram-project-react/actions/workflows/yamdb_workflow.yml/badge.svg)
## Описание
FOODGRAM = это новый сервис, который поможет Вам делится рецептами и разнообразить свои кулинарные способности.
Доступен по адресу 51.250.11.18
А поиск по тегам поможет вам легко и быстро сориентироваться в предлагаемых рецептах.
Кулинарные рецепты с фото помогают получать о готовом блюде самое точное представление.
""ЛЮБОВЬ ПРИХОДИТ И УХОДИТ А КУШАТЬ ХОЧЕТСЯ ВСЕГДА""
#### Реализован функционал, дающий возможность:
* Регистрироваться на сайте.
* Оставлять и редактировать рецепты.
* Добавлять рецепты в избранное, в список покупок.
* Скачивать список необходимых ингредиентов. 
* Подписываться на других авторов. 

### Технологии
``` 
Python 3.7
Django 3.2
DRF 3.12.4
docker-compose 3.8
React 17.0.1
PostgresSQL 13.0
```

# Endpoint:
- Ресурс auth: аутентификация, получение токена.
- Ресурс users: пользователи, подписки на авторов.
- Ресурс recipes: рецепты, избранные рецепты, список покупок.
- Ресурс tags: теги к рецептам.
- Ресурс ingredients: ингредиенты для рецептов.-



# инструкция по запуску и настройке

## в терминале выполнить команду:
git@github.com:OlegZhigulin/foodgram-project-react.git


## В переменную окружения .env добавить:
```{
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME= # имя базы данных
POSTGRES_USER= # логин для подключения к базе данных
POSTGRES_PASSWORD= # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД }
```




# Примеры запросов к API:

### Авторизация пользователя
На эндпоинт http://51.250.11.18/api/users/ передаем POST запрос с обязательными параметрами first_name, last_name, username, password и email. 
```
{
"email": "CameronDiaz@yandex.ru",
"username": "Cameron1996",
"first_name": "Василий",
"last_name": "Иванов",
"password": "Qwerty123"
}
```
при успешной регистрации получаем ответ и статус код 201:
```
{
"email": "CameronDiaz@yandex.ru",
"id": 0,
"username": "Cameron1996",
"first_name": "Василий",
"last_name": "Иванов"
}
```
### Получаем токен
Далее, на эндпоинт http://51.250.11.18/api/auth/token/login передаем POST запрос с параметрами email и password. В ответ получаем токен, который используем для выполнения запросов как авторизованный пользователь.
```
{
"auth_token": "2313sadsadsd11010"
}
```
При отправке запроса передавайте токен в заголовке Authorization: BearTokener <<токен>>
### Просмотр списка ингредиентов 
Передаем GET запрос на эндпоинт http://51.250.11.18/api/ingredients/:
```
[
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "малоко",
            "measurement_unit": "литр"
        },
        {
            "id": 2,
            "name": "абрикосовое пюре",
            "measurement_unit": "г"
        },
        {
            "id": 3,
            "name": "абрикосовое варенье",
            "measurement_unit": "г"
        }
    ]
}
]
```

### Просмотр списка тегов 
Передаем GET запрос на эндпоинт http://51.250.11.18/api/tags/:
```
[
    {
        "id": 6,
        "name": "обед",
        "color": "#FFA500",
        "slug": "lanch"
    },
    {
        "id": 7,
        "name": "ужин",
        "color": "#008000",
        "slug": "dinner"
    },
    {
        "id": 8,
        "name": "перекус",
        "color": "#800080",
        "slug": "snack"
    },
    {
        "id": 9,
        "name": "фастфуд",
        "color": "#FFFF00",
        "slug": "fastfood"
    }
]
```
### Создаем новыe рецепт 
Передаем POST-запрос на адрес http://51.250.11.18/api/recipes/
Обязательные поля:   
```
{
"ingredients": [
        {
            "id": 1123,
            "amount": 10
        }
    ],
"tags": [
        1,
        2
    ],
"image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABA",
"name": "Вареники с картошкой",
"text": "Рецептов вареников с картошкой существует множество. Причем вариации касаются как начинки, так и самого теста. Кто-то готовит последнее на воде, кто-то не использует яйца, кто-то добавляет в него и соль, и сахар.",
"cooking_time": 120
}
```
Ответ будет выглядеть следующим образом:   

```
{
"id": 12,
"tags": [
{
"id": 1,
"name": "Завтрак",
"color": "#E26C2D",
"slug": "breakfast"
}
],
"author": {
"email": "user@example.com",
"id": 0,
"username": "Muchahos",
"first_name": "Амиго",
"last_name": "Мучачо",
"is_subscribed": false
},
"ingredients": [
    {"id": 1123,
    "name": "Картофель отварной",
    "measurement_unit": "г",
    "amount": 10}
],
"is_favorited": true,
"is_in_shopping_cart": False,
"name": "Вареники с картошкой",
"image": "http://51.250.11.18/media/recipes/images/image.jpeg",
"text": ""Рецептов вареников с картошкой существует множество. Причем вариации касаются как начинки, так и самого теста. Кто-то готовит последнее на воде, кто-то не использует яйца, кто-то добавляет в него и соль, и сахар."",
"cooking_time": 120
}
```

### Редактируем рецепт 
Передаем POST-запрос на адрес http://51.250.11.18/api/recipes/{id}/
Обязательные поля:   
```

{
  "ingredients": [
    {
      "id": 23,
      "amount": 1
    }
  ],
  "tags": [
    8
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "Макароны",
  "text": "Макароны с фаршем и овощами",
  "cooking_time": 25
}
```

### Получаем список людей на которых мы подписаны.
Передаем GET-запрос на адрес http://51.250.11.18/api/users/subscriptions/

Ответ будет выглядеть следующим образом:

```
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 2,
            "email": "oleg@oleg.oleg",
            "username": "oleg",
            "first_name": "oleg",
            "last_name": "eolg",
            "is_subscribed": true,
            "recipes": [
                {
                    "id": 1,
                    "name": "макарики",
                    "image": "/media/recipes/images/raise_for_status.png",
                    "cooking_time": 12
                }
            ],
            "recipes_count": 1
        }
    ]
}
```
### Скачать список для покупки ингредиентов
Передаем GET-запрос на адрес http://51.250.11.18/api/recipes/download_shopping_cart/

Ответ будет PDF файл:

```
(https://github.com/OlegZhigulin/foodgram-project-react/backend/foodgram/data/example_list_page.jpeg)
```

# Документация (запросы для работы с API): http://localhost/redoc/


# для завершения работы нажмите Ctrl+C

### backend  Жигулин Олег телеграм @Oleg_Zhigulin
### frontend  Yandex Practicum
