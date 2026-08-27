---
name: a-architecture
description: 'Use when designing, reviewing, or documenting the Data Finance pipeline architecture, layer boundaries, or data contracts. Trigger phrases: architecture, pipeline design, medallion layers, contracts, new data source.'
---

# A - Architecture

## When to Use
- Designing a new pipeline or data source
- Reviewing structural changes across Bronze/Silver/Gold
- Defining or updating data contracts

## Procedure
1. Understand business objective and current architecture.
2. Map impacted layers, files, and contracts.
3. Propose or review the design with explicit acceptance criteria.
4. Document assumptions, risks, and pending decisions.

## Standards
- Preserve the existing layered architecture.
- No hardcoded local paths or credentials.
- Document trade-offs before implementation.
