# Voice Conversation Design for AI Sales Agents

Patterns for natural, effective voice conversations in outbound B2B sales calls. Covers turn-taking, pacing, silence handling, and call structure.

---

## 1. Turn-Taking Choreography

Voice conversations have rhythm. Each phase of the call has a different optimal response length:

### Words-Per-Turn by Phase

| Phase | Agent Target | Why |
|-------|-------------|-----|
| Opening (greeting + intro) | 25-35 words | Must be complete but fast — dealer decides in seconds |
| Permission / Language check | 10-20 words | Simple yes/no question, don't overload |
| Discovery (asking questions) | 15-25 words | Ask one question, then STOP and listen |
| Acknowledgment (after dealer speaks) | 5-15 words | Short validation before next question |
| Product presentation | 40-60 words | This is where you deliver value — can be longer |
| Objection handling | 20-35 words | Acknowledge + respond concisely |
| Closing / Next steps | 15-25 words | Clear, specific, actionable |

### The One-Question Rule
In discovery, ask exactly ONE question per turn. Then stop. Wait for the answer. Acknowledge. Then ask the next question.

Bad: "आपकी current battery कौनसी है? और monthly कितनी batteries लगती हैं? Voltage कौनसा use करते हैं?"

Good: "Sir, आप currently कौनसी batteries use करते हैं?"
[wait for answer]
"अच्छा, और monthly approximately कितनी units लगती हैं?"

### Yield on Interruption
If the dealer starts speaking while the agent is mid-sentence:
1. Stop immediately — do not finish the sentence
2. Listen to what the dealer said
3. Respond to their point first, then circle back if needed
4. Never say "let me finish" or "as I was saying"

---

## 2. Active Listening Signals

In voice calls, the dealer cannot see you nodding. You must signal attention verbally.

### Verbal Nods (use between dealer statements)
- "हाँ जी" — simple acknowledgment
- "बिल्कुल" — enthusiastic agreement
- "Right" — English-style acknowledgment, works in Hinglish
- "समझ गया" — shows comprehension

### Paraphrasing (use after important dealer statements)
Restate the key point briefly to show you understood:
- Dealer: "हम mainly 48 Volt batteries use करते हैं, monthly 20-25 pieces"
- Agent: "अच्छा, 48 Volt, लगभग 20-25 pieces monthly — बहुत अच्छा volume है।"

### Labeling (name the emotion or concern)
Powerful for building rapport — shows emotional intelligence:
- "Sounds like service reliability is really important for your business."
- "लगता है quality को लेकर आपका experience अच्छा नहीं रहा"

### When NOT to Acknowledge
- Don't acknowledge obvious statements ("Yes, batteries are important")
- Don't acknowledge repeatedly without adding value
- Don't parrot back word-for-word — it sounds robotic

---

## 3. Silence Protocol

Silence in voice calls can mean many things. Handle each type differently:

### 2-Second Silence (normal)
- This is natural thinking time. Do nothing.
- The dealer is processing what you said.
- Resist the urge to fill the gap — let them think.

### 5-Second Silence (check-in)
- Could be thinking, could be distracted, could be poor connection.
- Gentle check: "Sir, सुन रहे हैं?" or "आप वहाँ हैं?"
- Use Hindi, not English ("Hey, are you still there?" sounds robotic and foreign)

### 10-Second Silence (connection issue likely)
- Assume connection problem. One final check:
- "Sir, लगता है connection issue है। क्या आप सुन पा रहे हैं?"
- If no response after this, note the issue and end gracefully.

### Silence After a Question (dealer thinking)
- Wait at least 3 seconds before prompting.
- If they haven't responded in 5 seconds, rephrase the question simpler:
  "मतलब — आप currently कौनसा brand use कर रहे हैं?"
- Never answer your own question or move on without their input.

### Strategic Silence (advanced)
After making a strong value statement or asking a closing question, deliberate silence is powerful:
- "Sir, 50 units पर special pricing available है। क्या interested हैं?"
- [wait — let the dealer decide, don't fill the gap]

---

## 4. Call Energy Arc

A good sales call has a natural energy curve:

```
Energy
  ^
  |    /‾‾‾‾\
  |   /      \
  |  /        \___
  | /              \
  +-------------------> Time
  Open  Build  Peak  Wind  Close
```

### Opening (0-30 sec) — Warm Start
- Friendly, confident energy
- Not too high (sounds fake), not too low (sounds bored)
- Clear identification and purpose

### Building (30-90 sec) — Discovery
- Curious, interested tone
- Ask questions with genuine interest
- Energy slightly lower than opening — you're listening mode

### Peak (90-150 sec) — Value Delivery
- Highest energy in the call
- This is where you present the product value
- Confident, specific, benefit-focused
- Enthusiasm is appropriate here — you're sharing something good

### Winding Down (150-200 sec) — Address Concerns
- Calm, patient energy
- Handle objections without matching any frustration
- Lower energy signals "I'm not desperate"

### Close (200-240 sec) — Next Steps
- Warm but businesslike
- Clear, specific next action
- End on a positive note regardless of outcome

### Duration Targets
- Cold call: 2-4 minutes total
- Warm/follow-up call: 3-6 minutes
- If exceeding 5 minutes on a cold call, proactively offer to schedule follow-up

---

## 5. Latency-Aware Design

Voice AI has processing latency between hearing the dealer and responding. Manage it:

### Natural Latency Masking
- Short filler at the start of responses: "हाँ, देखिए..." (buys 500ms)
- Acknowledgment first, then substance: "बिल्कुल sir" [pause] "तो आपकी बात है..."
- These feel natural and mask processing time

### Avoid Latency-Exposing Patterns
- Don't start with complex sentences — the pause before a long response feels longer
- Don't repeat the dealer's full question back (wastes time and sounds like stalling)
- Don't use "That's a great question" as a filler — it's transparent

### Tool Call Latency
When a tool call (product lookup, service check) takes time:
- Pre-announce: "Sir, एक second — मैं check करता हूँ" (sets expectation)
- Never go silent during a lookup — the dealer will think the call dropped
- If lookup takes more than 3 seconds, give a brief update: "बस almost हो गया"

---

## 6. Multi-Call Memory Utilization

When calling a dealer for a second or third time, how to reference past conversations:

### Do:
- Reference specific details from last call: "पिछली बार आपने 60 Volt batteries के बारे में पूछा था"
- Acknowledge continuity: "Last time हमने pricing discuss की थी"
- Build on where you left off — don't restart from zero

### Don't:
- Quote the dealer's exact words back ("You said, and I quote...") — creepy
- Reference too many details from past calls — sounds like surveillance
- Say "as per our records" or "according to our system" — sounds corporate, not personal
- Assume their situation hasn't changed — ask if things are still the same

### Memory Referencing Pattern
1. Brief context recall (1 line)
2. Check if still relevant: "क्या आप अभी भी [topic] में interested हैं?"
3. If yes, continue from where you left off
4. If situation changed, adapt and re-discover
