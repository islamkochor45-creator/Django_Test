# Django Internet Shops API

Это backend-приложение интернет-магазина на Django REST Framework. Проект позволяет:

- просматривать каталог товаров и категории;
- регистрироваться и использовать JWT-аутентификацию;
- работать с корзиной и избранным;
- создавать заказы;
- создавать и подтверждать платежи;
- оставлять отзывы к товарам.

## Основная структура проекта

- apps/catalog — категории и товары
- apps/cart — корзина покупателя
- apps/wishlist — избранное
- apps/orders — заказы
- apps/payments — платежи
- apps/reviews — отзывы
- apps/users — регистрация и пользователи
- DjangoInternetShops — настройки проекта и общие URL

## Базовые адреса

- http://localhost:8000/ — основной сервер
- http://localhost:8000/admin/ — админ-панель Django
- http://localhost:8000/api/docs/ — Swagger UI документация
- http://localhost:8000/api/schema/ — OpenAPI схема

## Аутентификация

Проект использует JWT через SimpleJWT.

- POST /api/token/ — получить access/refresh токены
- POST /api/token/refresh/ — обновить access токен

Для защищённых запросов нужно передавать заголовок:

```http
Authorization: Bearer <token>
```

## API-маршруты

### Каталог

- GET /api/categories/ — список категорий
- GET /api/products/ — список товаров с поиском/фильтрами/сортировкой
- GET /api/products/<id>/ — подробности товара

### Регистрация

- POST /api/auth/register/ — регистрация пользователя

### Корзина

- GET /api/cart/ — получить корзину текущего пользователя
- POST /api/cart/add/ — добавить товар в корзину
- DELETE /api/cart/item/<id>/ — удалить товар из корзины

### Избранное

- GET /api/wishlist/ — получить избранное
- POST /api/wishlist/add/ — добавить товар в избранное
- DELETE /api/wishlist/remove/<id>/ — удалить из избранного

### Заказы

- GET /api/orders/ — мои заказы
- POST /api/orders/create/ — создать заказ из корзины
- GET /api/orders/<id>/ — детали заказа
- GET /api/orders/admin/all/ — все заказы (только для администратора)
- PATCH /api/orders/admin/status/<id>/ — изменить статус заказа (только для администратора)

### Платежи

- POST /api/payment/create/ — создать платеж по заказу
- POST /api/payment/confirm/<id>/ — подтвердить оплату

### Отзывы

- GET /api/reviews/product/<product_id>/ — отзывы к товару
- POST /api/reviews/create/ — создать отзыв

## Как это работает по шагам

1. Пользователь регистрируется или получает JWT-токен.
2. Через /api/products/ можно посмотреть товары.
3. Товар добавляется в корзину через /api/cart/add/.
4. Из корзины создаётся заказ через /api/orders/create/.
5. Для заказа создаётся платеж через /api/payment/create/.
6. После подтверждения оплаты заказ переводится в обработку.
7. Пользователь может оставить отзыв через /api/reviews/create/.

## Запуск проекта

### Через Docker

```bash
docker compose up --build
```

Сервер будет доступен на:

- http://localhost:8000/

### Через Django

```bash
python manage.py migrate
python manage.py runserver
```

## Примечание

Проект уже настроен для работы с PostgreSQL в Docker и для отдачи статических медиа-файлов товаров.
