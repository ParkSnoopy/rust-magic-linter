# rust-magic-linter

> "How to get your agents to follow Rust best practices: enforce pedantic clippy lints in your Cargo.toml so that every best practice is required by default."
> — [@notnotstorm](https://x.com/notnotstorm)

**Strict Clippy lint configurations for AI-assisted Rust development.** Turn "taste" into compiler errors.

---

## Quick Start

### Using Claude Code (Recommended)

If you use [Claude Code](https://claude.ai/claude-code), just say:

```
Add rust-magic-linter to this project
```

Claude will ask which preset you want and set everything up.

**To install the skill permanently:**

```bash
# Create skills directory if it doesn't exist
mkdir -p ~/.claude/skills

# Download the skill
curl -sL https://raw.githubusercontent.com/vicnaum/rust-magic-linter/main/skill/SKILL.md \
  -o ~/.claude/skills/rust-magic-linter.md
```

Then use `/rust-magic-linter` or `/rust-magic-linter standard` in any Rust project.

---

### Copy-Paste (5 seconds)

Add this to your `Cargo.toml`:

```toml
[lints.clippy]
pedantic = { level = "warn", priority = -1 }
unwrap_used = "deny"
expect_used = "deny"
panic = "deny"
allow_attributes = "deny"
dbg_macro = "deny"
todo = "deny"
print_stdout = "deny"
print_stderr = "deny"
```

---

### Shell Script (interactive)

```bash
curl -sL https://raw.githubusercontent.com/vicnaum/rust-magic-linter/main/scripts/install.sh | bash
```

Or specify a preset directly:

```bash
# Options: minimal, standard, maximum
curl -sL https://raw.githubusercontent.com/vicnaum/rust-magic-linter/main/scripts/install.sh | bash -s -- standard
```

---

### Download Full Config

```bash
# Get the complete lint configuration
curl -sL https://raw.githubusercontent.com/vicnaum/rust-magic-linter/main/templates/cargo-lints.toml >> Cargo.toml

# Get clippy.toml for complexity thresholds
curl -sL https://raw.githubusercontent.com/vicnaum/rust-magic-linter/main/templates/clippy.toml -o clippy.toml
```

---

## Presets

| Preset | What it does | Best for |
|--------|--------------|----------|
| **minimal** | Panic guards only: `unwrap`, `expect`, `panic`, `allow_attributes` | Quick safety net with minimal code changes |
| **standard** | Pedantic + async safety + output control | Most projects (recommended) |
| **maximum** | All lint groups at deny level | Maximum strictness, critical infrastructure |

See [`presets/`](presets/) for the full configurations.

---

## Why These Lints?

### The "No Cheating" Rule

```toml
allow_attributes = "deny"
```

This is the key insight: AI agents often bypass errors by adding `#[allow(clippy::...)]`. This lint makes that impossible—the AI must actually fix the code.

### Panic Prevention

| Lint | Why |
|------|-----|
| `unwrap_used` | Forces `?` or explicit error handling instead of panics |
| `expect_used` | Same—no hidden panics |
| `panic` | No explicit `panic!()` calls |
| `panic_in_result_fn` | Functions returning `Result` shouldn't panic internally |

### Async Safety

| Lint | Why |
|------|-----|
| `await_holding_lock` | Prevents deadlocks when holding `MutexGuard` across `.await` |
| `large_futures` | Catches huge stack allocations in async code |

### Code Hygiene

| Lint | Why |
|------|-----|
| `dbg_macro` | No debug leftovers |
| `todo` | No incomplete code markers |
| `print_stdout` | Use `tracing`, not `println!` |

---

## Additional Files

### clippy.toml

Complexity thresholds (put in project root):

```toml
cognitive-complexity-threshold = 15
type-complexity-threshold = 200
too-many-lines-threshold = 100
doc-valid-idents = ["LLM", "AI", "API", "CLI", "TUI", "AST", "MCP"]
```

### .cargo/deny.toml

Supply chain security with [cargo-deny](https://github.com/EmbarkStudios/cargo-deny):

```toml
[licenses]
allow = ["MIT", "Apache-2.0", "BSD-3-Clause", "ISC", "Zlib", "CC0-1.0"]

[bans]
wildcards = "deny"

[advisories]
vulnerability = "deny"
```

### CONSTITUTION.md

A markdown file defining immutable laws for your codebase—AI reads it once and respects it as "supreme law". See [`templates/CONSTITUTION.md`](templates/CONSTITUTION.md).

---

## The Philosophy

> "Coding in Rust means that the agents can't sneeze without being smacked in the face by the compiler."
> — [@Mockapapella](https://x.com/Mockapapella)

**The future of AI coding is not about making AI smarter—it's about making the environment smarter.** Strict linting turns "taste" into compiler errors, letting AI agents learn the rails through fast feedback loops.

This project analyzed 7 repositories using strict linting for AI development and extracted the best patterns:

1. **The Constitution Pattern** — Codify laws, not just lints
2. **The "No Cheating" Lint** — `allow_attributes = "deny"`
3. **Worktree Isolation** — Safe sandboxing with `git worktree`

---

## Credits

Based on analysis of lint configurations from:

- [OpenAgentsInc/openagents](https://github.com/OpenAgentsInc/openagents) — Async safety lints
- [Mockapapella/tenex](https://github.com/Mockapapella/tenex) — Maximum strictness
- [john-agentic-ai-tools/crush](https://github.com/john-agentic-ai-tools/crush) — Constitution pattern
- [deltartificial/cawd](https://github.com/deltartificial/cawd) — The "no cheating" lint
- [djinn09/CytoScnPy](https://github.com/djinn09/CytoScnPy) — Complexity thresholds
- [mkroman/zeta](https://github.com/mkroman/zeta) — Balanced pedantic config
- [danthedaniel/BF-JIT](https://github.com/danthedaniel/BF-JIT) — AI-written safe wrappers

See [`docs/CREDITS.md`](docs/CREDITS.md) for full attribution and [`docs/ANALYSIS.md`](docs/ANALYSIS.md) for the complete research.

---

## License

MIT — See [LICENSE](LICENSE)
