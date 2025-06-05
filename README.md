### Тестовое задание: Платформа для обмена вещами на DRF с unit-тестами 🚀

- Ознакомиться с результатом можно по репозиторию или ссылке ниже:
```
barter-api.noobweer.ru/admin/ - админ-панель Django
barter-api.noobweer.ru/docs/ - документация по эндпоинтам
barter.noobweer.ru - фронтенд для взаимодействия и теста функционала
```
```
admin:88238823Admin - login:pass для авторизации в админ-панели и фронтенд
```

- Также прошу обратить внимание на фронтенд, он находится в отдельном репозитории и написан на Vue:
[Репозиторий фронтенда (barter-frontend)](https://github.com/noobweer/barter-frontend)

### **Установка и запуск на Windows**
- Клонируйте репозиторий
```bash
git clone https://github.com/noobweer/barter-backend.git
```
- Создайте виртуальное окружение и установите зависимости
```bash
python -m venv venv
venv\Scripts\activate
cd barter-backend
pip install -r requirements.txt
```
- Примените миграции, создайте суперпользователя и запускайте
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
- Запустить тесты можно данной командой:
```bash
python manage.py test ads.tests
```

