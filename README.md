# Chart Generation Agentic Workflow — LangGraph

A production-structured Python project that implements the **reflection design pattern** for data visualization using **LangGraph**.

An LLM generates a matplotlib chart from a natural-language instruction, a second vision-capable LLM critiques the chart image, and improved code is generated and executed automatically.

---

## Why LangGraph?

This workflow has **explicit shared state** and **four distinct sequential steps** — a perfect fit for LangGraph's `StateGraph`:

- Each step (generate → execute → reflect → execute) is an isolated, testable node
- A shared `ChartAgentState` TypedDict flows cleanly between all nodes
- Conditional edges add automatic error-handling with zero extra code
- The graph is extendable (retry loops, human-in-the-loop, branching) without restructuring

LangChain (LCEL) alone is better suited for simple linear prompt→LLM→output chains. This project needs stateful multi-step orchestration — that's LangGraph's strength.

---

## Project Structure

```
chart_agent/
├── main.py                   # Entry point — CLI args, runs the graph
├── graph.py                  # LangGraph StateGraph definition
├── state.py                  # Shared ChartAgentState TypedDict
├── nodes/
│   ├── generate_node.py      # Step 1: LLM writes matplotlib code (V1)
│   ├── execute_node.py       # Steps 2 & 4: exec() the generated code
│   └── reflect_node.py       # Step 3: vision LLM critiques chart → V2 code
├── utils/
│   ├── llm_clients.py        # OpenAI + Anthropic client setup & helpers
│   ├── data_loader.py        # CSV loading + date-part derivation
│   └── image_utils.py        # Base64 encoding, tag extraction helpers
├── data/
│   └── coffee_sales.csv      # Sample dataset
├── outputs/                  # Generated charts saved here (gitignored)
├── .env.example              # Rename to .env and add your API keys
├── requirements.txt
└── README.md
```

---

## Workflow

```
User instruction
      │
      ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│  generate   │────►│  execute_v1  │────►│   reflect   │────►│  execute_v2  │
│  (LLM)      │     │  (exec code) │     │  (vision    │     │  (exec code) │
│             │     │              │     │   LLM)      │     │              │
└─────────────┘     └──────────────┘     └─────────────┘     └──────────────┘
      │                    │                    │
    error               error               error
      └────────────────────┴────────────────────┴──► END (with error logged)
```

---

## Setup

```bash
# 1. Clone / copy the project
cd chart_agent

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure API keys
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY and/or ANTHROPIC_API_KEY
```

---

## Usage

```bash
# Run with defaults (gpt-4o-mini for generation, gpt-4o for reflection)
python main.py

# Custom instruction
python main.py --instruction "Show monthly revenue trend for 2024"

# Mix models
python main.py \
  --generation-model gpt-4o-mini \
  --reflection-model claude-3-5-sonnet-20241022 \
  --image-basename monthly_revenue

# Full options
python main.py --help
```

### CLI Arguments

| Argument | Default | Description |
|---|---|---|
| `--instruction` | Q1 comparison prompt | Natural-language chart request |
| `--dataset` | `data/coffee_sales.csv` | Path to input CSV |
| `--generation-model` | `gpt-4o-mini` | LLM for code generation |
| `--reflection-model` | `gpt-4o` | Vision LLM for reflection (must support images) |
| `--image-basename` | `chart` | Prefix for output filenames |

---

## Outputs

Charts are saved to the `outputs/` directory:

- `outputs/chart_v1.png` — Initial generated chart
- `outputs/chart_v2.png` — Improved chart after reflection

---

## Extending the Workflow

Because this is a LangGraph `StateGraph`, extensions are straightforward:

- **Retry on exec error** — add a conditional edge from `execute_v1` back to `generate`
- **Second reflection pass** — add another `reflect → execute` cycle
- **Human-in-the-loop** — add an interrupt before `execute_v2` for approval
- **Different datasets** — pass any CSV path via `--dataset`

---

## Model Combinations

| Generation | Reflection | Notes |
|---|---|---|
| `gpt-4o-mini` | `gpt-4o` | Fast + accurate, all-OpenAI |
| `gpt-4o-mini` | `claude-3-5-sonnet-20241022` | Excellent vision critique |
| `gpt-4o` | `claude-3-opus-20240229` | Highest quality, higher cost |