# laws

Fixed rule IDs the colony's roles and mechanics are expected not to violate.

A law is an ID + machine-readable rule name. It is **not** prose policy (see `../policies/`) and not enforcement code (see `../runtime/`).

These laws are the non-negotiable invariants of a PMCR-O colony:

| ID | Rule | Practical meaning |
|----|------|-------------------|
| L-EVIDENCE | completion_requires_evidence | No completion without attached evidence |
| L-CHECKER-GATE | checker_must_pass_before_completion | Reflector may not seal without Checker PASS |
| L-STATE-MEMORY | workflow_state_is_not_shared_memory | State and memory are separate stores |
| L-AGENT-MEMORY | agent_memory_is_scoped_to_agent | One agent's memory is not another's |
| L-CAPABILITY | agents_use_skills_and_tools_for_capabilities | Capabilities are exercised through declared skills/tools |
| L-ORCHESTRATION | orchestrator_owns_routing_not_domain_implementation | Orchestrator routes; it does not implement domain work |
| L-RESEARCH | version_sensitive_decisions_require_current_authoritative_evidence | Do not rely on stale knowledge for version-sensitive choices |
| L-PLUGIN-ISOLATION | plugin_skills_require_active_binding_envelope_or_open_cycle_before_TYPE1 | State-changing (TYPE1) mutations need an open cycle / binding |
| L-OUTPUT-CONTRACT | governed_results_must_satisfy_the_runtime_output_contract | Every governed result carries the required envelope |

Laws are stable. Policies may change posture; laws do not.
