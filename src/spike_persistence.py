import sqlite3
from datetime import datetime, timezone
from pathlib import Path

Path("data").mkdir(exist_ok=True)

conn = sqlite3.connect("data/spike.db")
conn.execute(
    "CREATE TABLE IF NOT EXISTS execucoes ("
    "id INTEGER PRIMARY KEY AUTOINCREMENT, "
    "executado_em TEXT NOT NULL)"
)
conn.execute(
    "INSERT INTO execucoes (executado_em) VALUES (?)",
    (datetime.now(timezone.utc).isoformat(),),
)
conn.commit()

total = conn.execute("SELECT COUNT(*) FROM execucoes").fetchone()[0]
print("Linhas na tabela execucoes:", total,)
conn.close()