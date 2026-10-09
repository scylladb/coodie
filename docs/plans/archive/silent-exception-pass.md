# Silent Exception Pass — Review & Fix Plan

> **Goal:** Audit every `except … pass` and overly broad exception handler in
> the coodie source tree, classify each as *problematic*, *acceptable*, or
> *test-only*, and fix the problematic cases so that no production-code
> exception is silently swallowed.

---

## Table of Contents

1. [Audit Results](#1-audit-results)
   - [1.1 Production Code (`src/`)](#11-production-code-src)
   - [1.2 Test Code (`tests/`)](#12-test-code-tests)
2. [Classification](#2-classification)
3. [Implementation Phases](#3-implementation-phases)
4. [Test Plan](#4-test-plan)
5. [References](#5-references)

---

## 1. Audit Results

Legend:
- ✅ **Acceptable** — exception handling is correct and intentional
- ❌ **Problematic** — exception is silently swallowed or handler is overly broad
- 🔧 **Test-only** — acceptable in test context but noted for completeness

### 1.1 Production Code (`src/`)

| # | File | Line | Pattern | Status |
|---|---|---|---|---|
| 1 | `src/coodie/schema.py` | 17 | `except Exception:` falls back to raw `__annotations__` | ❌ |
| 2 | `src/coodie/drivers/cassandra.py` | 28–29 | `except ImportError: pass` silently skips `dict_factory` setup | ❌ |
| 3 | `src/coodie/migrations/autogen.py` | 501–502 | `except ValueError: pass` skips non-numeric migration sequence parts | ✅ |
| 4 | `src/coodie/__init__.py` | 6–12 | `except PackageNotFoundError / ImportError` → version fallback chain | ✅ |
| 5 | `src/coodie/schema.py` | 210–211 | `except ImportError` → `annotationlib` fallback (Python 3.14+) | ✅ |
| 6 | `src/coodie/drivers/acsylla.py` | 238–239 | `except RuntimeError: current_loop = None` from `get_running_loop()` | ✅ |
| 7 | `src/coodie/drivers/python_rs.py` | 226–227 | `except RuntimeError: current_loop = None` from `get_running_loop()` | ✅ |

### 1.2 Test Code (`tests/`)

| # | File | Line | Pattern | Status |
|---|---|---|---|---|
| 8 | `tests/integration/test_migration_phase_b.py` | 60–61, 64–65 | `except Exception: pass` in table-drop cleanup | 🔧 |
| 9 | `tests/test_batch.py` | 107–108, 236–237 | `except ValueError: pass` catching expected error | 🔧 |

---

## 2. Classification

### Case 1 — `_cached_type_hints` catches bare `Exception` (❌ Problematic)

**File:** `src/coodie/schema.py:17`

```python
except Exception:
    return getattr(cls, "__annotations__", {})
```

**Problem:** `get_type_hints()` can fail with `NameError` (unresolved forward
refs), `AttributeError`, or `TypeError` — all recoverable.  However, catching
bare `Exception` also suppresses unexpected errors like `RecursionError`,
`RuntimeError`, or bugs in the typing machinery that should propagate.

**Fix:** Narrow to `(NameError, AttributeError, TypeError)` and add a
`logging.debug()` call so the fallback is observable.

### Case 2 — CassandraDriver silently skips `dict_factory` (❌ Problematic)

**File:** `src/coodie/drivers/cassandra.py:28–29`

```python
except ImportError:
    pass
```

**Problem:** If the CassandraDriver has a session, the `cassandra` package
must be installed.  A failure to import `cassandra.query.dict_factory` is
unexpected and silently degrades behaviour — `_rows_to_dicts()` must then
convert named-tuples at runtime, and any code path that assumes dict rows
could break.

**Fix:** Replace `pass` with a `logging.warning()` that tells the user the
session will fall back to named-tuple rows.

### Case 3 — Migration sequence `int()` parse (✅ Acceptable)

**File:** `src/coodie/migrations/autogen.py:501–502`

The `ValueError` is specific and expected: filenames that don't have a
numeric sequence component should simply be skipped.  No change needed.

### Cases 4–7 — Version fallback / asyncio loop detection (✅ Acceptable)

Standard Python patterns for optional imports and event-loop introspection.
No change needed.

### Cases 8–9 — Test cleanup / expected errors (🔧 Test-only)

Test teardown `except Exception: pass` is a common pattern for
best-effort cleanup.  Not worth changing but noted for awareness.

---

## 3. Implementation Phases

### Phase 1: Fix Problematic Silent Exception Passes (Priority: High) ✅ Done

**Goal:** Eliminate the two problematic silent-pass cases identified in the audit.

| Task | Description | Status |
|---|---|---|
| 1.1 | Narrow `_cached_type_hints` exception handler from bare `Exception` to `(NameError, AttributeError, TypeError)` and add `logging.debug()` | ✅ Done |
| 1.2 | Replace `except ImportError: pass` in `CassandraDriver.__init__` with `logging.warning()` | ✅ Done |
| 1.3 | Add unit tests for narrowed exception handling and warning emission | ✅ Done |

---

## 4. Test Plan

| Test Case | Phase | File |
|---|---|---|
| `_cached_type_hints` falls back on `NameError` (unresolved forward ref) | 1 | `tests/test_schema.py` |
| `_cached_type_hints` propagates `RecursionError` (no longer silenced) | 1 | `tests/test_schema.py` |
| `CassandraDriver.__init__` logs warning when `dict_factory` import fails | 1 | `tests/test_drivers.py` |

---

## 5. References

- Python `typing.get_type_hints` documentation
- PEP 563 — Postponed Evaluation of Annotations
- [ruff S110](https://docs.astral.sh/ruff/rules/try-except-pass/) — `try-except-pass` lint rule
