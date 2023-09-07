# Проект «Фудграм»
«Фудграм» — сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Пользователям сайта также доступен сервис «Список покупок». Он позволияет создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

### Технологии:

- Python
- Django
- Django Rest Framework
- Docker
- Gunicorn
- NGINX
- PostgreSQL
- Yandex.Cloud
- Continuous Integration
- Continuous Deployment

### Проект состоит из следующих страниц: 
- главная
- страница рецепта
- страница пользователя
- страница подписок
- избранное
- список покупок
- создание и редактирование рецепта

Документация к API доступна по адресу http://localhost/api/docs/ после локального запуска проекта

### Как развернуть проект локально:
Cклонировать реппозиторий:
```
git clone https://github.com/evkasonka/foodgram-project-react.git
cd foodgram/backend
```
Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
source env/bin/activate
```
Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
Выполнить миграции:
```
python manage.py migrate
```
Заполняем базу тестовыми данными ингредиентов:
```
python manage.py upload_csv
```
Перейдя а папку infra, создайте файл .env по образцу:
```
cd infra
touch .env
```
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY='секретный ключ Django'
```

затем, находясь в папке infra, выполните команду 
```
docker-compose up
```
При выполнении этой команды контейнер frontend, описанный в docker-compose.yml, подготовит файлы, необходимые для работы фронтенд-приложения, а затем прекратит свою работу.
По адресу http://localhost будут доступен проект, а по адресу http://localhost/api/docs/ — спецификация API. 

### Как развернуть проект на удаленном сервере:
Cклонировать реппозиторий:
```
git clone https://github.com/evkasonka/foodgram-project-react.git
```
Установить на сервере docker, docker-compose:
```
sudo apt install docker.io
sudo apt install docker-compose
```

В github actions Settings → Secrets в вашем репозитории добавьте:
```
DOCKER_PASSWORD             # пароль от Docker Hub
DOCKER_USERNAME             # логин Docker Hub
HOST                        # публичный IP сервера
USER                        # имя пользователя на сервере
SSH_KEY                     # приватный ssh-ключ
PASSPHRASE                  # ssh-ключ защищен паролем
TELEGRAM_TO                 # ID телеграм-аккаунта для отправки сообщения
TELEGRAM_TOKEN              # токен бота
```

По команде git push в ветку master будет происходить:
- Проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8)      #tests
- Сборка и доставка докер-образов backend       #build_and_push_to_docker_hub
  и frontend на Docker Hub      #build_frontend_and_push_to_docker_hub
- Разворачивание проекта на удаленном сервере       #deploy
- Отправка уведомления пользователю в Телеграм      #send_massage

Создать суперпользователя и заполнить тестоовыми данными базу:
```
sudo docker compose exec backend python manage.py createsuperuser
sudo docker compose exec backend python manage.py upload_csv
```