# Gemini 3.1 Architecture & Deployment Routing

## TL;DR

Google DeepMind's Gemini 3.1 multi-tiered architecture dictates non-linear, workload-specific routing across **Pro**, **Flash**, and **Flash-Lite** variants. Selection strictly triages reasoning depth, time-to-first-token (TTFT) latency, and token throughput economics.

## Workload Routing

| Model Variant | Target Workload | Model ID |
| --- | --- | --- |
| **Pro** | Advanced autonomous reasoning | gemini-3.1-pro-preview |
| **Flash** | Standard processing | gemini-3-flash-preview |
| **Flash-Lite** | Ultra-low-latency asynchronous processing | gemini-3.1-flash-lite-preview |

## Operational Controls

Granular configuration parameters affecting performance and pricing:

- **Thinking Levels:** Mandatory and adjustable
- **Media Resolution:** Dynamic scaling
- **Thought Signatures:** Encrypted
- **Temperature Constraints:** Immutable
