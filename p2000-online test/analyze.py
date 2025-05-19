import json
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict

data = "berichten.json"
with open(data, "r") as f:
    berichten = json.load(f)

messages_per_week = defaultdict(int)
for bericht in berichten:
    date_str = bericht["datetime"].split(" ")[0]
    date_obj = datetime.strptime(date_str, "%d-%m-%Y")
    year, week, _ = date_obj.isocalendar()
    week_label = f"Week {week:02d}"
    messages_per_week[week_label] += 1

weeks = sorted(messages_per_week.keys())
if len(weeks) > 2:
    weeks = weeks[1:-1]
counts = [messages_per_week[week] for week in weeks]

plt.figure(figsize=(10, 5))
plt.plot(weeks, counts, marker='o')
plt.xlabel('Week')
plt.ylabel('Aantal berichten')
plt.title(f'Berichten per week in {year}')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("output.jpg", format="jpg")
