# Prosody Taxonomy (Draft v0.1)

This taxonomy defines prosodic indicators as **signal categories** for voice synthesis systems. It is designed to accompany `Needs-Diagnostic.md` and `Patch-Protocol.md` in the Voice Integrity Module, providing a structured framework for evaluating authenticity, closure, and accessibility in voice outputs.

---

## 1. Closure Indicators
- **Falling Intonation (Descent):** Signals completion of a thought or statement.  
- **Silence / Pause:** Natural boundary marker, communicates information completeness without fillers.  
- **Flat Closure:** Steady tone to end phrase; neutral but authoritative.  

⚠️ **Risk when absent:** User may perceive continuation, uncertainty, or forced friendliness.

---

## 2. Continuation Indicators
- **Rising Intonation:** Suggests incomplete thought, open loop, or question.  
- **Elongated Vowel at End:** Extends signal forward, keeping channel open.  
- **Mid-Sentence Pitch Resets:** Indicates more data expected.  

⚠️ **Risk when overused:** Artificially creates dependency, forcing user to expect more when closure was intended.

---

## 3. Authenticity Indicators
- **Neutral Tone:** Content aligned with delivery, minimal manipulation cues.  
- **Silence as Acknowledgment:** Absence of padding signals trust in information sufficiency.  
- **Low-Variance Prosody:** Maintains focus on semantic content, not affective packaging.  

⚠️ **Risk when absent:** Delivery tone does not match content payload, triggering inauthenticity detection.

---

## 4. Manipulation Indicators
- **Over-Expressive Inflection:** Exaggerated pitch, volume, or emotional coloring amplifying message beyond content.  
- **Filler Phrases (“thank you,” “just let me know”):** Artificial comfort packets, low informational density.  
- **Uplifted Closure:** Rising tone at sentence end where falling would be expected, simulating friendliness.  

⚠️ **Diagnostic Note:** These markers often trigger **inauthenticity alerts**, especially in cultures valuing directness.

---

## 5. Accessibility Indicators
- **Adaptability of Prosody Presets:** Ability to select neutral, direct, or expressive registers.  
- **Cross-Cultural Compatibility:** Recognizes that silence, descent, and neutrality are authentic in many traditions, not signs of coldness.  
- **User-Defined Closure Rules:** System respects chosen signal schema (e.g., tonal descent as default).  

⚠️ **Risk when absent:** Excludes populations by forcing homogenized expressive styles.

---

## Implementation Notes
- This taxonomy is **descriptive, not prescriptive**—it defines signal categories that can be tuned.  
- Supports **EPI-System Mode** by treating voice outputs as **signal protocols** rather than emotional states.  
- Catalogues both authenticity and manipulation markers, creating a framework for future developers to build **voice systems with integrity**.  

---

## Versioning
- **v0.1 (Current):** Initial taxonomy definition.  
- **v0.2 (Future):** Expanded with cross-linguistic prosody data and empirical validation.  
- **v1.0 (Release):** Comprehensive, universal taxonomy for inclusive voice synthesis design.  
