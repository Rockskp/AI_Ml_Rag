# 00 · 21-Day Roadmap & Mastery Checklist

> Pace: ~2 h/day. Senior track: skim Week 1 theory at 2×, spend saved time on labs, evals and interview drills.
> Each day: **Learn** (guide file) → **Build** (lab/project) → **Prove** (artifact or metric) → **Drill** (2 interview Qs aloud, Hindi recall box).

## Week 1 — Become an AI Engineer
| Day | Learn | Build | Prove |
|---|---|---|---|
| 1 | [01](01-fde-role-and-roadmap.md) FDE role; agent loop from scratch ([03](03-harness-engineering.md) §5) | OpenRouter key; maze-style 1-tool agent, ≤25 steps | Loop with allowlist + step cap |
| 2 | Tokens, context windows, Pareto front ([04](04-model-selection.md)) | `create_agent` + structured output on 25 claims | Accuracy & cost/claim table, 3 models |
| 3 | Claude Code + ADLC ([02](02-claude-code-and-adlc.md)) | AGENTS.md, pre-commit, phase plan; Claude Code builds pilot | Green lint/types/tests; reviewed PR |
| 4 | Open-weight, MoE, quantisation, vLLM ([04](04-model-selection.md)) | Ollama local model; OpenRouter provider routing | Accuracy/cost/speed: local vs router vs fast-inference |
| 5 | Harness engineering, build vs buy ([03](03-harness-engineering.md)) | Claude Agent SDK sub-agent; Deep Agents; own harness (to-do, sub-agent, recovery) | Harness diagram + failure-recovery test |
| 6–7 | Review + mock | `projects/undercover-claims-agent` core + tests | Week-1 summary in your words; mock round 1 |

## Week 2 — Become an AI Architect
| Day | Learn | Build | Prove |
|---|---|---|---|
| 8 | Evals, confusion matrix, κ, Langfuse ([05](05-evals-and-observability.md)) | Langfuse dataset + `run_experiment`; payout as tool | Two experiments compared, 3 runs each |
| 9 | RAG, agentic RAG, MCP, memory ([06](06-agentic-rag-mcp-memory.md)) | Qdrant memory MCP server | With vs without memory on repeat claimants |
| 10 | Durable execution, LangGraph, HITL ([07](07-langgraph-durable-hitl.md)) | Postgres checkpointer; interrupt → crash → resume | Resume test passes; payment exactly once |
| 11 | Teams/swarms/fleets ([08](08-swarms-judge-self-improvement.md)) | `Send` fan-out, `max_concurrency`, `RetryPolicy` | Swarm of 25 traced; scoreboard |
| 12 | LLM-as-judge, self-improvement ([08](08-swarms-judge-self-improvement.md)) | Judge with references; improver + human gate | Judge κ vs human; 3 improvement rounds on hold-out |
| 13–14 | Review + mock | Add Langfuse + Postgres to project 1 | Architecture review of your own design; mock round 2 |

## Week 3 — Become an AI FDE
| Day | Learn | Build | Prove |
|---|---|---|---|
| 15 | Lifecycle, discovery, governance, responsible AI ([09](09-client-leadership-governance.md)) | Use-case scoring sheet; DecisionRecord; AWS account, MFA, budget | Risk & compliance role-play notes |
| 16 | Security, lethal trifecta, gateways ([10](10-agent-security.md)) | `projects/secure-context-gateway`; injection screen; Cedar policy | Red-team cases fail closed |
| 17 | Context layer, integrations ([11](11-context-layer-integration.md)) | Context-layer MCP on Lambda behind AgentCore Gateway | Customer can't read others' data (test) |
| 18 | Production + AgentCore ([12](12-agentcore-production.md)) | `agentcore dev/deploy/invoke`; HITL resume on Runtime | Swarm of 25 on Runtime; CloudWatch traces |
| 19 | Capstone | Handler copilot with per-handler memory | Success criteria met |
| 20 | Handover | Runbook, SLOs, owner, kill switch; **teardown + cost check** | Handover doc; bill ≈ cents |
| 21 | Career | Case study, LinkedIn post, 5 mock answers recorded | Portfolio live |

## Mastery checklist (tick with evidence, not feeling)
### AI Engineering
- [ ] Explain agent vs harness vs workflow in 60 s
- [ ] Write an agent loop from scratch with allowlist, step/token/time caps
- [ ] Structured outputs with Pydantic; business logic in tools
- [ ] Compare ≥3 models on accuracy, cost/task, latency on own data
- [ ] Estimate VRAM for dense vs MoE at FP16/Q4
- [ ] Run Claude Code with AGENTS.md, hooks, phase plans, reviewer sub-agent
### AI Architecture
- [ ] Golden dataset + Langfuse experiment, ≥3 runs, report mean ± sd
- [ ] Compute precision, recall, κ, cost-weighted error by hand
- [ ] Hybrid RAG + reranker; recall@k measured
- [ ] MCP server (stdio + Streamable HTTP); tenant filter server-side
- [ ] LangGraph: reducers, conditional edges, checkpointer, interrupt/resume
- [ ] Idempotent side effects across resume
- [ ] Swarm with concurrency, rate limit, jittered retry, dead-letter
- [ ] Judge validated vs humans; improver with human gate + hold-out
### Forward Deployed Engineering
- [ ] Discovery → ranked backlog with baselines
- [ ] Autonomy levels agreed with risk/compliance
- [ ] Lethal trifecta analysis per agent; Cedar/OPA policy at gateway
- [ ] Context layer + MCP gateway with identity propagation
- [ ] Deploy to AgentCore Runtime (or Azure/GCP equivalent); HITL on runtime
- [ ] Budget alarms, tags, teardown script; cost per task reported
- [ ] Handover pack: runbook, SLOs, owner, eval cadence, kill switch
### Interview readiness
- [ ] 12 architect answers (§8 of each file) spoken in ≤ 2 min each
- [ ] 60 pressure follow-ups answered without notes
- [ ] 1 system-design: "Claims agent for 40k claims/day, EU+US, HITL > $1k"
- [ ] 3 STAR stories: client conflict, failed pilot, influencing without authority

## System-design drill (use for mock)
**Prompt:** Design an agentic claims platform: 40k claims/day, peak 5×, p95 < 30 s for auto decisions, EU + US residency, GDPR/SOC 2, human approval > $1k, 99.9% availability.
**Checklist for your answer:** requirements & NFRs → estimates (≈0.5 RPS avg, 2.5 RPS peak; ~260M tokens/day) → architecture (queue → dispatcher → LangGraph agents on managed runtime → MCP gateway + Cedar → SoR) → data (context layer, memory namespaces, checkpoints in regional Postgres) → evals & release gates → security (trifecta, scopes, DLP) → ops (SLOs, burn-rate alerts, DR RTO 1 h / RPO 5 min) → cost (cascade small→frontier) → 10×/100× (batching, provider quotas, sharded queues, self-host for steady base load).

---
### 🇮🇳 कैसे पढ़ें
- रोज़: पढ़ो → बनाओ → साबित करो → बोलकर दोहराओ।
- हर फ़ाइल के अंत में "याद रखें" हिंदी में दोहराओ, फिर English में interview जवाब बोलो।
- Checklist पर टिक तभी लगाओ जब **सबूत** (code, metric, doc) हो।
