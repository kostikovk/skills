# Native telemetry capture

Read with the [measurement table](execution-evidence.md#native-telemetry-and-coverage). Set `helper` to the receipt helper as in [Local execution evidence](execution-evidence.md).

Check the installed version/help and project permissions first. These examples do not grant additional tool permissions or select a model:

```sh
codex exec --json -C /path/to/project 'Read the accessible plan skill and prepare the requested ticket' > /tmp/planning-native.jsonl
claude -p 'Read the accessible code-change skill and implement the approved ticket' --output-format stream-json --verbose > /tmp/development-native.jsonl
python3 -B "$helper" native /tmp/pricing-plan --provider codex --source /tmp/planning-native.jsonl
python3 -B "$helper" native /tmp/pricing-dev --provider claude --source /tmp/development-native.jsonl
```

CLI flags/capabilities are documented in [Codex noninteractive mode](https://learn.chatgpt.com/docs/non-interactive-mode) and [Claude programmatic execution](https://code.claude.com/docs/en/headless). Do not automatically start another provider process from inside its own run. A launcher/operator imports the completed outer capture and regenerates the report. Provider import retains raw bytes and extracts exposed session, model(s), usage and estimated cost. It does not infer unexposed models, estimate cost from token pricing or sum conversation totals across imports. Byte-identical imports are rejected; overlapping/resumed captures still require operator reconciliation. Partial/failed streams remain raw evidence with unavailable fields.
