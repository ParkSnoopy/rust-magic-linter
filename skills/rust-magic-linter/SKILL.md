---
name: rust-magic-linter
description: Add strict Clippy lint configurations to Rust projects for AI-assisted development. Use when the user wants to add Clippy lints, AI guardrails, or rust-magic-linter to a Rust project. Supports three presets (minimal, standard, maximum) that enforce best practices and prevent common AI coding mistakes like using unwrap(), silencing warnings with #[allow()], or leaving debug code.
---

# Rust Magic Linter

Add strict Clippy lint configurations to Rust projects. These "guardrails" help AI agents write better Rust code by turning best practices into compiler errors.

## Workflow

1. Verify this is a Rust project (check for `Cargo.toml`)
2. Ask which preset the user wants (if not specified)
3. Check if `[lints.*]` sections already exist in Cargo.toml
4. Detect workspace vs single project (use `[workspace.lints.*]` for workspaces)
5. Apply `assets/<preset>/lint.toml`, merging existing lint tables rather than appending duplicates
6. Create `clippy.toml` from `assets/<preset>/clippy.toml`; preserve existing `clippy.toml` or `.clippy.toml` unless replacement is requested
7. Optionally offer shared `.cargo/deny.toml` and `assets/<preset>/CONSTITUTION.md`
8. Run `cargo clippy` to verify

## Presets

- **minimal** - Just panic guards: `unwrap`, `expect`, `panic`, `allow_attributes`, `dbg_macro`, `todo`. Use for quick safety net with minimal code changes.
- **standard** - Pedantic + async safety + output control. Recommended for most projects.
- **maximum** - Clippy's all, pedantic, nursery, and cargo groups at deny level, plus Rust and rustdoc checks and explicit relaxations. Forbids unsafe code.

## Assets

All configuration files are in `assets/`:

- `assets/minimal/` - Minimal profile bundle
- `assets/standard/` - Standard profile bundle (recommended)
- `assets/maximum/` - Maximum profile bundle (strictest)
- `assets/deny.toml` - cargo-deny config for `.cargo/deny.toml`

Each profile contains `lint.toml`, `clippy.toml`, and a self-contained `CONSTITUTION.md`.
Clippy settings share defaults across profiles; thresholds only affect enabled lints.
Constitutions share Google's Rust guidance and minimal guardrails, with additional rules for standard and maximum.
Profile overrides explicitly document stricter panic, lint-suppression, and unsafe-code policies rather than claiming exact Google compliance.

## Applying Configurations

1. Read `assets/<preset>/lint.toml` and its companion `CONSTITUTION.md`
2. For workspaces: replace `[lints.` with `[workspace.lints.`
3. Merge into `Cargo.toml` with a header linking to https://github.com/ParkSnoopy/rust-magic-linter; do not duplicate existing tables
4. Copy `assets/<preset>/clippy.toml` to project root unless `clippy.toml` or `.clippy.toml` already exists
5. If user wants supply chain security: copy `assets/deny.toml` to `.cargo/deny.toml`
6. If user wants project rules: copy `assets/<preset>/CONSTITUTION.md` to project root; preserve an existing constitution unless replacement is requested
7. For workspaces: add `[lints]` with `workspace = true` in each participating member, including the root package when present
8. Run `cargo clippy --workspace --all-targets` and report actual diagnostics; do not weaken lint levels to obtain a pass

## Key Lints Explained

`allow_attributes = "deny"` rejects `#[allow(...)]` attributes during Clippy checks.
Do not use other suppression mechanisms to evade the selected policy; these configurations are checks, not a tamper-proof sandbox.

Other critical lints:
- `unwrap_used`, `expect_used`, `panic` - Reject these constructs, not every possible panic source
- `dbg_macro`, `todo` - No debug leftovers or incomplete code
- `print_stdout`, `print_stderr` - Use structured logging or explicit writers in standard and maximum
- `await_holding_lock` - Reject synchronous lock guards held across await in standard and maximum

## Repository

https://github.com/ParkSnoopy/rust-magic-linter
