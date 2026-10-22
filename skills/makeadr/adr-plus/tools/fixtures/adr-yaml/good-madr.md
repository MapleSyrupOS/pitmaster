---
status: accepted
date: 2026-05-01
decision-makers: Alice, Bob
consulted: Carol
informed: the whole team
---

# ADR-913 — Use a message queue between the importer and the indexer

## Context and Problem Statement

The importer outruns the indexer.

## Decision Drivers

* Throughput.

## Considered Options

* A queue.
* A shared table.

## Decision Outcome

Chosen option: "A queue", because it absorbs bursts.

### Consequences

* Good, bursts no longer drop records.

### Confirmation

A load test.

## More Information

None.
