---
name: rust-lints
description: Add rust-magic-linter strict Clippy configuration to a Rust project
triggers:
  - rust-magic-linter
  - add rust lints
  - strict clippy
  - ai guardrails rust
---

# Rust Magic Linter Skill

Add strict Clippy lint configurations to a Rust project for AI-assisted development.

## What This Skill Does

1. Detects if the current directory is a Rust project
2. Asks which preset to use (minimal, standard, maximum)
3. Adds the lint configuration to Cargo.toml
4. Creates clippy.toml for complexity thresholds
5. Optionally creates .cargo/deny.toml for supply chain security
6. Optionally creates CONSTITUTION.md for project rules

## Instructions

When the user asks to add rust-magic-linter or strict Clippy lints:

1. **Check for Rust project**: Look for `Cargo.toml` in the current directory

2. **Ask about preset** (if not specified):
   - **minimal**: Just panic guards (`unwrap`, `expect`, `panic`, `allow_attributes`, `dbg_macro`, `todo`)
   - **standard**: The viral tweet config + async safety (recommended for most projects)
   - **maximum**: Everything at deny level (Tenex-style, very strict)

3. **Check for existing lints**: Look for `[lints.` or `[workspace.lints.` in Cargo.toml

4. **Determine if workspace**: Check for `[workspace]` in Cargo.toml. If workspace, use `[workspace.lints.*]` instead of `[lints.*]`

5. **Add the configuration**: Append the selected preset to Cargo.toml

6. **Create clippy.toml** with complexity thresholds:
   ```toml
   cognitive-complexity-threshold = 15
   type-complexity-threshold = 200
   too-many-lines-threshold = 100
   doc-valid-idents = ["LLM", "AI", "API", "CLI", "TUI", "AST", "MCP"]
   ```

7. **Offer additional files**:
   - `.cargo/deny.toml` for cargo-deny supply chain security
   - `CONSTITUTION.md` for project rules

## Preset Contents

### Minimal
```toml
[lints.clippy]
unwrap_used = "deny"
expect_used = "deny"
panic = "deny"
allow_attributes = "deny"
dbg_macro = "deny"
todo = "deny"
```

### Standard
```toml
[lints.clippy]
pedantic = { level = "warn", priority = -1 }
unwrap_used = "deny"
expect_used = "deny"
panic = "deny"
panic_in_result_fn = "deny"
allow_attributes = "deny"
dbg_macro = "deny"
todo = "deny"
unimplemented = "deny"
print_stdout = "deny"
print_stderr = "deny"
await_holding_lock = "deny"
exit = "deny"

# Relaxations
missing_errors_doc = "allow"
missing_panics_doc = "allow"
doc_markdown = "allow"
must_use_candidate = "allow"
module_name_repetitions = "allow"
similar_names = "allow"
too_many_lines = "allow"
```

### Maximum
See templates/cargo-lints.toml for the full configuration with all lint groups at deny level.

## Repository

https://github.com/vicnaum/rust-magic-linter
