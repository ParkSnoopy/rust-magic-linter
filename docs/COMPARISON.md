# Clippy Lint Configuration Comparison Report

## Executive Summary

This report compares the two most comprehensive Rust Clippy lint configurations found:

1. **OpenAgentsInc/openagents** - The "viral tweet" config from @notnotstorm (enhanced version)
2. **Mockapapella/tenex** - Self-described "every single restriction" config

**Finding:** Neither config is a strict superset of the other. Each has valuable lints the other is missing. The combined "best of both" config is what rust-magic-linter provides.

---

## Side-by-Side Comparison

### Lint Groups Enabled

| Lint Group | OpenAgentsInc | Tenex | Winner |
|------------|---------------|-------|--------|
| `all` | not set | **deny** | Tenex |
| `pedantic` | warn | **deny** | Tenex |
| `nursery` | not set | **deny** | Tenex |
| `cargo` | not set | **deny** | Tenex |

**Tenex wins on breadth** - it enables more lint groups and at `deny` level.

---

### Lints in OpenAgentsInc MISSING from Tenex

These are critical lints for AI agents that Tenex lacks:

```toml
# === ASYNC SAFETY (Critical for modern Rust) ===
await_holding_lock = "deny"      # Prevent deadlocks in async code
# This is CRITICAL - async code with locks is a common footgun

# === PROCESS/MEMORY SAFETY ===
exit = "deny"                    # Library code should never call exit()
mem_forget = "deny"              # std::mem::forget can leak resources

# === STACK/PERFORMANCE ===
large_stack_arrays = "warn"      # Catch huge stack allocations
panic_in_result_fn = "warn"      # Functions returning Result shouldn't panic

# === OUTPUT CONTROL ===
print_stdout = "deny"            # No println! in library code
print_stderr = "deny"            # No eprintln! in library code
# These force structured logging - important for production
```

**Why these matter for AI agents:**
- `await_holding_lock` - AI agents write async code frequently and this is a subtle bug
- `print_stdout/stderr` - Forces agents to use proper logging instead of debug prints
- `panic_in_result_fn` - Catches when agent writes `fn foo() -> Result<...>` but panics inside
- `exit` - Prevents agents from adding `std::process::exit()` which breaks composability

---

### Lints in Tenex MISSING from OpenAgentsInc

Tenex has these that the tweet config lacks:

```toml
# === ADDITIONAL LINT GROUPS ===
all = { level = "deny", priority = -1 }      # Base clippy lints
nursery = { level = "deny", priority = -1 }  # Experimental lints
cargo = { level = "deny", priority = -1 }    # Dependency/manifest hygiene

# === ALLOW ATTRIBUTE CONTROL ===
allow_attributes_without_reason = "deny"     # If you DO allow, document why
```

---

### Rust Lints (Beyond Clippy)

**Tenex has comprehensive `[lints.rust]` that OpenAgentsInc lacks:**

```toml
[lints.rust]
unsafe_code = "forbid"                    # No unsafe anywhere
warnings = "deny"                         # All warnings are errors
rust_2018_idioms = { level = "deny", priority = -1 }
future_incompatible = { level = "deny", priority = -1 }
nonstandard_style = { level = "deny", priority = -1 }
missing_docs = "deny"                     # Public items must be documented
missing_debug_implementations = "deny"    # Types must impl Debug
missing_copy_implementations = "deny"     # Types that can be Copy should be
non_ascii_idents = "forbid"               # No unicode in identifiers

[lints.rustdoc]
all = { level = "deny", priority = -1 }   # Documentation must be valid
```

**OpenAgentsInc only has:**
```toml
[workspace.lints.rust]
missing_docs = "allow"        # Explicitly allows missing docs
unexpected_cfgs = "allow"
```

---

## What's Unique to Each Config

### OpenAgentsInc's Unique Value
1. **Async-specific guards** (`await_holding_lock`, `exit`, `mem_forget`)
2. **Output control** (`print_stdout`, `print_stderr`)
3. **Stack safety** (`large_stack_arrays`, `panic_in_result_fn`)
4. **Curated pedantic overrides** with detailed explanations

### Tenex's Unique Value
1. **Full lint group coverage** (`all`, `nursery`, `cargo` at deny level)
2. **Comprehensive Rust lints** (beyond clippy)
3. **Documentation enforcement** (`missing_docs`, `missing_debug_implementations`)
4. **Stricter overall** (deny vs warn)

---

## Recommendation for AI Agent Workflows

For maximum AI guardrails, prioritize these categories:

### Must-Have (Prevent Bad Code)
```toml
unwrap_used = "deny"           # No hidden panics
expect_used = "deny"           # No hidden panics
panic = "deny"                 # No explicit panics
allow_attributes = "deny"      # Can't silence warnings
todo = "deny"                  # No incomplete code
unimplemented = "deny"         # No incomplete code
dbg_macro = "deny"             # No debug leftovers
```

### Should-Have (Prevent Subtle Bugs)
```toml
await_holding_lock = "deny"    # Async deadlock prevention
panic_in_result_fn = "deny"    # Logic error detection
exit = "deny"                  # Composability
mem_forget = "deny"            # Resource leak prevention
```

### Nice-to-Have (Code Quality)
```toml
print_stdout = "deny"          # Proper logging
print_stderr = "deny"          # Proper logging
nursery = "warn"               # Catch more issues
missing_docs = "warn"          # Force documentation
```

---

## The Combined Configuration

rust-magic-linter's `standard` preset combines the best of both:

- OpenAgentsInc's async safety and output control
- Tenex's comprehensive lint groups
- Carefully curated relaxations for practical use

See [skills/rust-magic-linter/assets/](../skills/rust-magic-linter/assets/) for the complete configurations.
