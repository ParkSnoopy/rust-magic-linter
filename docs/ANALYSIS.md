# Rust AI Agent Guardrails: Complete Analysis Report

## Executive Summary

This report analyzes 7 GitHub repositories that use strict Clippy linting for AI-assisted Rust development. The key finding: **these repos represent a complete "AI Agent Stack"** with different components serving distinct roles.

| Role | Repository | Purpose |
|------|------------|---------|
| **Brain/Runtime** | OpenAgentsInc/openagents | Autonomous agent OS with DSPy, crypto identity, Plan 9 filesystem |
| **Hands/Terminal** | Mockapapella/tenex | Git worktree isolation for parallel agent execution |
| **Eyes/Sensors** | djinn09/CytoScnPy | Static analysis via MCP for agents to self-verify code |
| **Workflow** | john-agentic-ai-tools/crush | "Constitution" pattern + spec-driven TDD |
| **Visualization** | deltartificial/cawd | Read-only TUI to verify agent file edits |
| **Plugin System** | mkroman/zeta | Modular IRC bot showing pedantic + ergonomic balance |
| **Low-level Safety** | danthedaniel/BF-JIT | JIT compiler showing lints for unsafe code wrapping |

---

## The Three Breakthrough Patterns

### 1. The Constitution Pattern (Crush)

**What:** A markdown file (`.specify/memory/constitution.md`) that defines immutable laws for the codebase.

**Why it matters:** Instead of repeating constraints in every prompt, the AI agent reads this file once and respects it as "supreme law."

**Example rules:**
- "Performance First"
- "Test-First Development (NON-NEGOTIABLE)"
- "No unwrap() in production code"

### 2. The "No Cheating" Lint (Cawd)

**What:** `allow_attributes = "deny"` in Cargo.toml

**Why it matters:** AI models often bypass errors by adding `#[allow(clippy::...)]`. This lint makes that impossible - the AI must actually fix the code.

```toml
[lints.clippy]
allow_attributes = "deny"  # AI cannot silence warnings
```

### 3. Worktree Isolation (Tenex)

**What:** Using `git worktree` to give each agent its own filesystem sandbox.

**Why it matters:** Agents can run destructive commands (`rm -rf`, conflicting edits) without affecting the main repo or other agents.

---

## Key Insights by Repository

### OpenAgentsInc/openagents
- **Most comprehensive lint config** with async safety additions
- **DSPy in Rust** - typed LLM signatures with compiler enforcement
- **Plan 9 filesystem** - agents interact via file read/write (LLMs are good at this)
- Key lints: `await_holding_lock`, `print_stdout`, `exit`, `mem_forget`

### Mockapapella/tenex
- **Strictest lint levels** - uses `deny` for all groups including nursery
- **Worktree isolation** - brilliant sandboxing without containers
- **90% test coverage enforcement** in CI
- Comprehensive `[lints.rust]` section beyond clippy

### djinn09/CytoScnPy
- **MCP server** - agents can call the linter as a tool
- **Taint analysis** - agents can self-verify for security vulnerabilities
- **PGO builds** - makes tools fast enough for interactive use
- Key contribution: `clippy.toml` complexity thresholds

### john-agentic-ai-tools/crush
- **The Constitution pattern** - game-changer for AI workflows
- **Spec-driven scripts** - enforces plan→task→implement workflow
- **cargo-deny** for supply chain security

### deltartificial/cawd
- **`allow_attributes = "deny"`** - the "no cheating" rule
- **Read-only TUI** - purpose-built for verifying agent output

### mkroman/zeta
- **Balanced pedantic** - shows how to be strict but ergonomic
- **Plugin architecture** - good pattern for extensible agent tools

### danthedaniel/BF-JIT
- **AI-written code** - AArch64 backend by Claude 3 Opus
- **Safe wrapper for unsafe** - strict lints protect the boundaries

---

## Architectural Recommendations

### The Complete AI Agent Stack

```
┌─────────────────────────────────────────────────────────────┐
│                    YOUR RUST PROJECT                        │
├─────────────────────────────────────────────────────────────┤
│  CONSTITUTION.md         │  Immutable laws for AI           │
│  Cargo.toml [lints]      │  Compiler-enforced guardrails    │
│  clippy.toml             │  Complexity thresholds           │
│  .cargo/deny.toml        │  Supply chain security           │
├─────────────────────────────────────────────────────────────┤
│                    RUNTIME LAYER                            │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │ Tenex   │  │OpenAgent│  │CytoScnPy│  │  Cawd   │        │
│  │ (Hands) │  │ (Brain) │  │ (Eyes)  │  │ (View)  │        │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │
│       │            │            │            │              │
│       ▼            ▼            ▼            ▼              │
│  Git Worktree   DSPy Sigs    MCP Server   TUI Display      │
│  Isolation      + Runtime    for Analysis  for Verify      │
└─────────────────────────────────────────────────────────────┘
```

### Recommended Workflow

1. **Create CONSTITUTION.md** - Define your project's immutable laws
2. **Copy the lint config** to your workspace Cargo.toml
3. **Add clippy.toml** for complexity thresholds
4. **Run continuously:**
   ```bash
   cargo fmt && cargo clippy --workspace --all-targets -- -D warnings && cargo test
   ```
5. **Use Tenex** for parallel agent execution with worktree isolation
6. **Use Cawd** to visually verify agent edits in real-time

---

## Lint Category Analysis

### Must-Have: Panic Safety
```toml
unwrap_used = "deny"     # No Option::unwrap()
expect_used = "deny"     # No Option::expect()
panic = "deny"           # No explicit panic!()
panic_in_result_fn = "deny"  # Result functions shouldn't panic
```

### Must-Have: Meta-Linting
```toml
allow_attributes = "deny"  # THE "NO CHEATING" RULE
allow_attributes_without_reason = "deny"  # Or require reasons
```

### Must-Have: Code Hygiene
```toml
dbg_macro = "deny"       # No debug leftovers
todo = "deny"            # No incomplete code
unimplemented = "deny"   # No stubs
print_stdout = "deny"    # Use tracing
print_stderr = "deny"    # Use tracing
```

### Should-Have: Async Safety
```toml
await_holding_lock = "deny"  # Prevents deadlocks
large_futures = "warn"       # Stack safety
```

### Should-Have: Process Safety
```toml
exit = "deny"            # Libraries shouldn't exit
mem_forget = "deny"      # Prevents leaks
```

### Nice-to-Have: Performance
```toml
large_stack_arrays = "warn"
large_types_passed_by_value = "warn"
```

---

## Conclusion

The viral tweet from @notnotstorm revealed a powerful pattern: **use Rust's static analysis as AI guardrails**. But the 7 repositories we analyzed show this is just the beginning.

The most impactful discoveries:
1. **The Constitution pattern** (Crush) - codify laws, not just lints
2. **The "no cheating" lint** (Cawd) - `allow_attributes = "deny"`
3. **Worktree isolation** (Tenex) - safe sandboxing without containers
4. **MCP integration** (CytoScnPy) - let agents verify their own code

**The future of AI coding is not about making AI smarter - it's about making the environment smarter.** Strict linting turns "taste" into compiler errors, letting AI agents learn the rails through fast feedback loops.

---

## Research Files

Raw research notes are available in the [research/](research/) directory:
- `gemini1-tenex-openagents.md` - Analysis of Tenex and OpenAgents
- `gemini2-cytoscnpy.md` - Analysis of CytoScnPy
- `gemini3-others.md` - Analysis of Crush, Zeta, BF-JIT, and Cawd
