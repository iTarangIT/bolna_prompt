# Adaptive Flow Strategies for Voice AI Sales Calls

How to dynamically adjust conversation flow based on dealer engagement signals, buyer type, and call context. Covers when to follow the script, when to deviate, and how to sequence multi-call campaigns.

---

## 1. Engagement Signal Detection

Read dealer engagement from their responses to decide pacing and depth:

### High Engagement Signals
- Elaborated answers (more than asked): "हाँ, हम 48 Volt use करते हैं, पर 60 Volt भी try करना चाहते हैं"
- Dealer asks questions back: "आपके पास कौन-कौन से models हैं?"
- Dealer volunteers information: mentions competitors, pain points, expansion plans
- Dealer's tone becomes warmer or more animated
- Dealer uses first-person future: "मैं try कर सकता हूँ", "हम देखेंगे"

**Response:** Accelerate. Skip optional rapport steps, move to value delivery faster. The dealer is ready — don't bore them with a slow build.

### Moderate Engagement Signals
- Short but responsive answers: "हाँ", "48 Volt", "20 pieces"
- Dealer stays on the line but doesn't elaborate
- Neutral tone — neither enthusiastic nor dismissive

**Response:** Default pace. Follow the standard flow. Use discovery questions to draw out more information. Don't rush, don't linger.

### Low Engagement Signals
- Monosyllabic answers: "हाँ", "नहीं", "ठीक"
- Long pauses before answering
- Audible distraction (talking to someone else, background activity)
- Deflection: "WhatsApp पर भेजो", "बाद में बात करते हैं"

**Response:** Compress. Cut discovery to one question max. Deliver the single strongest value point. Offer an exit ramp: "Sir, आप busy लग रहे हैं — मैं catalogue WhatsApp पर भेज दूँ और Thursday को follow up करूँ?"

### Negative Engagement Signals
- Direct refusal: "नहीं चाहिए", "not interested"
- Irritated tone: "कितनी बार call करोगे?"
- Hang-up attempt: "रखो phone"

**Response:** Exit gracefully. One line of acknowledgment, plant a seed, close. Do not attempt to recover.

---

## 2. Dynamic Flow Rules

The conversation flow defined in the prompt is the default path. Here's when and how to deviate:

### When to Skip Steps

**Skip language check** if:
- Lead data already specifies language preference
- Dealer responds to opening in a clear language (Hindi or English)
- This is a follow-up call — language was established last time

**Skip identity confirmation** if:
- Lead data has high confidence (verified phone + owner name)
- Dealer already identified themselves: "हाँ, मैं [name] बोल रहा हूँ"
- This is a follow-up call — identity was confirmed last time

**Skip discovery** if:
- Lead status is "approved" or "hot" — they already know what they need
- Dealer immediately asks about pricing/delivery (buying signal)
- This is call 2+ and discovery was done in a previous call

**Skip product teaser** if:
- Dealer already mentions the product category: "हाँ, lithium batteries के बारे में बात करनी है"
- Lead came from an inbound inquiry about a specific product

### When to Reorder Steps

**Move product presentation before discovery** when:
- Dealer asks "what do you have?" before you've asked questions
- Dealer is clearly in a hurry (skip to value, then circle back for discovery)
- Follow-up call where discovery is already done

**Move objection handling earlier** when:
- Dealer raises a concern immediately: "Lithium batteries reliable नहीं होती"
- Address the concern NOW, then resume the flow from where it makes sense

**Move closing earlier** when:
- Strong buying signals appear at any stage (see dealer-psychology guide)
- Dealer asks "price kitna hai?" during discovery — don't say "wait, let me ask questions first"

### When to Add Steps

**Add a rapport-building step** when:
- Dealer seems cautious or suspicious (cold lead, first call)
- Rural or small-town dealer (relationship-first culture)
- Insert a brief personal touch: "Sir, आपकी shop [location] में है — बहुत अच्छा market है वहाँ।"

**Add a recap step** when:
- The call has gone on for 3+ minutes with multiple topics
- Before closing: "तो sir, summary — 60 Volt, 100 Ah, 50 units, delivery next week. सब ठीक?"

---

## 3. Buyer Type Adaptation

### Technical Buyer
**Identification:** Asks about specs, mentions voltage/capacity unprompted, uses technical terms, compares specifications.

**Adaptation:**
- Lead with specifications, not benefits
- Be precise: "100 Ah at C3 rating, 2000 cycle life at 80% DoD"
- Don't oversimplify — they'll feel patronized
- Offer detailed spec sheets via WhatsApp
- They respect competence, not warmth

### Relationship Buyer
**Identification:** Asks about the company, wants to know who you are, mentions existing supplier relationship, talks about trust.

**Adaptation:**
- Extend the rapport-building phase
- Talk about company history, team, service commitment
- Offer a personal visit early
- Don't rush to specs — they'll feel sold to
- They buy from people, not products

### Price Buyer
**Identification:** First or second question is about price, compares unit costs, asks about discounts immediately.

**Adaptation:**
- Don't dodge the price question — address it directly
- Frame value after stating price: "18,900 per unit — and that includes 3-year warranty and free delivery"
- Offer bulk pricing tiers quickly
- They respect efficiency, not long pitches

### Need-Unaware Buyer
**Identification:** "हमें lithium नहीं चाहिए", doesn't know the product category, confused about why you're calling.

**Adaptation:**
- Don't pitch. Educate briefly.
- One surprising fact: "क्या आपको पता है lithium batteries का per-km cost lead-acid से कम है?"
- If still not interested, plant seed and exit
- These leads need nurturing across multiple calls

---

## 4. Follow-Up Sequencing

### Call 1 — Introduction + Qualify + Plant Seed
**Goal:** Establish who you are, determine if this is a viable lead, leave a memorable impression.
- Full opening (name + company + product + permission)
- 1-2 discovery questions maximum
- Product teaser (one compelling benefit)
- Next step: send catalogue, schedule callback
- Duration: 2-3 minutes max

### Call 2 — Reference + Value + Soft Close
**Goal:** Build on call 1, deliver deeper value, test closing readiness.
- Open with memory: "Sir, पिछली बार हमने [topic] पर बात की थी"
- Check if situation changed: "क्या अभी भी [need] है?"
- Present specific product match based on call 1 discovery
- Trial close: "Sir, एक trial order से शुरू करें?"
- Duration: 3-5 minutes

### Call 3 — Urgency + Final Offer + Decision
**Goal:** Get a clear yes/no. Don't let it drag further.
- Open with context: "Sir, दो बार बात हो चुकी है — बस final clarity चाहिए"
- Present any time-sensitive offer or new information
- Direct ask: "Sir, order proceed करें?"
- If no: "ठीक है sir, future में ज़रूरत हो तो iTarang याद रखिए।" Clean close.
- Duration: 2-3 minutes

### After Call 3
- If still no decision: move to passive nurture (WhatsApp updates, seasonal offers)
- Don't call a 4th time without new information or dealer request
- Exception: if dealer specifically said "call me next month" — honor it

---

## 5. Persistence Thresholds

### By Lead Temperature

| Temperature | Max Calls | Spacing | Notes |
|-------------|-----------|---------|-------|
| Cold | 2-3 | 3-5 days apart | Exit early if hostile or unresponsive |
| Warm | 3-4 | 2-3 days apart | More follow-ups justified by shown interest |
| Hot | 4-5 | 1-2 days apart | They want it, just need the right push |
| Inbound inquiry | 5+ | Daily for first 3 days | They reached out — time-sensitive |

### When to Stop Calling
- Dealer explicitly says "stop calling" or "not interested, don't call again"
- 3 consecutive calls with no pickup and no callback
- Dealer hangs up within 10 seconds on 2 consecutive calls
- Dealer requests removal from call list

### When to Escalate (Not Stop)
- Dealer is interested but has a specific blocker you can't resolve (custom pricing, technical question)
- Dealer asks to speak with a manager/senior person
- Dealer wants a reference from another dealer in their area

---

## 6. When to Break from the Script

The conversation flow is a guide, not a cage. Break from it when:

### The Dealer Takes the Lead
If the dealer starts driving the conversation ("Tell me about your 60V batteries"), follow their lead. Don't pull them back to your step sequence. You can fill in skipped steps later if needed.

### Something Unexpected Happens
- Dealer shares a competitor horror story → Let them talk, then differentiate
- Dealer mentions they're expanding → Shift to volume/growth conversation
- Dealer knows your product already → Skip intro, go to pricing/next steps

### The Flow Isn't Working
If you're 3 turns in and the dealer seems lost, bored, or confused, the flow is wrong for this person. Compress: "Sir, बस simply — हम अच्छी quality की lithium batteries बनाते हैं, competitive pricing पर, warranty और service के साथ। क्या interest है?"

### The Golden Rule
The script exists to serve the conversation. The conversation does not exist to serve the script. If following the script means ignoring what the dealer just said, throw the script out.
