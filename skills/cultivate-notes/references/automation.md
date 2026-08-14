# Scheduled workflows

Create, update, inspect, or remove an automation only when the user asks. Use the product's automation capability; do not represent a cron snippet or prose schedule as an active automation.

## Safe recurring prompt

Adapt repository path, cadence, and batch size, then use a prompt with these constraints:

```text
Use $cultivate-notes in <absolute-repository-path>. Validate the configuration, scan for unread inputs, and cultivate at most <N> primary notes. Access sources only through the bundled claim gate. Write timestamped, source-backed proposals under the configured review path, register each proposal, and report corrections and review flags. Never publish, archive, modify raw notes, access excluded/private material, or reset processing state. If no unread notes exist, report that without rereading prior inputs.
```

Default to a small batch, usually one to three notes. Scheduled runs may research, propose visualizations, and create review artifacts. They must not:

- archive or move raw sources;
- publish to the served documentation tree;
- change exclusions or privacy markers;
- delete or reset the ledger;
- infer approval from silence or from a previous run.

If a run lacks network access or a required file parser, preserve the proposal boundary and add a timestamped manual-review or potentially-outdated marker. Do not bypass the claim copy to make a parser work.
