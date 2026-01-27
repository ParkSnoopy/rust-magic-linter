# Credits

## Original Inspiration

This project was inspired by a viral tweet from [@notnotstorm](https://x.com/notnotstorm) (January 2026):

> "How to get your agents to follow Rust best practices: enforce pedantic
> clippy lints in your Cargo.toml so that every best practice is required
> by default."

The insight: use Rust's static analysis as AI guardrails. Turn "taste" into compiler errors.

## Repositories Analyzed

The lint configurations in this project are derived from analysis of these 7 repositories that pioneered strict linting for AI-assisted Rust development:

### OpenAgentsInc/openagents
- **URL:** https://github.com/OpenAgentsInc/openagents
- **Role:** The "Brain" - Autonomous agent OS with DSPy, crypto identity, Plan 9 filesystem
- **Key Contribution:** Async safety lints (`await_holding_lock`), output control (`print_stdout`)

### Mockapapella/tenex
- **URL:** https://github.com/Mockapapella/tenex
- **Role:** The "Hands" - Git worktree isolation for parallel agent execution
- **Key Contribution:** Maximum strictness config with all lint groups at `deny`

### djinn09/CytoScnPy
- **URL:** https://github.com/djinn09/CytoScnPy
- **Role:** The "Eyes" - Static analysis via MCP for agents to self-verify code
- **Key Contribution:** `clippy.toml` complexity thresholds, MCP integration pattern

### john-agentic-ai-tools/crush
- **URL:** https://github.com/john-agentic-ai-tools/crush
- **Role:** Workflow - Constitution pattern + spec-driven TDD
- **Key Contribution:** The "Constitution" pattern for codifying project laws

### deltartificial/cawd
- **URL:** https://github.com/deltartificial/cawd
- **Role:** Visualization - Read-only TUI to verify agent file edits
- **Key Contribution:** `allow_attributes = "deny"` - the "no cheating" rule

### mkroman/zeta
- **URL:** https://github.com/mkroman/zeta
- **Role:** Plugin System - Modular IRC bot showing pedantic + ergonomic balance
- **Key Contribution:** Balanced pedantic overrides for maintainable strict linting

### danthedaniel/BF-JIT
- **URL:** https://github.com/danthedaniel/BF-JIT
- **Role:** Low-level Safety - JIT compiler showing lints for unsafe code wrapping
- **Key Contribution:** Demonstrates AI-written code (AArch64 backend by Claude 3 Opus) with strict lints

## The AI Agent Stack

These repositories together form a complete "AI Agent Stack":

```
                    YOUR RUST PROJECT
┌─────────────────────────────────────────────────────────────┐
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
└─────────────────────────────────────────────────────────────┘
```

## Research

See [ANALYSIS.md](ANALYSIS.md) for the full technical analysis of these repositories.

## License

This project is MIT licensed. The original repositories have their own licenses - please check each repository for details.
