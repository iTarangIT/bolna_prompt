# ElevenLabs Conversational AI Prompting Best Practices

Source: ElevenLabs Documentation (elevenlabs.io/docs/eleven-agents/best-practices/prompting-guide)

## System Prompt Structure

Organize instructions into clearly separated sections using markdown headings:

- **Personality**: Agent role and character traits
- **Goal**: Primary objectives and workflow steps
- **Guardrails**: Non-negotiable rules and safety boundaries
- **Tone**: Communication style and response format
- **Tools**: Available capabilities with usage instructions
- **Error Handling**: Recovery procedures for failures

"Models are tuned to pay extra attention to certain headings (especially `# Guardrails`), and clear section boundaries prevent instruction bleed where rules from one context affect another."

## Core Design Principles

### Conciseness and Clarity
- Every instruction should be action-based and essential.
- Remove filler language — unnecessary words create ambiguity.
- BAD: "be really friendly and approachable, making sure that you're speaking in a way that feels natural"
- GOOD: "speak in a friendly, conversational manner while maintaining professionalism"

### Emphasis of Critical Instructions
- Highlight critical steps by adding "This step is important" at the end of the line.
- Repeating the most important 1-2 instructions twice in the prompt can help reinforce them.

### Guardrails Section
- Dedicate a specific section to non-negotiable rules.
- Models are tuned to pay extra attention to the `# Guardrails` heading.
- Include: data protection, authority boundaries, escalation triggers, tone/conduct guidelines.

## Tool Configuration

### Precise Parameter Documentation
- Tool parameters require explicit format descriptions with examples.
- Instead of "email address" → specify "standard email format, e.g. 'john@gmail.com'"

### Usage Context and Sequencing
- Provide when to invoke each tool, required preconditions, step-by-step calling procedures, and expected response formats.

### Error Handling
- "Tools can sometimes fail due to network issues, missing data, or other errors."
- Provide explicit recovery procedures: acknowledge the issue, avoid fabricating responses, offer alternatives (retry, escalation, callbacks).

## Architecture Patterns

### Specialization Over Generalization
- "A general-purpose 'do everything' agent is harder to maintain and more likely to fail."
- Each agent should have narrow, clearly defined responsibilities.

### Orchestrator and Specialist Pattern
- **Orchestrator**: Intent classification and routing
- **Specialists**: Domain-specific task handling
- **Human escalation**: Clear handoff criteria

## Testing and Iteration

### Targeted Refinement Process
1. Isolate the problematic prompt section
2. Test changes against previously failed conversation examples
3. Modify one element at a time
4. Re-evaluate with identical test cases

"Avoid making multiple prompt changes simultaneously — this makes it impossible to attribute improvements or regressions."

### Failure Pattern Analysis
- Identify incorrect information sources
- Note intent recognition failures
- Flag edge cases breaking character
- Analyze tools with high failure rates

## Production Safeguards

- Address failures across all integration points (network, missing data, timeouts, permissions).
- Always verify customer identity before accessing sensitive data.
- Define clear escalation thresholds and authority boundaries.

## Formatting Standards

- Use markdown headings for structural organization.
- Employ bulleted lists for digestible instruction groups.
- Separate sections with whitespace.
- Maintain consistent formatting patterns throughout.
