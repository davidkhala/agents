# Model Provider

## Hugging Face Model
Error: `Model Qwen/Qwen3-VL-8B-Instruct is not a valid task, must be one of ('text2text-generation', 'text-generation').`
- Cause: Qwen/Qwen3-VL-8B-Instruct 是一个多模态模型（Vision-Language），没有 text-generation 或 text2text-generation 标签
- Cause: 本 Dify plugin 不支持

## Azure OpenAI Service Model
The only support plugin for Microsoft Foundry native models
- **API Endpoint URL**: `https://ai-japanest.cognitiveservices.azure.com/openai/deployments/<model-name>/chat/completions?api-version=2025-01-01-preview`
- **API Version**: `2025-01-01-preview`
- **Base Model**: select one equals to your model name
- **Deployment Name**: model name
