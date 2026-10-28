# rust-magic-linter

> "How to get your agents to follow Rust best practices: enforce pedantic clippy lints in your Cargo.toml so that every best practice is required by default."
> — [@notnotstorm](https://x.com/notnotstorm)

**Strict Clippy lint configurations for AI-assisted Rust development.** Turn "taste" into compiler errors.

---

## What is Clippy?

[Clippy](https://github.com/rust-lang/rust-clippy) is Rust's official linter—a tool that analyzes your code and catches common mistakes, suggests improvements, and enforces best practices.

**Install/Update Clippy:**
```bash
rustup component add clippy
```

**Run it:**
```bash
cargo clippy
```

The lint configurations in this repo tell Clippy *which* checks to enforce and at what severity level.

---

## Quick Start (4 ways to install)

### 1. Using Claude Code / Codex / Cursor (Recommended)

**Install the skill** (one-time setup):

```bash
git clone https://github.com/ParkSnoopy/rust-magic-linter.git
cp -r rust-magic-linter/skills/rust-magic-linter ~/.claude/skills/
# For Codex: ~/.codex/skills/
# For Cursor: ~/.cursor/skills/
```

**Then use it in any Rust project:**

```
/rust-magic-linter standard
```

Or just say "Add rust-magic-linter to this project" and it will ask which preset you want.

---

### 2. Copy-Paste (5 seconds)

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

### 3. Shell Script (interactive)

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/ParkSnoopy/rust-magic-linter/main/scripts/install.sh)"
```

Or specify a preset directly:

```bash
# Options: minimal, standard, maximum
bash -c "$(curl -fsSL https://raw.githubusercontent.com/ParkSnoopy/rust-magic-linter/main/scripts/install.sh)" -- standard
```

---

### 4. Download Config Directly

```bash
# Get the standard preset
curl -fsSL https://raw.githubusercontent.com/ParkSnoopy/rust-magic-linter/main/skills/rust-magic-linter/assets/standard/lint.toml >> Cargo.toml

# Get clippy.toml for complexity thresholds
curl -fsSL https://raw.githubusercontent.com/ParkSnoopy/rust-magic-linter/main/skills/rust-magic-linter/assets/standard/clippy.toml -o clippy.toml
```

---

## Presets


| Preset       | What it does                                                       | Best for                                    |
| ------------ | ------------------------------------------------------------------ | ------------------------------------------- |
| **minimal**  | Panic guards, lint-suppression checks, and debug cleanup | Quick safety net, minimal code changes      |
| **standard** | Pedantic + async safety + output control                           | Most projects (recommended)                 |
| **maximum**  | Broad lint groups at deny level; unsafe code forbidden             | Projects accepting strict policy constraints |


Each profile has its own `lint.toml`, `clippy.toml`, and `CONSTITUTION.md`: [minimal](skills/rust-magic-linter/assets/minimal/), [standard](skills/rust-magic-linter/assets/standard/), and [maximum](skills/rust-magic-linter/assets/maximum/).  
The constitutions follow [Google's Rust Style Guide](https://google.github.io/styleguide/rustguide.html), with explicit stricter profile overrides.  
See [configuration and installation](docs/CONFIGURATION.md) for workspace setup, existing configurations, and profile differences.  

For a fully documented reference config with explanations of every lint, see [`docs/cargo-lints-reference.toml`](docs/cargo-lints-reference.toml).

---

## Why These Lints?

### The "No Cheating" Rule

```toml
allow_attributes = "deny"
```

This rejects `#[allow(...)]` attributes during Clippy checks; agents must fix findings rather than suppress them.  

### Panic Prevention


| Lint                 | Why                                                     |
| -------------------- | ------------------------------------------------------- |
| `unwrap_used`        | Forces `?` or explicit error handling instead of panics |
| `expect_used`        | Same—no hidden panics                                   |
| `panic`              | No explicit `panic!()` calls                            |
| `panic_in_result_fn` | Functions returning `Result` shouldn't panic internally |


### Async Safety


| Lint                 | Why                                                          |
| -------------------- | ------------------------------------------------------------ |
| `await_holding_lock` | Flags synchronous lock guards held across `.await` in standard and maximum |
| `large_futures`      | Flags oversized futures in maximum                          |


### Code Hygiene


| Lint           | Why                           |
| -------------- | ----------------------------- |
| `dbg_macro`    | No debug leftovers            |
| `todo`         | No incomplete code markers    |
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

Supply chain security with [cargo-deny](https://github.com/EmbarkStudios/cargo-deny). Install it first:

```bash
cargo install cargo-deny
```

Then create `.cargo/deny.toml`:

```toml
[licenses]
allow = ["MIT", "Apache-2.0", "BSD-3-Clause", "ISC", "Zlib", "CC0-1.0"]

[bans]
wildcards = "deny"

[advisories]
vulnerability = "deny"
```

Run with `cargo deny check`.

### CONSTITUTION.md

A profile-specific guide for AI agents and human reviewers, based on Google's Rust guidance with explicit local overrides.  
Use the constitution from the same profile as your lint settings, such as [standard/CONSTITUTION.md](skills/rust-magic-linter/assets/standard/CONSTITUTION.md).  

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

See [`docs/CREDITS.md`](docs/CREDITS.md) for full attribution, [`docs/ANALYSIS.md`](docs/ANALYSIS.md) for the complete research of how these repos work with AI, and [`docs/COMPARISON.md`](docs/COMPARISON.md) for a lint-by-lint comparison.

---

## License

MIT — See [LICENSE](LICENSE)