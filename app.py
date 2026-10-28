from flask  import Flask, render_template
import sqlite3
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
	subprocess.run(
		["python3", "import_logs.py"],
		check=True
	)

	connection = sqlite3.connect("cowrie.db")
	cursor = connection.cursor()

	cursor.execute("SELECT COUNT(*) FROM events")
	total_events = cursor.fetchone()[0]

	cursor.execute("""
		SELECT COUNT(*) FROM events
		WHERE event_type = 'cowrie.session.connect'
	""")
	connections = cursor.fetchone()[0]

	cursor.execute("""
		SELECT COUNT(*) FROM events
		WHERE event_type IN (
			'cowrie.login.success',
			'cowrie.login.failed'
		)
	""")
	login_attempts = cursor.fetchone()[0]

	cursor.execute("""
		SELECT COUNT(*) FROM events
		WHERE event_type = 'cowrie.command.input'
	""")
	commands = cursor.fetchone()[0]

	cursor.execute("""
		SELECT src_ip, COUNT(*)
		FROM events
		WHERE event_type = 'cowrie.session.connect'
			AND src_ip IS NOT NULL
		GROUP BY src_ip
		ORDER BY COUNT(*) DESC
	""")
	ip_addresses = cursor.fetchall()

	cursor.execute("""
		SELECT username, COUNT(*)
		FROM events
		WHERE event_type IN (
				'cowrie.login.success',
				'cowrie.login.failed'
		)
			AND username IS NOT NULL
		GROUP BY username
		ORDER BY COUNT(*) DESC
	""")
	usernames = cursor.fetchall()

	cursor.execute("""
		SELECT command, COUNT(*)
		FROM events
		WHERE event_type = 'cowrie.command.input'
			AND command IS NOT NULL
		GROUP BY command
		ORDER BY COUNT(*) DESC
	""")
	entered_commands = cursor.fetchall()

	connection.close()

	return render_template(
		"dashboard.html",
		total_events=total_events,
		connections=connections,
		login_attempts=login_attempts,
		commands=commands,
		ip_addresses=ip_addresses,
		usernames=usernames,
		entered_commands=entered_commands
	)

if __name__ == "__main__":
	app.run(host="127.0.0.1", port=5000)
