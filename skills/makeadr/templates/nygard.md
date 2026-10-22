# NNNN. The decision, as a short title

Date: YYYY-MM-DD

## Status

Proposed

## Context

The forces at play: technical, political, social and project-local. Describe them neutrally.

## Decision

What we will do, stated in full sentences in the active voice: "We will …".

## Consequences

What becomes easier or harder because of this decision, good and bad alike.

---

This layout follows Michael Nygard's 2011 article "Documenting Architecture Decisions". A later decision that
replaces this one gets its own record, and this one's Status becomes "Superseded by NNNN". `adr-index.py` reads
the line under `## Status`; `adr-check.py` checks only that it is present.
