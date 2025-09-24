#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path
import random
import csv

CATEGORIES = ["Security", "Network", "Memory", "Storage", "Application", "Other"]

TEMPLATES = {
    "Security": ["Failed login for user={user} from ip={ip}", "Multiple 401s detected for user={user}"],
    "Network": ["Packet loss {pct}% to dest={ip}", "High latency {ms}ms to service={svc}"],
    "Memory": ["OOM killer invoked pid={pid}", "Container mem usage {mb}MB exceeds limit"],
    "Storage": ["Disk space {pct}% on mount={mnt}", "I/O error on device={dev}"],
    "Application": ["NullPointer at {svc}:{path}", "Timeout calling {svc} ({ms}ms)"],
    "Other": ["Heartbeat from {svc}", "Job {job} completed"]
}

def rand_ip():
    return ".".join(str(random.randint(1, 254)) for _ in range(4))

def synth_row(i: int) -> dict:
    cat = random.choices(CATEGORIES, weights=[0.15,0.2,0.15,0.15,0.25,0.1])[0]
    tpl = random.choice(TEMPLATES[cat])
    msg = tpl.format(
        user=f"u{random.randint(1,999)}",
        ip=rand_ip(),
        pct=random.randint(1, 99),
        ms=random.randint(50, 3000),
        svc=f"svc-{random.randint(1,20)}",
        pid=random.randint(100, 9999),
        mb=random.randint(256, 4096),
        mnt=random.choice(["/","/var","/data"]),
        dev=random.choice(["nvme0n1","sda1","dm-0"]),
        path=f"/api/v1/{random.randint(1,9)}",
        job=f"job-{random.randint(100,999)}",
    )
    ts = (datetime(2024,1,1) + timedelta(seconds=i*5)).isoformat()
    return {
        "timestamp": ts,
        "host": f"h{random.randint(1,50)}",
        "facility": random.choice(["auth","kern","daemon","app"]),
        "severity": random.choice(["INFO","WARN","ERROR"]),
        "service": f"svc-{random.randint(1,20)}",
        "component": random.choice(["api","worker","db","ingress"]),
        "message": msg,
        "category": cat,
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="data/raw/synthetic/logs.csv")
    ap.add_argument("--n", type=int, default=5000)
    args = ap.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rows = [synth_row(i) for i in range(args.n)]
    with out_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {len(rows)} rows to {out_path}")

if __name__ == "__main__":
    main()


