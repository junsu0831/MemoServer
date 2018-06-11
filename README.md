# memo-server
메모 앱 서버의 소스코드 입니다.

## 설치 및 실행 방법
```
> git clone https://github.com/chjs/memo-server.git
> cd memo-server
> python -m venv myvenv
> myvenv\Scripts\activate
(myvenv) > python -m pip install --upgrade pip
(myvenv) > pip install -r requirements.txt
(myvenv) > python manage.py makemigrations memo
(myvenv) > python manage.py migrate
(myvenv) > python manage.py createsuperuser
(myvenv) > python manage.py runserver
```
