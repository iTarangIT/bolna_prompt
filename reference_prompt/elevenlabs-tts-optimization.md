# ElevenLabs Text-to-Speech Optimization Best Practices

Source: ElevenLabs Documentation (elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices)

## Number & Symbol Formatting

### Core Rule
Avoid writing numbers as digits or using symbols, especially with multilingual models. The number "1" is written identically in many languages but pronounced differently — writing it out removes ambiguity.

### Normalization Formats

| Type | Raw | Normalized |
|------|-----|-----------|
| Cardinals | 123 | "one hundred twenty-three" |
| Ordinals | 2nd | "second" |
| Currency | $45.67 | "forty-five dollars and sixty-seven cents" |
| Phone numbers | 123-456-7890 | "one two three, four five six, seven eight nine zero" |
| Decimals | 3.5 | "three point five" |
| Fractions | 2/3 | "two-thirds" |
| Abbreviations | Dr., Ave. | "Doctor", "Avenue" |
| Alphanumeric | 100km | "one hundred kilometers" |
| URLs | elevenlabs.io/docs | "eleven labs dot io slash docs" |
| Percentages | 40% | "forty percent" |

### Normalization Methods

**System Prompt Method (default)**: Instruct the LLM to write numbers and symbols as words before TTS processing. No additional latency but models may occasionally fail.

**ElevenLabs Normalizer**: Applies normalization after LLM generation, before TTS. More reliable, minor latency overhead. Better for compliance/audit since transcripts stay readable.

## Pronunciation Control

### SSML Phoneme Tags (Flash v2 and English v1 only)
- CMU Arpabet (recommended): `ph="M AE1 D IH0 S AH0 N"` for Madison
- IPA: `ph="ˈæktʃuəli"` for actually
- Ensure correct stress marking for multi-syllable words.

### Alias Tags (for Multilingual v2)
```xml
<lexeme>
  <grapheme>Claughton</grapheme>
  <alias>Cloffton</alias>
</lexeme>
```

### Pronunciation Dictionaries
Upload .PLS or .TXT files for consistent term pronunciation. Searches are case-sensitive.

## Pauses and Pacing

### Break Tags (v2 & v2.5 only)
`<break time="1.5s" />` for pauses up to 3 seconds. Too many break tags can cause instability.

### Natural Pause Techniques
- Dashes (— or –) for short pauses
- Ellipses (...) for hesitant tones
- Standard punctuation provides natural rhythm

## Common Pitfalls & Solutions

| Issue | Solution |
|-------|----------|
| Mispronounced names/terms | Use phoneme tags, alias tags, or pronunciation dictionaries |
| Symbol/number errors | Spell out numbers, remove symbols, use normalized text |
| Inconsistent pauses | Use exact SSML syntax or natural punctuation |
| Robotic delivery | Use narrative/scriptwriting style for tone guidance |
| Multilingual confusion | Write out numbers in the target language's words |

## Key Takeaway for Voice Agent Prompts

1. Always spell out numbers in word form in the system prompt.
2. Use "Rupees" not "₹" or "Rs."
3. Phone numbers digit by digit with commas for pausing.
4. Avoid abbreviations — expand them.
5. Use dashes and ellipses for natural pacing.
6. Keep responses short — long agent turns sound unnatural in voice.
