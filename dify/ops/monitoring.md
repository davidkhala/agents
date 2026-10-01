
# Metrics
`Total Messages` vs `Avg. Session Interactions`
- Session Interactions更接近自然对话
  - Agent 回复失败或被截断：用户发了消息，但没有对应回复，这样会增加 Messages，但不会增加完整的 Interaction。
  - System prompt和tool call它们会被计入 Messages，但不算 Interaction
  - 多轮回复： 用户发一条消息，Agent可能拆成多条回复（例如流式输出或分段回答），这会让 Messages 增加，但 Interaction 只算一次。
