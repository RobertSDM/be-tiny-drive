run:	
	@python main.py
create_tables:
	@python -m utils.db_create_tables
env-run:
	"$(CURDIR)/venv/Scripts/activate.bat" && make run