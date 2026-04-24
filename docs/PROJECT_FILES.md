# Documentation File Map

This file defines which documentation files are authoritative, what each file owns, and how to keep repository documentation consistent.

## Canonical Documentation Set

| File | Purpose | Ownership |
|------|---------|-----------|
| README.md | Project entry point: purpose, outcomes, capacities, discoveries | Project maintainer |
| docs/INDEX.md | Navigation by role and task | Project maintainer |
| docs/METHODOLOGY.md | Harmonization methodology and quality framework | Methodology owner |
| docs/inputs.md | Manual dataset onboarding and provenance requirements | Data ingestion owner |
| docs/AUTOMATED_DISCOVERY_README.md | Automated discovery workflow and operational controls | Pipeline automation owner |
| docs/DATA-PROCESSING/SCHEMA.md | Canonical harmonized data structure | Schema owner |
| docs/DATA-PROCESSING/RULES.md | Rule-based inference and normalization logic | Rules owner |
| docs/DATA-PROCESSING/CODEBOOK.md | Controlled values, severity scales, coding reference | Clinical mapping owner |
| .claude/CLAUDE.md | AI assistant project context and guardrails | Repository maintainer |

## Documentation Contracts

1. No unresolved merge markers are allowed in documentation files.
2. Paths must reflect the actual repository layout.
3. Do not duplicate long technical sections across files.
4. Keep one source-of-truth per topic, then link from index docs.
5. Update tests/docs references together when behavior changes.

## Purpose, Process, Outcomes, Capacities, Discoveries Coverage

The documentation set is intentionally organized around five mandatory dimensions:

- Purpose: why this harmonization workspace exists.
- Process: how data flows from input through normalized output.
- Outcomes: what results are expected from the pipeline.
- Capacities: what the current architecture can support.
- Discoveries: what kinds of research insights this workspace enables.

Coverage map:

| Dimension | Primary Files |
|-----------|---------------|
| Purpose | README.md, docs/METHODOLOGY.md |
| Process | docs/METHODOLOGY.md, docs/inputs.md, docs/AUTOMATED_DISCOVERY_README.md |
| Outcomes | README.md, docs/METHODOLOGY.md |
| Capacities | README.md, docs/DATA-PROCESSING/* |
| Discoveries | README.md, docs/METHODOLOGY.md |

## Change Workflow For Docs

1. Edit the source-of-truth file for the changed topic.
2. Update docs/INDEX.md links or reading paths if navigation is affected.
3. Update README.md if project-facing scope, claims, or status changed.
4. Run tests if schema/rules assumptions were changed.
5. Re-scan docs for merge markers and inconsistent paths.

## Legacy and Drift Control

If a new doc is added, it must:

1. Have a unique purpose not already covered by an existing canonical file.
2. Be listed in docs/INDEX.md.
3. Be listed in this file with ownership and maintenance intent.
