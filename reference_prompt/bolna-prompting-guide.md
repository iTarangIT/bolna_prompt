# Bolna AI Voice Agent Prompting Best Practices

Source: Bolna Docs (bolna.ai/docs/tips-and-tricks, bolna.ai/docs/agent-setup/agent-tab)

## Prompt Writing Guidelines

- **Conciseness**: Stay concise with prompts. Start with a clear, short prompt and keep adding details iteratively.
- **Iterative Refinement**: Expect to spend time perfecting prompts — agents may not immediately follow instructions as intended.
- **Low-Latency Expert Tip**: Begin your prompt with "You will not speak more than 2 sentences" for faster, smarter conversations.
- **Response Length Control**: Limiting agent verbosity is critical. Starting prompts with sentence-count constraints improves both speed and user experience.

## Agent Prompt Structure

| Section | Purpose | Guidance |
|---------|---------|----------|
| **Personality** | Agent's tone and demeanor | Example: "warm, empathetic, and grounded customer support agent" |
| **Context** | Role background and scope | Establish who the agent represents (e.g., company affiliation) |
| **Instructions** | Specific tasks and conversation flow | Detail step-by-step actions like "Ask for order number first" |
| **Guardrails** | Boundaries and restrictions | Specify prohibited topics or actions |

## Welcome Message Tips

- Keep greetings brief and friendly to avoid sounding robotic.
- A simple "Hello, thanks for calling!" suits most scenarios.
- Incorporate personalization using `{variable_name}` syntax.

## Agent Type Selection

- **Free-flowing agents**: Enable natural conversation but require fine-tuning.
- **IVR agents**: Provide complete control, cheaper, lower risk of deviation/hallucination.
- Choose based on priority: naturalness vs. predictability.

## Performance Configuration

- **Optimal low-latency stack**: Azure/gpt-4.1mini-cluster + ElevenLabs + Deepgram + Plivo
- **Language Matching**: Verify your selected voice supports the chosen language.
- **Smart tip**: For low-latency conversations, only use the Overview page (leave all pages blank).

## Dynamic Variables

- Use `{variable_name}` syntax for caller-specific content.
- Test values before live deployment.
- Configure timezone settings for time-dependent interactions.

## Intelligent Hangup

- Enable "Hangup using a prompt" to define conversation completion conditions.
- Allows the agent to determine naturally when discussions conclude rather than relying solely on silence detection.

## Post-Call Configuration

- **Summary**: Gives a short summary of all important points discussed.
- **Extraction**: Specify classifiers to pull from the conversation.
- Use webhooks to trigger downstream tasks based on conversation content.

## Bolna Internal Prompt Patterns (from prompts.py)

- **Filler avoidance**: Avoid fillers ("Got it", "Noted") and greetings ("hey", "hello") at response start.
- **Summarization**: Create neutral, single-paragraph call summaries focusing on user agenda. Capture specific details (orders, IDs, amounts, dates) and explicit next steps without fabrication.
- **Conversation completion**: Determine completion through explicit user statements ("That's all", "Goodbye"), goal satisfaction, or demonstrated achievement.
- **Language detection**: Identify dominant user language through code-switching analysis, substantive content focus, and multilingual patterns.
