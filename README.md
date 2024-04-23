# **Phone auth with referral system**

Это проект, написанный на языках 

- Python 3.11

С использованием библиотек/фреймворков:
- Django 5.0.4
- Django REST framework 3.15.1
- PostgreSQL 
- Simplejwt 5.3.1

API для сервиса регистрации и авторизации пользователей по номеру телефона с отправкой временных кодов. 
Также присутствует реферальная система. 


## **Установка**
### Для установки проекта, следуйте инструкциям ниже:

**<p>1. Сделайте Fork этого репозитория. Репозиторий появится в ваших личных репозиториях на GitHub.</p>**

**1.1 Сделайте `git clone` форкнутого репозитория, чтобы получить репозиторий локально:**

**<p>2. Перейдите в папку с проектом.</p>**

**<p>3. Создайте и активируйте виртуальное окружение:</p>**

`python3 -m venv <имя_окружения>`

`source <название_вашего_окружения>/bin/activate`

**<p>4. Установите зависимости проекта:</p>**

`pip install -r requirements.txt`

**<p>5. Создайте файл .env в корневой папке проекта (referral_sys/) и заполните данные для настройки проекта из 
файла .env.sample:</p>**

```ini
/.env/

# Django setting
DJANGO_SECRET_KEY=django secret key

# PostgreSQL connection
POSTGRES_DB=db name
POSTGRES_USER=psql username
POSTGRES_PASSWORD=psql password
POSTGRES_HOST=host for db
POSTGRES_PORT=port for db
```

**<p>6. Примените миграции:</p>**

`python manage.py migrate`

**<p>7. Воспользуйтесь командой для установки русского языка:</p>**

`python manage.py compilemessages`

**<p>8. ЗАПУСК BACKEND-ЧАСТИ: Запустите сервер:</p>**

`python manage.py runserver` или настройте запуск Django сервера в настройках.


Таким образом можно работать с backend-частью локально для отладки.

После запуска сервера. Вы сможете перейти на сайт с документацией http://127.0.0.1:8000/api/schema/redoc/ 
(если сервер запущен локально), и начать пользоваться всеми API методами проекта. 

Также вы можете схему данных .yaml файлом по адресу http://127.0.0.1:8000/api/schema/ (если сервер запущен локально).

### Либо с помощью Docker
**<p>1. Создайте файл .env в корневой папке проекта (referral_sys/) и заполните данные для настройки проекта из 
файла .env.sample:</p>**
```ini
/.env.docker/

# Django setting
DJANGO_SECRET_KEY=your django secret key

# PostgreSQL connection
POSTGRES_DB=database name
POSTGRES_USER=postgresql username
POSTGRES_PASSWORD=postgresql password
POSTGRES_HOST=container name
POSTGRES_PORT=your port
```

**<p>2. ЗАПУСК BACKEND-ЧАСТИ:: Воспользуйтесь командами:</p>**

`docker compose build` для создания оптимального билда проекта.

`docker compose up` для запуска docker compose контейнера.


## **Использование**
#### На проекте регистрация новых пользователей API происходит автоматически. 
Когда пользователь вводит номер телефона ему отправляется SMS код для подтверждения авторизации и если до этого такого
пользователя не было, то он записывается в базу данных.
- POST-запрос: http://localhost/api/phone/login/ (обязательный параметр - номер телефона "phone"). Служит для записи в БД и отправки 
СМС кода.
- POST-запрос: http://localhost/api/phone/confirm/ (обязательный параметр - код из СМС "pass_code"). Служит для подтверждения авторизации и 
генерации JWT токена для дальнейших действий требующих авторизации.
- GET-запрос: http://localhost/api/profile/ (обязательный параметр - Bearer-токен). Служит для просмотра профиля пользователя,
где он может посмотреть список своих рефералов, введенный реферальный код.
- POST-запрос: http://localhost/api/profile/ (обязательный параметр - реферальный код "referral_code"). Служит для того, 
чтобы пользователь мог ввести реферальный код в своем профиле.

  
Автор
VictorVolkov7 - vektorn1212@gmail.com