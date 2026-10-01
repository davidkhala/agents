# [Agent](https://docs.dify.ai/en/guides/workflow/node/agent#select-an-agent-strategy)
An Agent Node is a component in Dify Chatflow/Workflow that enables autonomous tool invocation.

![agentic strategy](https://assets-docs.dify.ai/dify-enterprise-mintlify/en/guides/workflow/node/1f4d803ff68394d507abd3bcc13ba0f3.png)
> Different Agentic strategies determine how the system plans and executes multi-step tool calls
- `FunctionCalling`
  - 明确、结构化 的任务
  - AI依然会自主决定对参数进行轻微调整，并多次调用工具
- `ReAct`
  - 模型先思考（Thought），再决定行动（Action），再根据 Observation 继续推理。 

Context (setting)
- 
## Limit
It don't have knowledge that link to your knowledge base