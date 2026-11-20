# X02 — When does a retry prevent recovery?

| Field | Value |
| --- | --- |
| ID / revision / date | X02 · 1.0 · 20 November 2026 |
| Prerequisites | S05 queues, S06 reliability and C03 useful capacity |
| Capability developed | Decide whether to spend a remaining deadline and a shared capacity budget on one more attempt. |
| Evidence | XR03 and XR04. Primary passages and scope below. |
| Experiment | Deterministic queue and deadline checks in the [worked companion](SDE_X02_answers.md). |

## Why a quiet minute can contain a busy second

Marc Brooker describes an operational pattern on Amazon EBS and AWS Lambda. Clients running periodic jobs lined up near clock boundaries. Looking at per-second traffic exposed bursts obscured by longer averages. The team worked with clients to stagger periodic work and reported processing the same work with less server capacity. The report gives no universal percentage saving. For periodic work they used a repeatable offset per host so recurring patterns remained diagnosable. For retrying clients, the same paper describes randomizing the backoff delay. [AWS Builders’ Library, “Jitter,” final five paragraphs](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

This case gives us two different engineering decisions. Spreading a fixed batch changes *when* its work arrives. Retrying a timed-out call can also change *how much* work arrives. A timeout tells the caller that it stopped waiting. The original attempt may still occupy a worker. Ask which of those two quantities is causing the problem before tuning a delay.

## Trace a recovery window

Imagine a retrieval service that can finish 100 equal-cost attempts per second. At the start of recovery it has 40 queued attempts. Every second 90 new requests arrive. An upstream client also has a pool of previously timed-out requests eligible for retry. Treat arrivals as a batch before service, assume a work-conserving queue and retain unfinished work. These values are invented. [S05](SDE_S05.md) explains why real requests can have very different costs.

With no extra attempts, ten slots per second drain old work. With 15 retries per second, the queue grows by five even though fresh traffic alone is below capacity. Compare end-of-second queue lengths.

| Extra attempts admitted each second | Start | After 1 s | After 2 s | After 3 s | After 4 s |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0 | 40 | 30 | 20 | 10 | 0 |
| 5 | 40 | 35 | 30 | 25 | 20 |
| 10 | 40 | 40 | 40 | 40 | 40 |
| 15 | 40 | 45 | 50 | 55 | 60 |

Compute each cell as `max(0, previous queue + fresh attempts + retries − capacity)`. At exactly ten retries per second the queue stops growing, yet never drains. To clear all 40 within eight seconds under constant rates, reserve five slots per second for recovery. That leaves at most five for retries. This is a budget for the entire dependency in this model. Giving each of ten callers its own five attempts per second would permit fifty.

The table holds retry arrivals fixed to isolate their cost. In a running service the loop can feed itself. More attempts lengthen the queue. More callers hit their deadline and resubmit, increasing arrivals again. Google SRE documents this pattern and recommends both per-request attempt limits and an aggregate retry budget. Its numeric overload example illustrates the mechanism. [Google SRE, chapter 22, “Retries”](https://sre.google/sre-book/addressing-cascading-failures/)

## Decide at the caller

Suppose an AI assistant has 800 ms to return evidence. Its first retrieval attempt times out at 560 ms. It needs 150 ms for another retrieval and 60 ms to assemble a response, using invented deterministic costs. Before backoff it has 240 ms left, of which 30 ms can be spent waiting. A 40 ms backoff puts the earliest modeled finish at 810 ms. The request should stop even if the dependency has spare retry tokens. Conversely, satisfying the deadline cannot create backend capacity. In production the stage times are distributions. Measure the joint end-to-end outcome under load and reserve slack for scheduling.

A workable policy has one layer own the retry. It checks whether the failure is transient, whether a repeated operation is safe, whether enough deadline remains, and whether the shared budget admits it. It propagates the remaining deadline downstream and records both attempts against one logical request. Two layers that each allow three attempts can send nine attempts to the bottom service on the all-fail path. Jitter spreads those attempts. A cap limits their number.

For a read-only retrieval, duplicate computation may be tolerable. For an agent issuing a billable or externally visible action, a missing reply can leave an unknown outcome. Reconcile using the operation identity and the provider's actual guarantees before reissuing it. See [C01](SDE_C01.md). Even read-only inference can be expensive if the original generation keeps decoding. Verify how cancellation propagates and when accelerator capacity is actually released.

## Practice

1. With 40 queued attempts, 90 fresh arrivals and capacity 100, find the largest constant integer retry rate that drains the queue in five seconds. Show why the next integer fails.
2. A retry needs 150 ms plus 60 ms for response assembly. Find the latest time at which it can start under an inclusive 800 ms deadline. What changes if the first attempt timed out at 610 ms?
3. An SDK and gateway each permit two retries after an initial attempt. Bound downstream attempts and choose which layer should own retries for this workload. Identify the information it needs.
4. Design a replay for the retrieval endpoint. Which metric would convince you that retries are helping users? Which measurement would make you stop them?

## Evidence and deployment questions

| Source | Inspected locator | Application boundary |
| --- | --- | --- |
| XR03 · Marc Brooker, AWS | [Timeouts, retries, and backoff with jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/), “Jitter,” EBS/Lambda periodic workload account, and “Retries and backoff” | Production experience with burst timing and guidance for retries. The model's capacity and deadlines are original assumptions. |
| XR04 · Mike Ulrich, Google | [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/), “Retries” and “Queue Management” | Describes retry feedback, aggregate limits and waiting costs. The service in our trace is hypothetical. |

Before choosing a budget, measure per-dependency headroom during recovery, attempts still running after a timeout, actual retries inside SDKs, and the fraction of logical requests delivering supported evidence by the deadline. An improving attempt success rate can coexist with fewer users receiving timely results.
