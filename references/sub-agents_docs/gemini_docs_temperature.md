# Gemini Temperature & Decoding Optimization Guide

## TL;DR

- **Core Pipeline:** Temperature Scaling $\to$ Top-K Filtering $\to$ Top-P Filtering $\to$ Final Sampling.
- **Gemini 3 Constraint:** **MUST** remain at $T=1.0$. Tuning causes reasoning collapse and infinite loops.
- **Determinism:** $T=0.0$ (Greedy Decoding) is "mostly deterministic" but limited by hardware floating-point non-associativity and parallelization noise.
- **Optimal Ranges:** Factual/Code ($0.0-0.3$), Creative/Ideation ($0.7-1.5$).

## 1. Mathematical Foundation

The temperature parameter ($T$) scales raw logits ($z_i$) within the softmax function to reshape the probability distribution ($P_i$):

$$P_i = \frac{e^{z_i / T}}{\sum_{j=1}^{K} e^{z_j / T}}$$

| Value | Effect | Result |
| :--- | :--- | :--- |
| **$T = 1.0$** | No change to logits. | Default; preserves model's organic confidence. |
| **$T < 1.0$** | Amplifies logit differences. | "Sharper" distribution; higher confidence/determinism. |
| **$T > 1.0$** | Compresses logit differences. | "Flatter" distribution; higher diversity/creativity. |
| **$T \to 0$** | Approaches Greedy Decoding. | Probability of max logit $\to 1.0$. |
| **$T \to \infty$** | Approaches Uniform Distribution. | All tokens become equally probable. |

## 2. Decoding Pipeline Sequence

Gemini applies heuristics in a strict chronological order:

1. **Temperature Scaling:** Reweights all tokens; no removals.
2. **Top-K Filtering:** Hard truncation. Retains top $K$ tokens, discards the rest. Renormalizes.
3. **Top-P (Nucleus) Sampling:** Dynamic trimming. Retains tokens until cumulative probability $\ge P$. Renormalizes.
4. **Final Sampling:** Weighted random selection from the surviving pool.

*Note: High Top-P often renders Top-K obsolete if the nucleus is reached before $K$ tokens.*

## 3. Determinism Limitations at $T=0.0$

Absolute bit-for-bit reproducibility is not guaranteed due to:

- **Floating-Point Precision:** Rounding errors in deep layers can flip logit ranks.
- **Parallelism (TPU/GPU):** Floating-point addition is non-associative; $(A+B)+C \neq A+(B+C)$. Execution order varies.
- **Software Libraries:** cuDNN may select different algorithms based on transient hardware state.
- **Tie-Breaking:** Equal logits rely on non-deterministic heuristics or unseeded memory.

## 4. Model Generation Constraints

| Generation | Models | Range | Default | Recommendation |
| :--- | :--- | :--- | :--- | :--- |
| **Gemini 1.0/1.5/2.0** | Pro, Flash, Nano, Lite | $0.0 - 2.0$ | $1.0$ | **Tune freely.** Use $T < 1.0$ for precision, $T > 1.0$ for creativity. |
| **Gemini 3** | Pro, Flash, Image | $0.0 - 2.0$ | $1.0$ | **LOCK AT 1.0.** Tuning causes looping and reasoning collapse. |

### Gemini 3 Reasoning Control

Since $T$ is locked, use `thinking_level` to modulate depth:

- **Minimal/Low:** Low latency, simple instructions.
- **Medium:** Balanced.
- **High:** Maximum depth (default); higher first-token latency.

## 5. Optimization Strategies (Tunable Models)

### Factual / Extraction / Code ($T: 0.0 - 0.3$)

- **Goal:** High precision, strict formatting (JSON/Code).
- **Action:** Lower $T$ to force statistical verification.
- **Tip:** If output is too repetitive, increase to $0.2-0.3$ for fluidity.

### Creative / Ideation ($T: 0.7 - 1.5$)

- **Goal:** Diversity, unexpected conceptual links.
- **Action:** Elevate $T$ to unlock diverse syntax.
- **Constraint:** Pair high $T$ (e.g., $1.2$) with restrictive Top-P (e.g., $0.9$) to filter "garbage tokens."

## 6. API Implementation (`GenerationConfig`)

```json
{
  "generation_config": {
    "temperature": 0.3,
    "topP": 0.95,
    "topK": 40,
    "maxOutputTokens": 1024,
    "stopSequences": ["\n\n"],
    "candidateCount": 1
  }
}
```

### SDK Nuances

- **Go SDK:** Requires explicit pointers: `genai.Ptr[float32](0.5)`.
- **Elixir (gemini_ex):** Uses keyword lists directly.
- **Specialized Models:** Image/Video models (Imagen/Veo) may restrict $T$ to $1.0$ or bypass it for deterministic noise control.

## 7. Multimodal Costs

- **Image:** `media_resolution_high` = 1,120 tokens.
- **PDF:** `media_resolution_medium` = 560 tokens/page.
- **Video:** 70 tokens/frame (Low/Med) or 280 tokens/frame (High/OCR).
- **Pricing:** Gemini 3.1 Flash Image Preview ($60/1M output tokens). Batch API reduces cost by 50%.
