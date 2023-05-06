# Middle test

## Quick start(Linux)
1. $ cd 
2. $ mkdir midtest
3. $ cd midtest
4. $ git clone https://gitlab.com/pavelepanov/midtest
5. $ cd midtest
5. $ python3 -m venv venv
6. $ source venv/bin/activate
7. $ pip install -r requirements.txt
8. $ cd src
9. $ uvicorn main:app --reload
10. Open http://127.0.0.1:8000/docs
10. Open new terminal
11. $ cd midtest/midtest
12. $ source venv/bin/activate
13. $ cd src
14. You must make a .env file with REDIS_HOST REDIS_PORT and DB
15. (DB=0)
14. $ celery -A tasks.tasks:celery worker --loglevel=INFO

*U can use it with redis-cli for checking info about tasks.*