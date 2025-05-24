cd backend
python3 -m app.scripts.create_user

alembic revision --autogenerate -m "create XXX table"
alembic upgrade head