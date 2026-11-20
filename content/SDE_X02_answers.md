# X02 — Worked retry decisions and checks

[Return to the lesson](SDE_X02.md). Try drawing a single time axis for the user and a separate queue for the dependency. Each retry consumes space on both.

## 1. Leave capacity for recovery

Five seconds to drain 40 attempts requires eight net completions per second beyond incoming work. With ten spare slots, at most two can go to retries. At two the queue follows 40, 32, 24, 16, 8, 0. At three it ends at five. A shared per-second limit assumes equally expensive requests and enforcement over all callers. A token bucket with accumulated burst tokens can briefly exceed that rate. Account for burst size when making a five-second guarantee.

## 2. Use the user's deadline

Latest modeled retry start is 800 − 150 − 60 = 590 ms. At 560 ms, waiting exactly 30 ms consumes all slack. Waiting 31 misses the deadline. At 610 ms even immediate dispatch is 20 ms too late. If the caller can cheaply return a useful partial result, evaluate that separately under the same evidence requirement. Returning unsupported evidence would change the task.

## 3. Count attempts through the stack

Each layer permits three attempts including the first. The worst case sends nine downstream calls for one logical request. If the gateway knows the user's deadline, dependency budget and operation identity, it can own the retry and configure the SDK for one attempt. That reduces the modeled ceiling to three. A different layer can own it if that layer has equivalent information. Verify effective SDK and proxy settings by tracing a controlled failing request.

## 4. Test the outcome people receive

Replay the same arrival trace against policies with zero retries and a bounded retry budget. Include a short transient disconnect and a sustained capacity loss, then restore capacity with a queue still present. Count logical requests that return valid evidence by their deadline divided by all eligible original requests. Alongside it record attempts per logical request, outstanding work after cancellation, peak queue and time to drain. Control model version, output requirements and cache state. A retry that rescues the disconnect but prolongs overload calls for different treatment of those failure classes. Stop admitting retries when the added load prevents the queue from draining within the recovery target. Production thresholds require measured service curves and an agreed recovery target.

## Reproduce the arithmetic

The following checks use a deterministic teaching model with a single queue and inclusive deadline.

```python
def trace(retries, seconds):
    queue = 40
    history = [queue]
    for _ in range(seconds):
        queue = max(0, queue + 90 + retries - 100)
        history.append(queue)
    return history

assert [trace(r, 4)[-1] for r in (0, 5, 10, 15)] == [0, 20, 40, 60]
assert trace(2, 5) == [40, 32, 24, 16, 8, 0]
assert trace(3, 5)[-1] == 5
assert max(r for r in range(101) if trace(r, 8)[-1] == 0) == 5
assert 560 + 30 + 150 + 60 == 800
assert 560 + 31 + 150 + 60 > 800
assert 610 + 150 + 60 == 820
assert (1 + 2) ** 2 == 9
```

A complete answer explains both limits on another attempt, shows where the time goes, and states which real measurements would change the decision.
