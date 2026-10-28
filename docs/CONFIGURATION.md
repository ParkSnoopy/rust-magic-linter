# Configuration and installation

## Profile bundles

Choose one profile and keep its three files together:

```text
skills/rust-magic-linter/assets/
├── minimal/
│   ├── lint.toml
│   ├── clippy.toml
│   └── CONSTITUTION.md
├── standard/
│   ├── lint.toml
│   ├── clippy.toml
│   └── CONSTITUTION.md
├── maximum/
│   ├── lint.toml
│   ├── clippy.toml
│   └── CONSTITUTION.md
└── deny.toml
```

- [Minimal](../skills/rust-magic-linter/assets/minimal/) denies `unwrap_used`, `expect_used`, `panic`, `allow_attributes`, `dbg_macro`, and `todo`.
- [Standard](../skills/rust-magic-linter/assets/standard/) retains those guardrails, adds pedantic warnings with explicit relaxations, and denies additional panic, output, async-lock, placeholder, and process-exit patterns.
- [Maximum](../skills/rust-magic-linter/assets/maximum/) adds Rust and rustdoc checks, forbids unsafe code and non-ASCII identifiers, and denies Clippy's `all`, `pedantic`, `nursery`, and `cargo` groups with explicit relaxations.

`lint.toml` is a Cargo manifest fragment, not a standalone Cargo manifest.
Merge its tables into `Cargo.toml`.
Place its companion `clippy.toml` next to the manifest and optionally copy the same profile's `CONSTITUTION.md` to the project root.
The optional [cargo-deny configuration](../skills/rust-magic-linter/assets/deny.toml) is shared by all profiles.

## Installation sources

Installation commands and downloaded assets use [ParkSnoopy/rust-magic-linter](https://github.com/ParkSnoopy/rust-magic-linter), branch `main`.
See the [README](../README.md#quick-start-4-ways-to-install) for installation methods.
The shell installer requires Bash, curl, and ordinary Unix command-line tools, and runs from the target Rust project's root.
It defaults to `standard`; pass `minimal` or `maximum` to select another bundle.
It downloads `assets/<profile>/lint.toml`, `assets/<profile>/clippy.toml`, and, when requested, `assets/<profile>/CONSTITUTION.md`.

The installer preserves an existing `clippy.toml`, `.clippy.toml`, or `CONSTITUTION.md`.
It refuses manifests containing existing lint tables rather than appending duplicate tables.
Merge those settings manually or through the skill after reviewing the selected profile.
When switching profiles, compare the companion constitution and Clippy settings as well as the lint fragment.

The compact `bash -c "$(curl ...)"` README form keeps stdin available for prompts but does not reliably propagate download failure.
For explicit download-failure propagation, run this from the target Rust project:

```bash
installer=$(curl -fsSL https://raw.githubusercontent.com/ParkSnoopy/rust-magic-linter/main/scripts/install.sh) && bash -c "$installer" -- standard
```

Optional files require affirmative answers; blank input or EOF declines them.
An affirmative answer to the cargo-deny prompt can replace `.cargo/deny.toml`.
Install cargo-deny separately with `cargo install cargo-deny` before running `cargo deny check`.

## Cargo workspaces

In a workspace root, use `[workspace.lints.*]` instead of `[lints.*]` for the selected fragment.
The shell installer performs that conversion.
Each participating package must explicitly inherit workspace lints:

```toml
[lints]
workspace = true
```

Add that table to each member's `Cargo.toml`.
If the workspace root also contains `[package]`, its root package needs the same opt-in.
The shell installer does not edit member manifests or add the root package opt-in automatically.

Verify the participating packages:

```bash
cargo clippy --workspace --all-targets
```

## Google guidance and profile overrides

Each constitution is self-contained and shares the minimal profile's [Google-based guidance](../skills/rust-magic-linter/assets/minimal/CONSTITUTION.md).
The [standard constitution](../skills/rust-magic-linter/assets/standard/CONSTITUTION.md) adds a short standard-specific section.
The [maximum constitution](../skills/rust-magic-linter/assets/maximum/CONSTITUTION.md) retains that guidance and adds its stricter overrides.

These are deliberate profile policies, not exact reproductions of [Google's Rust Style Guide](https://google.github.io/styleguide/rustguide.html):

- Google permits invariant panics and prefers `expect()` when one is necessary; all three profiles deny `unwrap()`, `expect()`, and explicit `panic!()` calls.
- Google permits some lint allowances; all three profiles deny `#[allow(...)]` attributes.
- Google permits necessary, justified unsafe abstractions; maximum forbids unsafe code entirely.
- Chromium-only async, threading, import, and source-layout requirements do not become universal Cargo-project rules.

Library API guidance should not force unnecessary abstractions into application code.
Public API documentation, ownership design, and other review rules remain relevant even where a profile does not enable a corresponding lint.
Passing Clippy does not establish complete Google-guide compliance or prove that code cannot panic.

## Clippy thresholds and comments

All three profiles currently ship identical `clippy.toml` defaults and consistent comments for shared lint entries.
Each bundle contains its own copy so it can be installed independently.
Keep shared defaults synchronized unless a profile intentionally requires a documented difference.

Thresholds configure lints; they do not enable them.
In particular, standard explicitly allows `too_many_lines`, and maximum explicitly allows `cognitive_complexity`.
Their respective thresholds therefore do not enforce those checks in those profiles.
`doc-valid-idents` similarly matters only when the documentation lint that consumes it is active.
The [complete lint reference](cargo-lints-reference.toml) is a separate explanatory example, not another installable profile.

## Repository verification

Run the installer integration tests with Python 3.11 or newer and an installed Rust toolchain with Clippy:

```bash
bash -n scripts/install.sh
shellharden --check scripts/install.sh
python3 -B -m unittest discover -s tests -v
```

The tests substitute local asset downloads at the curl boundary, verify profile selection and workspace inheritance, and run real offline Cargo/Clippy checks against installed configurations.
They do not publish the changed assets or prove that unpublished paths are already downloadable from GitHub.
