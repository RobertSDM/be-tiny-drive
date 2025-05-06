run:	
	cls && python main.py
create_tables:
	cls && python -m scripts.create_db
env-run:
	"$(CURDIR)/venv/Scripts/activate.bat" && make run