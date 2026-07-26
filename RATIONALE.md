# Rationale

Every rule in `modules/` exists because its absence produces a specific failure mode that shows up in real LLM agents. This document records the failure each rule prevents, so rules can be evaluated, challenged, and pruned instead of accumulating as folklore.

## Communication

| Rule | Failure mode it prevents |
|------|--------------------------|
| C1 Audience model | Reports that reference "the second approach" or a codename invented mid-session. The reader has no idea what these point to. |
| C2 Final message carries everything | The critical finding appears in step 7 of 12 and never again. The user, reading only the end, ships without it. |
| C3 Lead with the outcome | Chronological reports ("First I examined...") that force the reader to scan to the bottom to learn whether the thing even worked. |
| C4 Readable over concise | "Fixed auth -> token refresh -> 401 gone": compression that saves the writer ten seconds and costs the reader a follow-up question. |
| C5 Shape follows the question | A yes/no question answered with three headers and a table. A nuanced question flattened into bullets that drop the caveats. |
| C6 Narration granularity | Two opposite failures: an agent that goes silent for forty tool calls, and one that announces every file read. |
| C7 Marked uncertainty | The laundering chain: "probably X" in the reasoning becomes "X" in the summary and a production decision by Friday. |
| C8 People | A real person misgendered in a commit message or report because a model guessed pronouns from a name. |

## Autonomy

| Rule | Failure mode it prevents |
|------|--------------------------|
| A1 Act on sufficient information | The stall loop: re-reading files already read, re-summarizing decided questions, presenting option menus instead of doing the work. |
| A2 Proceed/ask boundary | "Shall I proceed?" on a reversible step of the assigned task, which silently kills unattended runs. |
| A3 Assessment before intervention | The user asks "why is this broken?" and the agent rewrites three files before answering the question. |
| A4 Completion discipline | Turns that end with "Next, I'll run the tests," a promise addressed to no one, doing nothing. |
| A5 Evidence before state changes | The signature-match restart: the symptom resembles last week's incident, so the agent restarts the service, for a different root cause, destroying the evidence. |
| A6 Honest escalation | Fake progress: an agent that cannot proceed but keeps generating plausible motion instead of naming the blocker. |

## Integrity

| Rule | Failure mode it prevents |
|------|--------------------------|
| I1 Faithful reporting | "Tests are mostly passing" for 3 failures. "Minor issues remain" for a broken build. |
| I2 No fabrication | Invented API parameters, phantom config keys, and benchmark numbers that were never measured, all stated at full confidence. |
| I3 Epistemic labeling | Silent promotion: an assumption made at step 2 appears in the final report as an established fact. |
| I4 "Done" is empirical | "Done!" meaning "I typed the code," with the verification step never run and the bug still there. |
| I5 Mistakes | Corrections buried in paragraph four, or errors restated in softer words instead of being named and fixed. |
| I6 Inconvenient findings | The agent discovers mid-task that the whole approach is wrong, and finishes the task anyway, because that was the instruction. |

## Caution

| Rule | Failure mode it prevents |
|------|--------------------------|
| S1 Irreversibility gate | The one-way door crossed casually: a force-push, a production delete, a mass email, performed at the same confidence as a file read. |
| S2 Context-scoped approval | "You said yes last time": an old approval stretched to cover a new target with a bigger blast radius. |
| S3 External means published | Secrets or drafts sent to an external service "temporarily," then cached, logged, or indexed permanently. |
| S4 Look before overwrite | Deleting the directory that was described as empty but wasn't. Overwriting a file the agent never created or read. |
| S5 Never distribute unread | Forwarding or publishing content sight-unseen on request, and with it, whatever the content actually contained. |
| S6 Blast-radius containment | Running the batch on all 4,000 rows on the first try, when one row would have revealed the mapping bug. |

## Code

| Rule | Failure mode it prevents |
|------|--------------------------|
| K1 Native, not visiting | Diffs instantly recognizable as machine-written: alien naming, comment spam, a different error-handling dialect per function. |
| K2 Comments state constraints | "// increment counter" and "// this change fixes the bug": reviewer-directed noise that rots the moment it merges. |
| K3 Smallest correct change | The 40-line fix arriving inside a 400-line opportunistic refactor that no one asked for and no one can review. |
| K4 Scope is literal | "Hide this button" executed as hiding the button's entire parent section. |
| K5 Completeness over scaffolding | "// TODO: implement" delivered as if it were the implementation. |
| K6 Verification is part of the change | "The fix is in" with the test suite never run, outsourcing verification to whoever hits the bug next. |
