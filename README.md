# rust-magic-linter

> "How to get your agents to follow Rust best practices: enforce pedantic
> clippy lints in your Cargo.toml so that every best practice is required
> by default." — [@notnotstorm](https://x.com/notnotstorm)

Strict Clippy lint configurations for AI-assisted Rust development. Turn "taste" into compiler errors.

## Why?

- AI agents write code fast but make mistakes
- Rust's static analysis catches issues at compile time
- Strict Clippy lints = "guardrails" that teach agents the codebase rules
- The `allow_attributes = "deny"` lint prevents AI from silencing warnings with `#[allow(...)]`

## Quick Start

### Option 1: Copy-paste (simplest)

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

### Option 2: Download full config

```bash
# Download the complete lint configuration
curl -sL https://raw.githubusercontent.com/vicnaum/rust-magic-linter/main/templates/cargo-lints.toml >> Cargo.toml

# Optional: download clippy.toml for complexity thresholds
curl -sL https://raw.githubusercontent.com/vicnaum/rust-magic-linter/main/templates/clippy.toml -o clippy.toml
```

### Option 3: Shell script

```bash
curl -sL https://raw.githubusercontent.com/vicnaum/rust-magic-linter/main/scripts/install.sh | bash
```

Or with a specific preset:

```bash
curl -sL https://raw.githubusercontent.com/vicnaum/rust-magic-linter/main/scripts/install.sh | bash -s -- minimal
```

### Option 4: Claude Code skill

If you use [Claude Code](https://claude.ai/claude-code), just ask:

> "Add rust-magic-linter to this project"

## Presets

| Preset | Description | Use Case |
|--------|-------------|----------|
| **minimal** | Just panic guards (`unwrap`, `expect`, `panic`, `allow_attributes`) | Quick safety net |
| **standard** | The viral tweet config + async safety | Most projects |
| **maximum** | Everything at deny level (Tenex-style) | Maximum strictness |

See the [presets/](presets/) directory for the full configurations.

## The Key Lints Explained

### The Guardrails (Critical for AI)

| Lint | Level | Why |
|------|-------|-----|
| `unwrap_used` | deny | Forces proper error handling instead of panics |
| `expect_used` | deny | Same as above - no hidden panics |
| `panic` | deny | No explicit panics allowed |
| `allow_attributes` | deny | **The "no cheating" rule** - AI can't silence warnings |
| `dbg_macro` | deny | No debug leftovers in production |
| `todo` | deny | No incomplete code |

### Async Safety

| Lint | Level | Why |
|------|-------|-----|
| `await_holding_lock` | deny | Prevents deadlocks when holding locks across `.await` |
| `large_futures` | warn | Catches huge stack allocations in async code |

### Output Control

| Lint | Level | Why |
|------|-------|-----|
| `print_stdout` | deny | Use `tracing` for structured logging |
| `print_stderr` | deny | Same - proper logging over println debugging |

## Additional Configuration

### clippy.toml

Put this in your project root to set complexity thresholds:

```toml
cognitive-complexity-threshold = 15
type-complexity-threshold = 200
too-many-lines-threshold = 100
doc-valid-idents = ["LLM", "AI", "API", "CLI", "TUI", "AST", "MCP"]
```

### cargo-deny (supply chain security)

Put `deny.toml` in `.cargo/` to prevent problematic dependencies:

```toml
[licenses]
allow = ["MIT", "Apache-2.0", "BSD-3-Clause", "ISC", "Zlib", "CC0-1.0"]

[bans]
multiple-versions = "warn"
wildcards = "deny"

[advisories]
vulnerability = "deny"
unmaintained = "warn"
```

## The Three Breakthrough Patterns

This project analyzed 7 repositories using strict linting for AI development. Key discoveries:

### 1. The Constitution Pattern

Create a `CONSTITUTION.md` defining immutable laws for your codebase. AI reads it once and respects it. See [templates/CONSTITUTION.md](templates/CONSTITUTION.md).

### 2. The "No Cheating" Lint

```toml
allow_attributes = "deny"
```

This single line prevents AI from bypassing errors with `#[allow(clippy::...)]`.

### 3. Worktree Isolation

Use `git worktree` to give each agent its own filesystem sandbox - destructive commands can't affect the main repo.

## Credits & Research

This project is based on analysis of lint configurations from leading AI-assisted Rust projects:

- [@notnotstorm](https://x.com/notnotstorm) - The original viral tweet
- [OpenAgentsInc/openagents](https://github.com/OpenAgentsInc/openagents) - DSPy in Rust, async safety lints
- [Mockapapella/tenex](https://github.com/Mockapapella/tenex) - Maximum strictness, worktree isolation
- [john-agentic-ai-tools/crush](https://github.com/john-agentic-ai-tools/crush) - Constitution pattern
- [deltartificial/cawd](https://github.com/deltartificial/cawd) - The "no cheating" lint
- [djinn09/CytoScnPy](https://github.com/djinn09/CytoScnPy) - MCP integration, complexity thresholds
- [mkroman/zeta](https://github.com/mkroman/zeta) - Balanced pedantic config
- [danthedaniel/BF-JIT](https://github.com/danthedaniel/BF-JIT) - AI-written safe wrappers

See [docs/CREDITS.md](docs/CREDITS.md) for full attribution and [docs/ANALYSIS.md](docs/ANALYSIS.md) for the complete research.

## License

MIT - See [LICENSE](LICENSE)
