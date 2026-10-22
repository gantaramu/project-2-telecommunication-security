import csv
import os
import re
import matplotlib.pyplot as plt

os.makedirs("evidence", exist_ok=True)

with open("evidence/https-test.txt", encoding="utf-8") as f:
    report = f.read()

routes = ["/login/", "/dashboard/", "/"]
statuses = []

for route in routes:
    pattern = (
        r"=== GET " + re.escape(route)
        + r" ===(.*?)(?=\n=== GET |\n=== TLS CERTIFICATE ===|\Z)"
    )
    match = re.search(pattern, report, re.S)
    if not match:
        raise SystemExit(f"Missing test result for {route}")

    status = re.search(r"HTTP_STATUS=(\d{3})", match.group(1))
    if not status:
        raise SystemExit(f"Missing HTTP status for {route}")

    statuses.append(int(status.group(1)))

with open("evidence/https-status-summary.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["endpoint", "http_status", "interpretation"])
    writer.writerow(["/login/", statuses[0], "Login page response"])
    writer.writerow(["/dashboard/", statuses[1], "Unauthenticated dashboard response"])
    writer.writerow(["/", statuses[2], "Root path response"])

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(routes, statuses)
ax.set_title("Project 2: HTTPS Endpoint Response Codes")
ax.set_xlabel("Tested endpoint")
ax.set_ylabel("HTTP status code")
ax.set_ylim(0, max(statuses) + 70)
ax.grid(axis="y", alpha=0.25)
ax.bar_label(bars, padding=3)
fig.tight_layout()

fig.savefig("evidence/https-status-codes.png", dpi=180)
fig.savefig("evidence/https-status-codes.pdf")
plt.close(fig)

print("Graph and CSV created from the recorded test results.")
for route, status in zip(routes, statuses):
    print(f"{route}: HTTP {status}")
