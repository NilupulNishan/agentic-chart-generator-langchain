Project structure
```
chart_agent/
├── main.py                  # Entry point — runs the workflow
├── graph.py                 # LangGraph graph definition (nodes + edges)
├── state.py                 # TypedDict for shared workflow state
├── nodes/
│   ├── __init__.py
│   ├── generate_node.py     # Step 1: LLM generates V1 code
│   ├── execute_node.py      # Step 2 & 4: executes <execute_python> code
│   └── reflect_node.py      # Step 3: vision LLM critiques chart + returns V2 code
├── utils/
│   ├── __init__.py
│   ├── data_loader.py       # load_and_prepare_data()
│   ├── image_utils.py       # encode_image_b64()
│   └── llm_clients.py       # OpenAI + Anthropic client setup, get_response()
├── data/
│   └── coffee_sales.csv
├── outputs/                 # Generated charts saved here
├── .env                     # API keys
├── requirements.txt
└── README.md
```