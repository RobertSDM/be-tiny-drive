run:	
	cls && @python main.py
create_tables:
	cls && @python -m utils.db_create_tables
env-run:
	"$(CURDIR)/venv/Scripts/activate.bat" && make run