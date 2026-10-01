You cannot change type of existing app
# type: Workflow
> Agentic flow for intelligent automations
- convertable to tool
  - **Immutable**. Once you publish it by configure `Workflow as tool`. It is a snapshot that will not get updated by `Publish Update`
  - To update it, you need to delete the derived workflow tool and recreate it.
Start Node
- does not have `sys.query`

# type: Chatflow
>　workflow enhanced for multi-turn chats

## Variable Assigner Node
> used to assign values to writable variables

writable variables is one of [conversation variables]

### conversation variables
defined by top-right corner
![conversation variables](conversation-var.png)

# basic type: Chatbot
>　LLM-based chatbot with simple setup
# basic type: Agent
> Intelligent agent with reasoning and autonomous tool use
- Agent Mode is not configurable, always `Function Calling` 

# basic type: Text Generator
> Al assistant for text generation tasks
- aka. Completion
- No workflow
- 只进行一次问答：没有system prompt
- 支持多模型并发，适合用于模型对比评估
