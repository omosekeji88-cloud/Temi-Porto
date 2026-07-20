"""Build the finance fraud dashboard from the Kaggle raw CSV.

Expected raw file:
    data/raw/creditcard.csv

Download source:
    https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
"""

from pathlib import Path
import csv
import html
import json
from collections import defaultdict

PROJECT_DIR = Path(__file__).resolve().parents[1]
RAW_CSV = PROJECT_DIR / "data" / "raw" / "creditcard.csv"
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"


def amount_bucket(amount):
    if amount < 10:
        return "$0-$10"
    if amount < 50:
        return "$10-$50"
    if amount < 100:
        return "$50-$100"
    if amount < 250:
        return "$100-$250"
    if amount < 1000:
        return "$250-$1,000"
    return "$1,000+"


def write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def analyse_transactions(raw_csv):
    total = fraud = legitimate = 0
    total_amount = fraud_amount = legitimate_amount = 0.0
    max_amount = max_fraud_amount = 0.0
    hourly = defaultdict(lambda: {"transactions": 0, "fraud": 0, "amount": 0.0, "fraud_amount": 0.0})
    buckets = defaultdict(lambda: {"transactions": 0, "fraud": 0, "amount": 0.0, "fraud_amount": 0.0})
    fraud_sample = []

    with raw_csv.open(newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            total += 1
            amount = float(row["Amount"])
            is_fraud = int(row["Class"]) == 1
            hour = int((float(row["Time"]) % 86400) // 3600)
            bucket = amount_bucket(amount)

            total_amount += amount
            max_amount = max(max_amount, amount)
            hourly[hour]["transactions"] += 1
            hourly[hour]["amount"] += amount
            buckets[bucket]["transactions"] += 1
            buckets[bucket]["amount"] += amount

            if is_fraud:
                fraud += 1
                fraud_amount += amount
                max_fraud_amount = max(max_fraud_amount, amount)
                hourly[hour]["fraud"] += 1
                hourly[hour]["fraud_amount"] += amount
                buckets[bucket]["fraud"] += 1
                buckets[bucket]["fraud_amount"] += amount
                fraud_sample.append({
                    "time_seconds": row["Time"],
                    "hour_of_day": hour,
                    "amount": round(amount, 2),
                    "class": 1,
                })
            else:
                legitimate += 1
                legitimate_amount += amount

    hourly_rows = []
    for hour in range(24):
        stats = hourly[hour]
        transactions = stats["transactions"]
        fraud_count = stats["fraud"]
        hourly_rows.append({
            "hour_of_day": hour,
            "transactions": transactions,
            "fraud_transactions": fraud_count,
            "fraud_rate_percent": round((fraud_count / transactions * 100) if transactions else 0, 4),
            "transaction_amount": round(stats["amount"], 2),
            "fraud_amount": round(stats["fraud_amount"], 2),
        })

    bucket_rows = []
    for bucket in ["$0-$10", "$10-$50", "$50-$100", "$100-$250", "$250-$1,000", "$1,000+"]:
        stats = buckets[bucket]
        transactions = stats["transactions"]
        fraud_count = stats["fraud"]
        bucket_rows.append({
            "amount_bucket": bucket,
            "transactions": transactions,
            "fraud_transactions": fraud_count,
            "fraud_rate_percent": round((fraud_count / transactions * 100) if transactions else 0, 4),
            "transaction_amount": round(stats["amount"], 2),
            "fraud_amount": round(stats["fraud_amount"], 2),
        })

    kpis = {
        "total_transactions": total,
        "fraud_transactions": fraud,
        "legitimate_transactions": legitimate,
        "fraud_rate_percent": round(fraud / total * 100, 4),
        "total_transaction_amount": round(total_amount, 2),
        "fraud_transaction_amount": round(fraud_amount, 2),
        "average_transaction_amount": round(total_amount / total, 2),
        "average_fraud_amount": round(fraud_amount / fraud, 2),
        "average_legitimate_amount": round(legitimate_amount / legitimate, 2),
        "max_transaction_amount": round(max_amount, 2),
        "max_fraud_amount": round(max_fraud_amount, 2),
        "dataset_source": "Kaggle: mlg-ulb/creditcardfraud",
        "dataset_license": "DbCL-1.0",
    }

    fraud_sample = sorted(fraud_sample, key=lambda item: item["amount"], reverse=True)[:20]
    return kpis, hourly_rows, bucket_rows, fraud_sample


def create_dashboard(kpis, hourly_rows, bucket_rows, fraud_sample):
    bars = []
    for row in hourly_rows:
        height = max(row["fraud_rate_percent"] * 42, 3)
        bars.append(
            f'<div class="bar-wrap"><div class="bar-count">{row["fraud_transactions"]}</div>'
            f'<div class="bar" style="height:{height:.1f}px"></div>'
            f'<div class="bar-label">{row["hour_of_day"]}</div></div>'
        )

    risk_rows = []
    for row in bucket_rows:
        width = min(row["fraud_rate_percent"] * 30, 100)
        risk_rows.append(
            f'<div class="risk-row"><strong>{html.escape(row["amount_bucket"])}</strong>'
            f'<div class="track"><div class="fill" style="width:{width:.1f}%"></div></div>'
            f'<span>{row["fraud_rate_percent"]:.3f}%</span></div>'
        )

    bucket_table = "".join(
        f'<tr><td>{html.escape(row["amount_bucket"])}</td><td>{row["transactions"]:,}</td>'
        f'<td>{row["fraud_transactions"]:,}</td><td>{row["fraud_rate_percent"]:.3f}%</td></tr>'
        for row in bucket_rows
    )
    sample_table = "".join(
        f'<tr><td>{row["hour_of_day"]:02d}:00</td><td>${row["amount"]:,.2f}</td><td>Fraud</td></tr>'
        for row in fraud_sample[:8]
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Finance Fraud Analytics Dashboard</title>
  <style>
    :root {{ --bg:#07111f; --panel:#101d31; --panel-2:#13263f; --text:#f7fbff; --muted:#9fb4d0; --teal:#4fe0c6; --gold:#ffcf5a; --red:#ff6b7a; --line:rgba(255,255,255,.12); }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; font-family:Arial, Helvetica, sans-serif; background:var(--bg); color:var(--text); letter-spacing:0; }}
    main {{ width:min(1180px, calc(100% - 32px)); margin:0 auto; padding:42px 0; }}
    header {{ display:grid; grid-template-columns:1.2fr .8fr; gap:28px; align-items:end; margin-bottom:28px; }}
    h1 {{ margin:0 0 14px; font-size:clamp(32px, 5vw, 58px); line-height:1; }}
    p {{ color:var(--muted); line-height:1.65; }}
    .source {{ text-align:right; }}
    .grid {{ display:grid; grid-template-columns:repeat(4, 1fr); gap:16px; margin-bottom:16px; }}
    .panel {{ background:linear-gradient(180deg, var(--panel), var(--panel-2)); border:1px solid var(--line); padding:22px; box-shadow:0 18px 42px rgba(0,0,0,.24); }}
    .kpi span {{ display:block; color:var(--muted); font-size:13px; font-weight:700; text-transform:uppercase; }}
    .kpi strong {{ display:block; margin-top:10px; font-size:30px; color:var(--teal); }}
    .wide {{ grid-column:span 2; }}
    .full {{ grid-column:1 / -1; }}
    h2 {{ margin:0 0 16px; font-size:22px; }}
    .chart {{ display:flex; align-items:end; gap:7px; min-height:220px; padding-top:14px; border-bottom:1px solid var(--line); }}
    .bar-wrap {{ flex:1; display:flex; flex-direction:column; align-items:center; gap:8px; }}
    .bar {{ width:100%; min-height:3px; background:linear-gradient(180deg, var(--red), var(--gold)); border-radius:7px 7px 0 0; }}
    .bar-count {{ font-size:11px; color:var(--muted); min-height:13px; }}
    .bar-label {{ font-size:10px; color:var(--muted); }}
    .horizontal {{ display:grid; gap:12px; }}
    .risk-row {{ display:grid; grid-template-columns:92px 1fr 74px; gap:12px; align-items:center; }}
    .track {{ height:14px; background:rgba(255,255,255,.08); border-radius:999px; overflow:hidden; }}
    .fill {{ height:100%; background:linear-gradient(90deg, var(--teal), var(--gold), var(--red)); }}
    table {{ width:100%; border-collapse:collapse; margin-top:8px; }}
    th, td {{ padding:12px 10px; border-bottom:1px solid var(--line); text-align:left; }}
    th {{ color:var(--muted); text-transform:uppercase; font-size:12px; }}
    .note {{ color:var(--muted); font-size:13px; margin-top:14px; }}
    @media (max-width:860px) {{ header, .grid {{ grid-template-columns:1fr; }} .wide, .full {{ grid-column:auto; }} .source {{ text-align:left; }} }}
  </style>
</head>
<body>
  <main>
    <header>
      <section>
        <h1>Finance Fraud Analytics Dashboard</h1>
        <p>Interactive portfolio dashboard built from the Kaggle credit card fraud dataset. It highlights class imbalance, fraud-rate patterns, transaction value risk and high-value fraudulent transactions.</p>
      </section>
      <section class="source">
        <p><strong>Dataset:</strong> Kaggle mlg-ulb/creditcardfraud<br><strong>Focus:</strong> BI reporting, fraud monitoring, analyst storytelling</p>
      </section>
    </header>
    <section class="grid">
      <div class="panel kpi"><span>Total transactions</span><strong>{kpis["total_transactions"]:,}</strong></div>
      <div class="panel kpi"><span>Fraud transactions</span><strong>{kpis["fraud_transactions"]:,}</strong></div>
      <div class="panel kpi"><span>Fraud rate</span><strong>{kpis["fraud_rate_percent"]:.3f}%</strong></div>
      <div class="panel kpi"><span>Fraud amount</span><strong>${kpis["fraud_transaction_amount"]:,.0f}</strong></div>
      <div class="panel wide"><h2>Fraud Rate by Hour of Day</h2><div class="chart">{''.join(bars)}</div><p class="note">Bar height shows fraud-rate percentage by transaction hour. Numbers above bars show fraud transaction count.</p></div>
      <div class="panel wide"><h2>Fraud Risk by Amount Bucket</h2><div class="horizontal">{''.join(risk_rows)}</div><p class="note">The dataset is highly imbalanced, so small changes in fraud rate matter.</p></div>
      <div class="panel wide"><h2>Amount Bucket Summary</h2><table><thead><tr><th>Bucket</th><th>Transactions</th><th>Fraud</th><th>Fraud Rate</th></tr></thead><tbody>{bucket_table}</tbody></table></div>
      <div class="panel wide"><h2>Highest-Value Fraud Sample</h2><table><thead><tr><th>Hour</th><th>Amount</th><th>Status</th></tr></thead><tbody>{sample_table}</tbody></table></div>
      <div class="panel full"><h2>Analyst Summary</h2><p>The dataset contains {kpis["total_transactions"]:,} transactions but only {kpis["fraud_transactions"]:,} confirmed fraud cases, producing a fraud rate of {kpis["fraud_rate_percent"]:.3f}%. This makes the project useful for showing BI work on imbalanced data, where percentage rates, segmented views and high-risk transaction monitoring are more informative than raw counts alone.</p></div>
    </section>
  </main>
</body>
</html>
"""


def main():
    if not RAW_CSV.exists():
        raise SystemExit(f"Missing raw dataset: {RAW_CSV}")

    kpis, hourly_rows, bucket_rows, fraud_sample = analyse_transactions(RAW_CSV)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    (PROCESSED_DIR / "fraud_kpis.json").write_text(json.dumps(kpis, indent=2))
    write_csv(PROCESSED_DIR / "hourly_fraud_summary.csv", hourly_rows, ["hour_of_day", "transactions", "fraud_transactions", "fraud_rate_percent", "transaction_amount", "fraud_amount"])
    write_csv(PROCESSED_DIR / "amount_bucket_risk.csv", bucket_rows, ["amount_bucket", "transactions", "fraud_transactions", "fraud_rate_percent", "transaction_amount", "fraud_amount"])
    write_csv(PROCESSED_DIR / "high_value_fraud_sample.csv", fraud_sample, ["time_seconds", "hour_of_day", "amount", "class"])
    (PROJECT_DIR / "dashboard.html").write_text(create_dashboard(kpis, hourly_rows, bucket_rows, fraud_sample))
    print("Dashboard and processed files rebuilt successfully.")


if __name__ == "__main__":
    main()
