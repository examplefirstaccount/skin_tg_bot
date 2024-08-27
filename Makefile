generate:
	alembic revision --message="$(NAME)" --autogenerate

migrate:
	alembic upgrade head

# sudo service redis-server start - to start redis server