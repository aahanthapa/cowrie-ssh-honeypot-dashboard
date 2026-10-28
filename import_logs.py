import json
import sqlite3
import hashlib

log_file = "var/log/cowrie/cowrie.json"
db_file = "cowrie.db"

connection = sqlite3.connect(db_file)
cursor = connection.cursor()

with open(log_file, "r") as file:
	for line in file:
		event = json.loads(line)

		event_hash = hashlib.sha256(
			json.dumps(event, sort_keys=True) .encode()
		).hexdigest()

		cursor.execute("""
			INSERT OR IGNORE INTO events
			(timestamp, event_type, src_ip, username, command, event_hash)
			VALUES (?, ?, ?, ?, ?, ?)
		""", (
			event.get("timestamp"),
			event.get("eventid"),
			event.get("src_ip"),
			event.get("username"),
			event.get("input"),
			event_hash
		))

connection.commit()

print("Cowrie logs imported successfully!")
print("Total events", cursor.execute(
	"SELECT COUNT(*) FROM events"
).fetchone()[0])

connection.close()
