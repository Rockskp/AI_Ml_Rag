# AI FDE & Agentic AI Architect — Principal Study Guide (EN + हिंदी)

> Status: DRAFT study material · Created 2026-11-26 · Based on the 3-week, 124-lecture course syllabus "AI FDE: The Forward Deployed Engineer & Agentic AI Architect".
> Code snippets in guide files are illustrative (not executed). Code in `projects/` is tested (see each README).

## Start here
1. [00 · 21-day roadmap & mastery checklist](00-roadmap-and-checklist.md)

## The 12 outcomes
Each file: senior concept · internals · enterprise use case · Mermaid · code · trade-offs · blind spots · architect answer · 9 interview Qs · 5 pressure follow-ups · 🇮🇳 Hindi recall.

| # | Outcome | Week |
|---|---|---|
| 01 | [AI Architect & FDE skills and roadmap](01-fde-role-and-roadmap.md) | 1 |
| 02 | [Claude Code & the ADLC, staying accountable](02-claude-code-and-adlc.md) | 1 |
| 03 | [Harness engineering: LangChain, Deep Agents, Claude Agent SDK](03-harness-engineering.md) | 1 |
| 04 | [Frontier vs open-weight vs local LLMs](04-model-selection.md) | 1 |
| 05 | [Evals & observability in Langfuse](05-evals-and-observability.md) | 2 |
| 06 | [Agentic RAG over MCP, long-term memory](06-agentic-rag-mcp-memory.md) | 2 |
| 07 | [LangGraph: durable state, crash recovery, HITL](07-langgraph-durable-hitl.md) | 2 |
| 08 | [Swarms, LLM-as-judge, self-improvement](08-swarms-judge-self-improvement.md) | 2 |
| 09 | [Leading clients: discovery → governance → handover](09-client-leadership-governance.md) | 3 |
| 10 | [Agent security: injection, lethal trifecta, gateways](10-agent-security.md) | 3 |
| 11 | [Context layer & MCP gateway](11-context-layer-integration.md) | 3 |
| 12 | [Production on AWS Bedrock AgentCore](12-agentcore-production.md) | 3 |

## Portfolio projects (tested)
| Project | Shows | Covers |
|---|---|---|
| [`projects/undercover-claims-agent`](../../projects/undercover-claims-agent/) | LangGraph claims workflow: injection screen, deterministic payout, HITL interrupt > $1k, crash-resume, idempotent payment, κ + cost-weighted eval, optional LLM decider | 03, 05, 07, 09, 10 |
| [`projects/secure-context-gateway`](../../projects/secure-context-gateway/) | MCP context-layer server: token identity, Cedar-style default-deny/forbid-wins policy, PII masking, tool-output quarantine, audit log | 06, 10, 11, 12 |

## Verify before quoting
- Model names/prices in the syllabus (e.g., GPT-6, DeepSeek V4.1) are course-time; check current.
- Python `mcp` SDK 2.x renamed FastMCP → `MCPServer`.
- AgentCore CLI flags change; run `agentcore --help`.
