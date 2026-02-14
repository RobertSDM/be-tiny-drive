.PHONY: run create_tables mock-db env-run run-mock

run:	
	./venv/bin/python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 4500 --log-level info

run-mock: mock-db run

create-tables:
	.\venv\Scripts\python.exe -m scripts.create_db
	
env-run:
	$(CURDIR)/venv/Scripts/activate.bat && make run
	
mock-db:
	$(CURDIR)/venv/Scripts/activate.bat && \
	docker container run --rm --name mock_db -p 5432:5432 -e POSTGRES_PASSWORD=password -d postgres:16-alpine && \
	timeout 3 && \
	alembic upgrade head && \
	.\venv\Scripts\python.exe -m app.scripts.load_mock_data

.PHONY: dump-dep
dump-dep:
	.\venv\Scripts\python.exe -m pip freeze > requirements.txt