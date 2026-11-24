# X08 — Worked point-in-time feature decisions

[Return to the lesson](SDE_X08.md). Every entity, timestamp, value and sample count below is invented. These checks teach reconstruction; they do not validate a production feature platform.

## 1. Apply both time predicates

For prediction time 10:00:

- E1 has `event_time=09:10 < 10:00` and `available_time=09:11 ≤ 10:00`, so include 40.
- E2 has `event_time=09:45 < 10:00` but `available_time=10:07 > 10:00`, so exclude 90.
- E3 has `event_time=10:05 > 10:00`, so exclude 30 regardless of its availability.

An event-time-only query returns `40 + 90 = 130`. The as-known feature is `40`. The leaked amount is 90. Running the warehouse query later does not move the prediction clock.

Before using `available_time`, prove it represents feature visibility to the serving path. An ingestion timestamp upstream of a delayed materialization can still leak.

## 2. Select the version known at the decision

At 10:00, only the `low` version is eligible because it became available at 08:02; the `high` correction is not available until 11:00. At 12:00, both versions are eligible and the latest revision is `high`.

Overwriting `low` with `high` destroys the availability history. A later backfill can know the current effective value but cannot prove what the 10:00 service returned. Preserve version rows or store the served feature vector/digest with the prediction.

This is a bitemporal selection: first restrict by knowledge time, then resolve the applicable effective-time version.

## 3. Make the window edges executable

For `[09:00, 10:00)` with the as-known predicate:

- E0 at 09:00 is included because the lower edge is inclusive: 10.
- E1 is included: 40.
- E2 is excluded because it was unavailable at prediction time.
- E-old at 08:59 is outside the event-time window.
- E3 is beyond the upper edge.

The sum is `10 + 40 = 50`. If the lower edge becomes exclusive, E0 is excluded and the sum becomes 40. That single bracket is part of the feature contract and needs a boundary fixture in both batch and serving implementations.

## 4. Count the union, then retain feature gates

Use inclusion–exclusion:

`120 + 25 − 5 = 140` predictions with at least one mismatch.

The global any-mismatch rate is `140 / 1,000 = 14%`. Language mismatch is 12%; count mismatch is 2.5%; their overlap is 0.5%.

A gate should be conjunctive: global mismatch under its limit **and** every critical feature/slice under its own limit. Report denominators for state, partner, device and model version. A low global value cannot purchase a breach in `prior_claim_count` for one state. Define exact matching for categories and tolerances for numeric values before inspecting the candidate pipeline.

Also compare missingness and reason codes. Equal aggregate mismatch can result from a harmless formatting normalization or a future-leaking late join.

## 5. Build a claim-triage training record

Use immutable `claim_id` plus `prediction_id`, with prediction time set when the triage decision is requested. Treat current-request fields separately from historical aggregates.

For mutable policy status, retain effective and availability/revision times and select the latest version available at prediction time. For repair invoices, store service/event time and feature-availability time; a late invoice must not enter an earlier claim’s training vector even if its service date predates the claim. Define windows such as `[prediction_time − 365 days, prediction_time)` and test the edges.

The fraud outcome can mature 30 days later as a label. It joins by claim/prediction identity but does not change the feature cutoff. Exclude or explicitly censor examples whose 30-day window is incomplete.

A useful hybrid is:

- log the exact served baseline vector, bundle version and request context;
- point-in-time backfill experimental features using both event and availability cutoffs;
- compare recomputed baseline features with the logged vector on overlapping rows;
- block training when critical-feature mismatch or missing logged coverage breaches a slice limit.

The evidence package needs source-delay distributions, correction history, online TTL/default rules, bundle/feature versions, label maturity, parity by state and a review path for mismatches. Logging failures must be measured; otherwise the retained sample may exclude the hardest traffic.

## Reproduce the temporal checks

The deterministic script implements the invented joins, window boundaries, mutable version and parity arithmetic.

```python
from datetime import datetime

def ts(value):
    return datetime.fromisoformat(f"2026-11-24T{value}:00")

prediction = ts("10:00")
events = [
    {"id": "E0", "amount": 10, "event": ts("09:00"), "available": ts("09:00")},
    {"id": "E-old", "amount": 100, "event": ts("08:59"), "available": ts("08:59")},
    {"id": "E1", "amount": 40, "event": ts("09:10"), "available": ts("09:11")},
    {"id": "E2", "amount": 90, "event": ts("09:45"), "available": ts("10:07")},
    {"id": "E3", "amount": 30, "event": ts("10:05"), "available": ts("10:05")},
]

event_only = sum(row["amount"] for row in events if row["id"] in {"E1", "E2"} and row["event"] < prediction)
as_known = sum(row["amount"] for row in events if row["id"] in {"E1", "E2", "E3"} and row["event"] < prediction and row["available"] <= prediction)
assert event_only == 130
assert as_known == 40

lower = ts("09:00")
window_rows = [row for row in events if lower <= row["event"] < prediction and row["available"] <= prediction]
assert {row["id"] for row in window_rows} == {"E0", "E1"}
assert sum(row["amount"] for row in window_rows) == 50

versions = [
    {"value": "low", "effective": ts("08:00"), "available": ts("08:02")},
    {"value": "high", "effective": ts("08:00"), "available": ts("11:00")},
]

def value_as_known(at):
    eligible = [row for row in versions if row["effective"] <= at and row["available"] <= at]
    return max(eligible, key=lambda row: row["available"])["value"]

assert value_as_known(ts("10:00")) == "low"
assert value_as_known(ts("12:00")) == "high"

language_mismatch = 120
count_mismatch = 25
both = 5
any_mismatch = language_mismatch + count_mismatch - both
assert any_mismatch == 140
assert any_mismatch / 1_000 == 0.14
assert count_mismatch / 1_000 == 0.025

print("PASS: availability cutoffs, window edges, corrections and parity checked")
```

A complete answer identifies the exact decision clock, distinguishes truth from knowability, versions mutable data, keeps label time separate and treats logged/recomputed disagreement as evidence rather than noise. These checks do not record learner mastery.
