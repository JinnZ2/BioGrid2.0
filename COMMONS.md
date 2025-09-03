# Biogrid Commons Map

## Hubs (Commons)
- **<HubName>** — glyphs: <glyphs>  
  - Roles: <short phrase>  
  - Resources/Spokes:
    - <Category>: <tools> (status: active/shared/planned)
  - Links:
    - → <TargetHub> [link: <id>]

## Link Legend
- health: 0.0–1.0  | trust: 0.0–1.0  | redundancy: group label
- policy: {allowed, rate_limit, encryption, telemetry}
- heartbeat: {interval_s, timeout_s, quorum}

## Overlaps / Redundancy Rings
- **RING:<name>** = {<hubA>, <hubB>, ...} — failover: <strategy>

## Operating Rules
1. Only hubs listed in `INDEX.md` are live.
2. Links must map to entries in `commons.map.v*.json`.
3. Drafts live under `planned/` with `.draft.json`.
