# dlt Workshop Results

| Question | Exact result | Selected option |
|---|---|---|
| Q1 | Span count for trace `019f8080cd4c27a64caf5b4a812a5671` = 4 | 5 |
| Q2 | dlt created 23 tables in schema `agent_traces` | 24 |
| Q3 | LLM input tokens = `[326, 1871]`, total = 2197 | 1500 - 5000 |

## Supporting details

- Trace/run identifier: `019f8080cd4c27a64caf5b4a812a5671`
- Span names in the trace: `invoke_agent agent`, `chat qwen-plus`, `execute_tool search`, `chat qwen-plus`
- DuckDB table names:
  - `_dlt_loads`
  - `_dlt_pipeline_state`
  - `_dlt_version`
  - `records`
  - `records__attributes__gen_ai_input_messages`
  - `records__attributes__gen_ai_input_messages__parts`
  - `records__attributes__gen_ai_input_messages__parts__result`
  - `records__attributes__gen_ai_output_messages`
  - `records__attributes__gen_ai_output_messages__parts`
  - `records__attributes__gen_ai_response_finish_reasons`
  - `records__attributes__gen_ai_system_instructions`
  - `records__attributes__gen_ai_tool_call_result`
  - `records__attributes__gen_ai_tool_definitions`
  - `records__attributes__gen_ai_tool_definitions__parameters__required`
  - `records__attributes__logfire_metrics__gen_ai_client_token_usage__details`
  - `records__attributes__logfire_scrubbed`
  - `records__attributes__logfire_scrubbed__path`
  - `records__attributes__model_request_parameters__function_tools`
  - `records__attributes__model_request_parameters__function_tools__parameters_json_schema__required`
  - `records__attributes__model_request_parameters__instruction_parts`
  - `records__attributes__pydantic_ai_all_messages`
  - `records__attributes__pydantic_ai_all_messages__parts`
  - `records__attributes__pydantic_ai_all_messages__parts__result`
