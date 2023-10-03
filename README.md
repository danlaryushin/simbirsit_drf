## **Стек технологий**
![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![image](https://img.shields.io/badge/rest%20framework-DBD7D2?style=for-the-badge&logo=django&logoColor=FF2400)
![image](https://img.shields.io/badge/sqlite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

# Волжский Янтарь
Проект на базе Django REST Framework, сделанный для магазина "Волжский Янтарь".

В проекте реализован API для интернет-магазина:
* Регистрация пользователей
* Авторизация по токену
* Возможность добавления товаров в избранное/корзину
* При оформлении заказа товары из корзины снимаются с продажи, а также в модели продукта полю `owner` присваивается имя покупателя.


Также реализована удобная админ-зона с различными возможностями:
* Создание, редактирование и публикация товаров
* Создание новых коллекций товаров
* Просмотр оформленных онлайн-заказов
, создавать новые коллекции, а также просматривать оформленные онлайн заказы.

## Инструкция по локальному запуску проекта
Склонируйте репозиторий
```
git clone https://github.com/danlaryushin/simbirsit_drf.git
```
Создайте виртуальное окружение
```
cd simbirsit
```
```
python -m venv venv
```
Установите зависимости
```
pip install -r requirements.txt
```
Перейдите в папку с файлом manage.py и запустите проект
```
cd simbirsit
```
```
python manage.py runserver
```

Документация к API будет доступна по адресу http://127.0.0.1:8000/swagger/

## Админ зона ##
Для доступа к админ-панели создайте суперпользователя
```
python manage.py createsuperuser
```
Далее введите Username, Email и пароль, после чего нужно авторизоваться по адресу http://127.0.0.1:8000/admin/

## Планы по доработке

* Настройка почтового сервера
* Написание фронтенда
* Контейнеризация с использованием Docker
* Deploy проекта на боевой сервер

## Автор ##
[Даниил Ларюшин](https://github.com/danlaryushin) - Разработчик
