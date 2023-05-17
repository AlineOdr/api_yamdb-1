Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка».  Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
# api_yamdb
Это API-сервис для YaMDb, который позволяет интегрировать сервисы YaMDb для других платформ.
### Как запустить проект:

Клонировать репозиторий:

```
git clone git@github.com:inovaras/api_yamdb.git
```

Перейти в него в командной строке:
```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source venv/Scripts/activate
```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```
### Примеры использования:
1) Регистрация нового пользователя:
* Отправить POST-запрос http://127.0.0.1:8000/api/v1/auth/signup/. В теле запроса указать: 
```
{
    "email": "user@example.com",
    "username": "string"
}
```

В ответ придет письмо, где будет указан confirmation_code
2) Получение JWT-токена:
* Отправить POST-запрос http://127.0.0.1:8000/api/v1/auth/token/. В теле запроса указать:
```
{
    "username": "string",
    "confirmation_code": "string"
}
```
* В ответ придёт JWT-токен в форме:

```commandline
{
    "token": "string"
}
```

3) Получение списка всех пользователей (может получить только администратор):

* Отправить GET-запрос http://127.0.0.1:8000/api/v1/users/.
* Ответ придёт в форме:

```
{
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": 
[
        {
            "username": "string",
            "email": "user@example.com",
            "first_name": "string",
            "last_name": "string",
            "bio": "string",
            "role": "user"
        }
    ]
}
```
4) Добавление пользователя (доступно только администратору, email и username должны быть уникальными):

* Отправить POST-запрос http://127.0.0.1:8000/api/v1/users/. В теле запроса указать:
```
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
```
* Ответ придёт в форме:

```
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
```

5) Получение пользователя по username (доступно только администратору):
* Отправить GET-запрос http://127.0.0.1:8000/api/v1/users/{username}/. 
```
* Ответ придёт в форме:
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
```
6) Изменение данных пользователя по username (доступно только администратору, email и username должны быть уникальными):
* Отправить PATCH-запрос http://127.0.0.1:8000/api/v1/users/{username}/. В теле запроса указать
```
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
```

* Ответ придёт в форме:
```
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
```
6) Удаление пользователя по username (удалить публикацию может только администратор):
* Отправить DELETE-запрос http://127.0.0.1:8000/api/v1/users/{username}/

7) Получение данных своей учетной записи (может получить любой авторизованный пользователь):

* Отправить GET-запрос http://127.0.0.1:8000/api/v1/users/me/
* Ответ придёт в форме:
```
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
```
8) Изменение данных своей учетной записи (может любой авторизованный пользователь, email и username должны быть уникальными):

* Отправить PATCH-запрос http://127.0.0.1:8000/api/v1/users/me/. В теле запроса указать:
```
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string"
}
```
* Ответ придёт в форме:

```
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
```
9) Получить список всех отзывов (Права доступа: Доступно без токена):
* Отправить GET-запрос http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/ :
* Ответ придёт в форме:

```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "score": 1,
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```
10) Добавить новый отзыв. Пользователь может оставить только один отзыв на произведение (Права доступа: Аутентифицированные пользователи.):
* Отправить POST-запрос http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/. В теле запроса указать:
```
{
  "text": "string",
  "score": 1
}
```
* Ответ придёт в форме:

```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
11) Получить отзыв по id для указанного произведения (Права доступа: Доступно без токена.):
* Отправить GET-запрос http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/ :
* Ответ придёт в форме:

```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
12) Частично обновить отзыв по id (Права доступа: Автор отзыва, модератор или администратор.):
* Отправить PATCH-запрос http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/. В теле запроса указать:
```
{
  "text": "string",
  "score": 1
}
```
* Ответ придёт в форме:

```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
13) Удалить отзыв по id (Права доступа: Автор отзыва, модератор или администратор.):
* Отправить DELETE-запрос http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/. 

14) Получить список всех комментариев к отзыву по id (Права доступа: Доступно без токена.):
* Отправить GET-запрос http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/ :
* Ответ придёт в форме:

```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```
15) Добавить новый комментарий для отзыва (Права доступа: Аутентифицированные пользователи.):
* Отправить POST-запрос http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/. В теле запроса указать:
```
{
  "text": "string"
}
```
* Ответ придёт в форме:

```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```
16) Получить комментарий для отзыва по id (Права доступа: Доступно без токена.):
* Отправить GET-запрос http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/ :
* Ответ придёт в форме:

```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```
17) Частично обновить комментарий к отзыву по id (Права доступа: Автор комментария, модератор или администратор.):
* Отправить PATCH-запрос http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/. В теле запроса указать:
```
{
  "text": "string"
}
```
* Ответ придёт в форме:

```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```
18)Удалить комментарий к отзыву по id (Права доступа: Автор комментария, модератор или администратор.):
* Отправить DELETE-запрос http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}//

