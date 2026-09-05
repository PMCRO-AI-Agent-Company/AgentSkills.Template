# capabilities

Registry of stable capability *contracts* (not tool names).

Do not invent capability definitions ahead of real wiring.  
Empty provider lists are required until a real integration is verified.

| id | status | default | file |
|----|--------|---------|------|
| `hyperlight-codeact` | planned (preview packages) | **off** | `hyperlight-codeact.yaml` |

Enablement requires explicit config (`Hyperlight:CodeAct:Enabled` or `PMCRO_CAPABILITY_HYPERLIGHT_CODEACT`) and must not register CodeAct tools when disabled.

See `.pmcro/design/PLAN-align-apphost-agui-hyperlight.md` and `CHECKLIST-agui-hyperlight.md`.
