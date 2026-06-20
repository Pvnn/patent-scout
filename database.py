from agno.db.sqlite import SqliteDb

# Initialize SqliteDb for session and history storage.
# Centralized here to avoid circular imports across agents, workflows, and app.py
sqlite_db = SqliteDb(session_table="sessions", db_file="db/sessions.db")
