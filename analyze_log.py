import json
from collections import Counter

log_file = "var/log/cowrie/cowrie.json"

events =  Counter()
ips = Counter()
usernames = Counter()
commands = Counter()

with open(log_file, "r") as file:
	for line in file:
		event = json.loads(line)

		event_type = event.get("eventid")
		events[event_type] += 1

		if event_type == "cowrie.session.connect":
			ips[event.get("src_ip")] =+ 1

		if event_type in ["cowrie.login.success", "cowrie.login.failed"]:
			usernames[event.get("username")] += 1
		if event_type == "cowrie.command.input":
			commands[event.get("input")] += 1

print("\n=== Cowrie Honeypot Analysis ===")

print("\nEvent Counts:")
for name, count in events.items():
	print(f"{name}: {count}")

print("\nIP Addresses:")
for ip, count in ips.items():
	print(f"{ip}: {count}")

print("\nUsernames Attempted:")
for username, count in usernames.items():
	print(f"{username}: {count}")

print("\nCommands Entered:")
for command, count in commands.items():
	print(f"{command}: {count}")
