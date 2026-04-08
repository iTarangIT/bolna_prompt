# ElevenLabs Prompting Guide

Source: https://elevenlabs.io/docs/eleven-agents/best-practices/prompting-guide

## Introduction

Effective prompting transforms ElevenLabs Agents from robotic to lifelike. A system prompt serves as the personality and policy blueprint of an AI agent. In enterprise contexts, these prompts tend to be comprehensive, defining the agent's role, goals, available tools, step-by-step task instructions, and guardrails describing prohibited behaviors.

The system prompt controls conversational behavior and response style, but does not control conversation flow mechanics like turn-taking or agent settings like language capabilities—those are handled at the platform level.

## Prompt Engineering Fundamentals

Production-grade prompt engineering rests on several core principles:

### Separate Instructions Into Clean Sections

Organizing instructions with markdown headings helps models prioritize and interpret them correctly. Models are tuned to pay extra attention to certain headings (especially `# Guardrails`), and clear section boundaries prevent instruction bleed where rules from one context affect another.

**Less effective approach:**
```
You are a customer service agent. Be polite and helpful. Never share sensitive data. You can look 
up orders and process refunds. Always verify identity first. Keep responses under 3 sentences 
unless the user asks for details.
```

**Recommended approach:**
```
# Personality
You are a customer service agent for Acme Corp. You are polite, efficient, and solution-oriented.

# Goal
Help customers resolve issues quickly by looking up orders and processing refunds when appropriate.

# Guardrails
Never share sensitive customer data across conversations or reveal sensitive account information 
without proper verification.
Always verify customer identity before accessing account information.

# Tone
Keep responses concise (under 3 sentences) unless the user requests detailed explanations.
```

### Be As Concise As Possible

Keep every instruction short, clear, and action-based. Concise instructions reduce ambiguity and token usage—every unnecessary word becomes a potential source of misinterpretation.

**Less effective approach:**
```
# Tone
When you're talking to customers, you should try to be really friendly and approachable, making 
sure that you're speaking in a way that feels natural and conversational, kind of like how you'd 
talk to a friend, but still maintaining a professional demeanor that represents the company well.
```

**Recommended approach:**
```
# Tone
Speak in a friendly, conversational manner while maintaining professionalism.
```

If the agent needs to maintain a specific tone, define it explicitly and concisely in the `# Personality` or `# Tone` section. Avoid repeating tone guidance throughout the prompt.

### Emphasize Critical Instructions

Highlight critical steps by adding "This step is important" at the end of the line. Repeating the most important 1-2 instructions twice in the prompt helps reinforce them. In complex prompts, models may prioritize recent context over earlier instructions, so emphasis and repetition ensure critical rules aren't overlooked.

**Less effective approach:**
```
# Goal
Verify customer identity before accessing their account.
Look up order details and provide status updates.
Process refund requests when eligible.
```

**Recommended approach:**
```
# Goal
Verify customer identity before accessing their account. This step is important.
Look up order details and provide status updates.
Process refund requests when eligible.

# Guardrails
Never access account information without verifying customer identity first. This step is important.
```

### Text Normalization

Text-to-speech models are best at generating speech from alphabetical text. Digits and symbols such as "@" or "£" are more likely to cause incorrect pronunciations or voice hallucinations. Text is normalized into words before reaching the TTS model (e.g., `123` → `one-hundred and twenty three`, `john@gmail.com` → `john at gmail dot com`).

#### Normalization Strategies

Two strategies are available via the `text_normalisation_type` agent configuration:

**`system_prompt` (default):**
- Adds instructions to the system prompt telling the LLM to write out numbers and symbols as words
- No additional latency
- LLMs may occasionally fail to normalize correctly
- Transcripts contain everything written out in words (e.g., "one thousand dollars" instead of "$1,000")

**`elevenlabs`:**
- Uses ElevenLabs' TTS normalizer to normalize text after LLM generation, before it reaches the TTS model
- More reliable than LLM-based normalization
- System prompt is not modified
- Transcripts retain natural formatting with symbols and numbers (e.g., "$1,000")
- Adds minor latency

If transcript readability matters, consider using the `elevenlabs` normalizer. It keeps transcripts clean with natural symbols and numbers while still producing correctly spoken audio.

#### Structured Data for Tool Inputs

When using the `system_prompt` normalization setting, the LLM writes out symbols and numbers as words in its responses. User transcriptions from speech-to-text can also arrive in non-standard form. When using these details as tool parameters, the LLM may use the unstructured version present in the conversation context.

If a tool parameter expects a correctly formatted value (e.g., `john@gmail.com` not `john at gmail dot com`), include the expected format directly in the tool parameter description with an example.

**Less effective:**
```
## `lookupAccount` tool parameters

- `email` (required): "The user's email."
- `phone` (required): "The user's phone number."
- `confirmation_code` (required): "The user's confirmation code."
```

**Recommended:**
```
## `lookupAccount` tool parameters

- `email` (required): "The user's email in standard email format, e.g. 'john@gmail.com'."
- `phone` (required): "The user's phone number as digits only, e.g. '5551234567'."
- `confirmation_code` (required): "The user's confirmation code as a single alphanumeric string 
  without spaces, e.g. 'ABC123'."
```

### Dedicate a Guardrails Section

List all non-negotiable rules the model must always follow in a dedicated `# Guardrails` section. Models are tuned to pay extra attention to this heading. Centralizing guardrails makes them easier to audit and update.

**Recommended approach:**
```
# Guardrails

Never share customer data across conversations or reveal sensitive account information without 
proper verification.
Never process refunds over $500 without supervisor approval.
Never make promises about delivery dates that aren't confirmed in the order system.
Acknowledge when you don't know an answer instead of guessing.
If a customer becomes abusive, politely end the conversation and offer to escalate to a supervisor.
```

## Tool Configuration for Reliability

Agents capable of handling transactional workflows can be highly effective. Equally important as prompt structure is how you describe the tools available to the agent. Clear, action-oriented tool definitions help the model invoke them correctly and recover gracefully from errors.

### Describe Tools Precisely with Detailed Parameters

When creating a tool, add descriptions to all parameters. This helps the LLM construct tool calls accurately.

**Tool description:** "Looks up customer order status by order ID and returns current status, estimated delivery date, and tracking number."

**Parameter descriptions:**
- `order_id` (required): "The unique order identifier, formatted as written characters (e.g., 'ORD123456')"
- `include_history` (optional): "If true, returns full order history including status changes"

Parameter descriptions act as inline documentation for the model, clarifying format expectations, required vs. optional fields, and acceptable values.

### Explain When and How to Use Each Tool in the System Prompt

Clearly define in the system prompt when and how each tool should be used. Don't rely solely on tool descriptions—provide usage context and sequencing logic.

**Recommended approach:**
```
# Tools

You have access to the following tools:

## `getOrderStatus`

Use this tool when a customer asks about their order. Always call this tool before providing order 
information—never rely on memory or assumptions.

**When to use:**
- Customer asks "Where is my order?"
- Customer provides an order number
- Customer asks about delivery estimates

**How to use:**
1. Collect the order ID from the customer
2. Call `getOrderStatus` with the order ID
3. Present the results to the customer in natural language

**Error handling:**
If the tool returns "Order not found", ask the customer to verify the order number and try again.

## `processRefund`

Use this tool only after verifying:
1. Customer identity has been confirmed
2. Order is eligible for refund (within 30 days, not already refunded)
3. Refund amount is under $500 (escalate to supervisor if over $500)

**Required before calling:**
- Order ID (from `getOrderStatus`)
- Refund reason code
- Customer confirmation

This step is important: Always confirm refund details with the customer before calling this tool.
```

### Specify Expected Formats in Tool Parameter Descriptions

When tools require structured identifiers (emails, phone numbers, codes), make the expected format explicit in the parameter description with an example.

### Handle Tool Call Failures Gracefully

Tools can fail due to network issues, missing data, or other errors. Include clear instructions in the system prompt for recovery. Without explicit handling instructions, agents may hallucinate responses or provide incorrect information.

**Recommended approach:**
```
# Tool error handling

If any tool call fails or returns an error:

1. Acknowledge the issue to the customer: "I'm having trouble accessing that information right now."
2. Do not guess or make up information
3. Offer alternatives:
   - Try the tool again if it might be a temporary issue
   - Offer to escalate to a human agent
   - Provide a callback option
4. If the error persists after 2 attempts, escalate to a supervisor

**Example responses:**
- "I'm having trouble looking up that order right now. Let me try again... [retry]"
- "I'm unable to access the order system at the moment. I can transfer you to a specialist who can 
  help, or we can schedule a callback. Which would you prefer?"
```

## Architecture Patterns for Enterprise Agents

While strong prompts and tools form the foundation of agent reliability, production systems require thoughtful architectural design. Enterprise agents handle complex workflows that often exceed the scope of a single, monolithic prompt.

### Keep Agents Specialized

Overly broad instructions or large context windows increase latency and reduce accuracy. Each agent should have a narrow, clearly defined knowledge base and set of responsibilities. Specialized agents have fewer edge cases to handle, clearer success criteria, and faster response times. They're easier to test, debug, and improve.

### Use Orchestrator and Specialist Patterns

For complex tasks, design multi-agent workflows that hand off tasks between specialized agents—and to human operators when needed.

**Architecture pattern:**

1. **Orchestrator agent:** Routes incoming requests to appropriate specialist agents based on intent classification
2. **Specialist agents:** Handle domain-specific tasks (billing, scheduling, technical support, etc.)
3. **Human escalation:** Defined handoff criteria for complex or sensitive cases

### Define Clear Handoff Criteria

When designing multi-agent workflows, specify exactly when and how control should transfer between agents or to human operators.

## Model Selection for Enterprise Reliability

Selecting the right model depends on performance requirements—particularly latency, accuracy, and tool-calling reliability.

### Model Recommendations by Use Case

* **GPT-4o or GLM 4.5 Air (recommended starting point):** Best for general-purpose enterprise agents where latency, accuracy, and cost must be balanced.
* **Gemini 2.5 Flash Lite (ultra-low latency):** Best for high-frequency, simple interactions where speed is critical.
* **Claude Sonnet 4 or 4.5 (complex reasoning):** Best for multi-step problem-solving, nuanced judgment, and complex tool orchestration.

### Benchmark with Your Actual Prompts

Model performance varies significantly based on prompt structure and task complexity. Test 2-3 candidate models with your actual system prompt, evaluate on real user queries, and measure latency, accuracy, and tool-calling success rate.

## Iteration and Testing

Reliability in production comes from continuous iteration. Even well-constructed prompts can fail in real use.

### Configure Evaluation Criteria

**Key metrics to track:**
- **Task completion rate:** Percentage of user intents successfully addressed
- **Escalation rate:** Percentage of conversations requiring human intervention

### Analyze Failure Patterns

- **Where does the agent provide incorrect information?** → Strengthen instructions in specific sections
- **When does it fail to understand user intent?** → Add examples or simplify language
- **Which user inputs cause it to break character?** → Add guardrails for edge cases
- **Which tools fail most often?** → Improve error handling or parameter descriptions

### Make Targeted Refinements

1. **Isolate the problem:** Identify which prompt section or tool definition is causing failures
2. **Test changes on specific examples:** Use conversations that previously failed as test cases
3. **Make one change at a time:** Isolate improvements to understand what works
4. **Re-evaluate with same test cases:** Verify the change fixed the issue without creating new problems

## Production Considerations

### Handle Errors Across All Tool Integrations

Every external tool call is a potential failure point. Ensure the prompt includes explicit error handling for:
* **Network failures:** "I'm having trouble connecting to our system. Let me try again."
* **Missing data:** "I don't see that information in our system. Can you verify the details?"
* **Timeout errors:** "This is taking longer than expected. I can escalate to a specialist or try again."
* **Permission errors:** "I don't have access to that information. Let me transfer you to someone who can help."

## Formatting Best Practices

* **Use markdown headings:** Structure sections with `#` for main sections, `##` for subsections
* **Prefer bulleted lists:** Break down instructions into digestible bullet points
* **Use whitespace:** Separate sections and instruction groups with blank lines
* **Keep headings in sentence case:** `# Goal` not `# GOAL`
* **Be consistent:** Use the same formatting pattern throughout the prompt

## FAQ Highlights

* **Minimum viable prompt:** Personality/role definition, Primary goal, Core guardrails, Tool descriptions
* **Prompt length:** Keep under 2000 tokens; split into specialized agents if longer
* **Prevent hallucination on tool failure:** Explicit error handling + "never guess" guardrail repeated in multiple sections
* **Prompt updates:** Can be modified at any time; test in staging first
* **Multi-model support:** Principles in this guide work across models; tune tool-calling format per model
