---
name: g_testing
description: 'Use when creating or reviewing tests, regression coverage, or validation for the Data Finance pipeline. Trigger phrases: test, pytest, regression, coverage, validation.'
---

# G - Testing

## When to Use
- Adding tests for new or changed pipeline logic
- Reviewing regression coverage
- Validating a fix before considering it complete

## Procedure
1. Identify the impacted area and critical cases.
2. Validate current behavior before changing tests.
3. Add or adjust tests following existing conventions.
4. Run tests and report evidence of the result.

## Standards
- No success claims without a fresh passing run.
- Test real behavior, avoid mock-only assertions.
