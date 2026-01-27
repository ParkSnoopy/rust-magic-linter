---
name: rust-magic-linter
description: Add strict Clippy lint configurations to Rust projects for AI-assisted development
argument-hint: "[minimal|standard|maximum]"
allowed-tools: Read, Write, Edit, Bash(cargo:*), Bash(curl:*), Glob
disable-model-invocation: true
---

# Rust Magic Linter

Add strict Clippy lint configurations to Rust projects. These "guardrails" help AI agents write better Rust code by turning best practices into compiler errors.

**Repository:** https://github.com/vicnaum/rust-magic-linter

## Presets

- **minimal** - Just panic guards: `unwrap`, `expect`, `panic`, `allow_attributes`, `dbg_macro`, `todo`
- **standard** - Recommended for most projects: pedantic + async safety + output control
- **maximum** - Maximum strictness (Tenex-style): all lint groups at deny level

## Instructions

When the user invokes this skill:

1. **Check if this is a Rust project** - Look for `Cargo.toml`. If not found, tell the user.

2. **Determine the preset** - Use the argument if provided (`$ARGUMENTS`), otherwise ask the user:
   - `minimal` - Quick safety net, minimal code changes needed
   - `standard` - Recommended for most projects
   - `maximum` - Very strict, may require significant code changes

3. **Check if workspace** - If `Cargo.toml` contains `[workspace]`, use `[workspace.lints.*]` instead of `[lints.*]`

4. **Check for existing lints** - Look for `[lints.` or `[workspace.lints.` sections. Warn if they exist.

5. **Apply the configuration** - Append the preset to `Cargo.toml`

6. **Create clippy.toml** - If it doesn't exist, create it with complexity thresholds

7. **Verify** - Run `cargo clippy` to check for any immediate issues

## Preset: minimal

```toml
[lints.clippy]
unwrap_used = "deny"
expect_used = "deny"
panic = "deny"
allow_attributes = "deny"
dbg_macro = "deny"
todo = "deny"
```

## Preset: standard

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

# Relaxations for practicality
missing_errors_doc = "allow"
missing_panics_doc = "allow"
doc_markdown = "allow"
must_use_candidate = "allow"
module_name_repetitions = "allow"
similar_names = "allow"
too_many_lines = "allow"
```

## Preset: maximum

For the full maximum preset (50+ lints), fetch from GitHub:

```bash
curl -sL https://raw.githubusercontent.com/vicnaum/rust-magic-linter/main/presets/maximum.toml
```

Or see the repository for the complete configuration.

## clippy.toml

Always create this file in the project root:

```toml
cognitive-complexity-threshold = 15
type-complexity-threshold = 200
too-many-lines-threshold = 100
doc-valid-idents = ["LLM", "AI", "API", "CLI", "TUI", "AST", "MCP"]
```

## Additional Files (Optional)

Offer to create these if the user wants:

- **`.cargo/deny.toml`** - Supply chain security with cargo-deny
- **`CONSTITUTION.md`** - Project rules template

Fetch templates from: `https://raw.githubusercontent.com/vicnaum/rust-magic-linter/main/templates/`
