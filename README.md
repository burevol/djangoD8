<!-- TABLE OF CONTENTS -->
<details>
  <summary>Содержание</summary>
  <ol>
    <li>
      <a id="#о-проекте">О проекте</a>
    </li>
    <li>
      <a id="#Запуск">Запуск</a>
      <ul>
        <li><a id="#зависимости">Зависимости</a></li>
        <li><a id="#установка">Установка</a></li>
      </ul>
    </li>
    <li><a id="#Использование">Использование</a></li>
    <li><a id="#Контакты">Контакты</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## О проекте

Это учебный проект новостного сайта на базе фреймворка Django

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Запуск

### Зависимости
1. Python => 3.7
2. Docker => 20.10

### Установка
1. Клонировать репозиторий: ```git clone https://github.com/burevol/djangoD8```
2. Установить виртуальное окружение ```python -m venv venv```
3. Активировать виртуальное окружение ```.\venv\Scripts\activate```
4. Установить модули ```pip install -r .\requirements.txt```
5. Запустить BD Redis ```docker run --name my-redis -p 6379:6379 -d redis```


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Использование
1. Запустить worker Celery ```celery -A newsportal worker -l INFO```
2. Запустить worker для периодических задач ```celery -A newsportal worker -l INFO -B```
3. Запустить сайт ```python ./manage.py runserver```


<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTACT -->
## Контакты

Alexander Maximoff - alexum2013@yandex.ru

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)

<p align="right">(<a href="#top">back to top</a>)</p>
