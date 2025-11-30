# ИНСТРУКЦИЯ ПО РАЗВЕРТЫВАНИЮ

## Вариант 1: Быстрый старт (для ознакомления)

### Шаг 1: Распакуйте архив
```bash
unzip equipment_catalog.zip
cd equipment_catalog
```

### Шаг 2: Установите зависимости
```bash
pip install -r requirements.txt
```

### Шаг 3: Запустите сервер
```bash
python manage.py runserver
```

### Шаг 4: Откройте браузер
```
http://127.0.0.1:8000/
```

### Данные для входа в админку:
- **URL:** http://127.0.0.1:8000/admin/
- **Логин:** admin
- **Пароль:** admin123

**База данных и примерные данные уже настроены!**

---

## Вариант 2: Чистая установка

### Шаг 1: Установите Python
Убедитесь, что установлен Python 3.8 или выше:
```bash
python --version
```

### Шаг 2: Создайте виртуальное окружение (рекомендуется)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Шаг 3: Установите зависимости
```bash
pip install -r requirements.txt
```

### Шаг 4: Удалите старую БД (если есть)
```bash
# Windows
del db.sqlite3

# Linux/Mac
rm db.sqlite3
```

### Шаг 5: Создайте новую БД
```bash
python manage.py migrate
```

### Шаг 6: Создайте суперпользователя
```bash
python manage.py createsuperuser
```
Введите желаемые логин, email и пароль.

### Шаг 7: (Опционально) Загрузите примерные данные
```bash
python manage.py shell < load_sample_data.py
```

### Шаг 8: Запустите сервер
```bash
python manage.py runserver
```

---

## Вариант 3: Production развертывание

### Для Ubuntu/Debian сервера:

#### 1. Подготовка сервера
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx postgresql
```

#### 2. Создайте пользователя БД PostgreSQL
```bash
sudo -u postgres psql
CREATE DATABASE equipment_catalog;
CREATE USER catalog_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE equipment_catalog TO catalog_user;
\q
```

#### 3. Настройте проект
```bash
cd /var/www/equipment_catalog
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

#### 4. Измените settings.py
```python
# Замените базу данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'equipment_catalog',
        'USER': 'catalog_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Безопасность
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']
SECRET_KEY = 'your-new-secret-key'  # Сгенерируйте новый!

# Статические файлы
STATIC_ROOT = '/var/www/equipment_catalog/static/'
```

#### 5. Соберите статику и примените миграции
```bash
python manage.py collectstatic
python manage.py migrate
python manage.py createsuperuser
```

#### 6. Настройте Gunicorn
Создайте файл `/etc/systemd/system/equipment_catalog.service`:
```ini
[Unit]
Description=Equipment Catalog
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/equipment_catalog
ExecStart=/var/www/equipment_catalog/venv/bin/gunicorn \
    --workers 3 \
    --bind 127.0.0.1:8000 \
    equipment_catalog.wsgi:application

[Install]
WantedBy=multi-user.target
```

#### 7. Настройте Nginx
Создайте файл `/etc/nginx/sites-available/equipment_catalog`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /var/www/equipment_catalog;
    }

    location /media/ {
        root /var/www/equipment_catalog;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### 8. Активируйте сайт
```bash
sudo ln -s /etc/nginx/sites-available/equipment_catalog /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl start equipment_catalog
sudo systemctl enable equipment_catalog
```

---

## Проверка установки

### Тест 1: Доступность сайта
Откройте браузер и перейдите на http://127.0.0.1:8000/

### Тест 2: Админка
Войдите в http://127.0.0.1:8000/admin/

### Тест 3: Добавление оборудования
1. Создайте цех через админку
2. Добавьте площадку
3. Создайте тип оборудования
4. Добавьте оборудование через веб-интерфейс

### Тест 4: Поиск
1. Перейдите в каталог
2. Попробуйте поиск
3. Используйте фильтры

---

## Решение проблем

### Ошибка: "ModuleNotFoundError: No module named 'django'"
```bash
pip install django
```

### Ошибка: "no such table"
```bash
python manage.py migrate
```

### Ошибка 403 при загрузке файлов
Проверьте права на директорию media/:
```bash
chmod -R 755 media/
```

### Сервер не запускается
Проверьте, не занят ли порт:
```bash
# Linux/Mac
lsof -i :8000

# Windows
netstat -ano | findstr :8000
```

---

## Резервное копирование

### Бэкап базы данных (SQLite)
```bash
cp db.sqlite3 db.sqlite3.backup
```

### Бэкап базы данных (PostgreSQL)
```bash
pg_dump equipment_catalog > backup.sql
```

### Бэкап медиа-файлов
```bash
tar -czf media_backup.tar.gz media/
```

---

## Обновление системы

1. Сделайте бэкап
2. Обновите код
3. Примените миграции:
```bash
python manage.py migrate
```
4. Соберите статику:
```bash
python manage.py collectstatic
```
5. Перезапустите сервер

---

## Контакты поддержки

При возникновении проблем:
- Проверьте README.md
- Изучите логи Django
- Обратитесь к документации Django

---

**Удачной работы!**
