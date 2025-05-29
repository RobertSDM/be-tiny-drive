run:	
	python main.py
create_tables:
	python -m scripts.create_db
env-run:
	$(CURDIR)/venv/Scripts/activate.bat && make run
	
mock-db:
	$(CURDIR)/venv/Scripts/activate.bat && \
	docker container run --rm --name mock_db -p 5432:5432 -e POSTGRES_PASSWORD=password -d postgres:16-alpine && \
	timeout 3 && \
	alembic upgrade head && \
	python -m app.scripts.db_load_mock_data