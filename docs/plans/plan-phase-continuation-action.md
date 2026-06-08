# Plan Phase Continuation GitHub Action

> **Goal:** Create a GitHub Actions workflow that detects when a merged PR
> introduces a new plan or completes a phase of an existing multi-phase plan
> in `docs/plans/`, identifies the first incomplete phase, and uses the
> Copilot CLI to directly delegate execution of that phase — so that
> multi-phase plans start automatically on merge and advance continuously
> without manual handoff or intermediate issues.

---

## Table of Contents

1. [Current State](#1-current-state)
2. [Desired Behavior](#2-desired-behavior)
3. [Feature Gap Analysis](#3-feature-gap-analysis)
4. [Implementation Phases](#4-implementation-phases)
   - [Phase 1: Plan Parsing Library](#phase-1-plan-parsing-library-priority-high)
   - [Phase 2: PR-to-Plan Linking Convention](#phase-2-pr-to-plan-linking-convention-priority-high)
   - [Phase 3: Core Workflow — Detect & Trigger](#phase-3-core-workflow--detect--trigger-priority-high)
   - [Phase 4: Copilot CLI Delegation](#phase-4-copilot-cli-delegation-priority-high)
   - [Phase 5: Safety Gates & Edge Cases](#phase-5-safety-gates--edge-cases-priority-medium)
   - [Phase 6: Documentation & Rollout](#phase-6-documentation--rollout-priority-medium)
5. [Plan File Format Assumptions](#5-plan-file-format-assumptions)
6. [Workflow YAML Design](#6-workflow-yaml-design)
   - [6.1 Trigger & Permissions](#61-trigger--permissions)
   - [6.2 Step-by-Step Pseudocode](#62-step-by-step-pseudocode)
   - [6.3 Draft Workflow YAML](#63-draft-workflow-yaml)
   - [6.4 Manual Dispatch & Testing](#64-manual-dispatch--testing)
7. [Security Considerations](#7-security-considerations)
8. [Test Plan](#8-test-plan)
9. [References](#9-references)

---

## 1. Current State

The repository has 15 plan documents in `docs/plans/`, several with multiple
implementation phases:

| Plan | Phases | Status |
|---|---|---|
| `udt-support.md` | 7 phases | Mixed (some ✅, some ⏳) |
| `documentation-plan.md` | 6 phases | Mixed (checkboxes in milestones) |
| `performance-improvement.md` | 5 phases | Multiple completed |
| `github-actions-testing-plan.md` | 4 phases | Partial |
| `python-rs-driver-support.md` | Multiple phases | Partial |

**Current workflow for advancing plans:**

1. A developer manually reads the plan to find the next incomplete phase
2. They manually create a PR implementing that phase
3. After merge they manually check if more phases remain
4. If yes, they repeat — or forget, and the plan stalls

**No automation exists to detect plan completion or trigger the next phase.**

The repository already has patterns for post-merge automation:

| Workflow | Pattern |
|---|---|
| `ci.yml` | `push` to master → semantic-release |

---

## 2. Desired Behavior

When a PR is merged to the default branch:

1. The workflow checks if the PR **introduces or modifies a plan file** in
   `docs/plans/` (by inspecting changed files), or **references** a plan file
   (via PR body or branch name convention)
2. If a plan is found, the workflow reads and parses the plan file
3. It identifies the first incomplete phase — this could be Phase 1 if the PR
   introduced the plan itself, or the next phase after the one just completed
4. If an incomplete phase is found, the workflow invokes the **Copilot CLI**
   to directly delegate execution of that phase, with a prompt like:
   *"Continue to phase N of plan docs/plans/\<name\>.md"*

**Key insight:** Merging a PR that introduces a new plan document is itself the
trigger to start Phase 1. No separate "kick-off" step is needed — the workflow
treats the plan PR merge the same as any phase-completing merge.

| Scenario | Result |
|---|---|
| PR merged, introduces a new plan file | Copilot CLI delegates Phase 1 (bootstrap) |
| PR merged, references plan, next phase exists | Copilot CLI delegates the next phase for implementation |
| PR merged, references plan, all phases complete | Comment on PR: "🎉 All phases of \<plan\> are complete!" |
| PR merged, no plan reference and no plan files changed | No action taken |
| PR merged, plan file not found | Warning comment on PR |
| PR closed without merge | No action taken |

---

## 3. Feature Gap Analysis

Legend:
- ✅ **Implemented** — working today
- 🔧 **Partial** — infrastructure exists but not fully exposed
- ❌ **Missing** — not yet implemented

| Feature | Status | Notes |
|---|---|---|
| Detect PR merge event | 🔧 | `push` to master triggers exist; need `pull_request: closed` with merge check |
| Detect plan files in PR changed files | ❌ | Need to inspect PR's changed files for `docs/plans/*.md` additions/modifications (bootstrap trigger) |
| Parse plan reference from PR | ❌ | No convention for linking PRs to plans |
| Read plan file from repo | 🔧 | `actions/checkout` already used in other workflows |
| Parse plan markdown for phases | ❌ | Need to extract phase headers and status markers |
| Identify next incomplete phase | ❌ | Need logic to scan phases for first non-✅ phase |
| Extract phase tasks for prompt | ❌ | Need to extract phase goal and task table for the Copilot CLI prompt |
| Invoke Copilot CLI to delegate task | 🔧 | Copilot CLI integration pattern can be reused |
| Handle "all phases complete" | ❌ | Post a congratulatory comment on the merged PR |
| Conventional plan-reference format | ❌ | Need a convention: `Plan: docs/plans/<name>.md` in PR body |

**Gap summary — automation pipeline:**
- Plan detection → inspect PR changed files for new/modified `docs/plans/*.md`
  files (bootstrap: starts Phase 1 when a plan is first merged)
- PR-to-plan linking → define a convention (`Plan: <path>` in PR body or
  branch name `plan/<plan-name>/phase-N`) for subsequent phase PRs
- Plan parsing → shell script or Python script that reads markdown, extracts
  `### Phase N:` headers and their ✅/❌ status
- Next-phase detection → find first phase header without ✅ in the header text
- Copilot CLI delegation → use `gh copilot` to delegate the next phase with
  a prompt like *"Continue to phase N of plan docs/plans/\<name\>.md — the
  phase goal is: \<goal\>. Tasks: \<task list\>"*

---

## 4. Implementation Phases

### Phase 1: Plan Parsing Library ✅

**Goal:** Create a reusable script that reads a plan markdown file and extracts
phase structure, status, and task tables.

| Task | Description | Status |
|---|---|---|
| 1.1 | Create `.github/scripts/parse-plan.py` — Python script that reads a plan `.md` file and outputs JSON with phase titles, status (complete/incomplete), and task content | ✅ |
| 1.2 | Support phase header formats: `### Phase N: Title ✅`, `### Phase N: Title (Priority: X)`, and `### Phase N: Title` | ✅ |
| 1.3 | Detect phase completion via ✅ in phase header **or** all tasks in the phase table having ✅ status | ✅ |
| 1.4 | Extract the task table (markdown) for each phase so it can be included in the delegation prompt | ✅ |
| 1.5 | Add unit tests for the parser in `.github/scripts/test_parse_plan.py` using `pytest` | ✅ |
| 1.6 | Test against real plan files: `udt-support.md`, `documentation-plan.md` | ✅ |

### Phase 2: PR-to-Plan Linking Convention ✅

**Goal:** Define and document the convention for linking a PR to a specific plan
and phase.

| Task | Description | Status |
|---|---|---|
| 2.1 | Define the linking convention: PR body must contain a line matching `Plan: docs/plans/<name>.md` (case-insensitive) | ✅ |
| 2.2 | Optionally support `Phase: N` in the PR body to indicate which phase this PR completes | ✅ |
| 2.3 | Support branch-name convention as fallback: `plan/<plan-name>/phase-N` (e.g., `plan/udt-support/phase-3`) | ✅ |
| 2.4 | Add a PR template snippet (`.github/PULL_REQUEST_TEMPLATE.md` or amendment) documenting the convention | ✅ |
| 2.5 | Update `CONTRIBUTING.md` with the plan-linking convention | ✅ |

### Phase 3: Core Workflow — Detect & Trigger ✅

**Goal:** Create the GitHub Actions workflow that triggers on PR merge, detects
plan references (or new plan files in changed files), parses the plan, and
identifies the next phase.

| Task | Description | Status |
|---|---|---|
| 3.1 | Create `.github/workflows/plan-continuation.yml` with `pull_request: types: [closed]` and `workflow_dispatch` triggers | ✅ |
| 3.2 | Add merge guard: run if manually dispatched OR if the PR was actually merged | ✅ |
| 3.3 | **Bootstrap detection:** Use GitHub API to list PR changed files and find any `docs/plans/*.md` additions/modifications — this starts Phase 1 when a plan is first merged | ✅ |
| 3.4 | Extract plan reference from PR body (`Plan: docs/plans/<name>.md`) and optionally from branch name (for subsequent phase PRs) | ✅ |
| 3.5 | Merge detected plan files: combine plans found via changed files (3.3) and PR body/branch (3.4), deduplicate | ✅ |
| 3.6 | Handle `workflow_dispatch` inputs: use `inputs.plan_file` and `inputs.phase` directly, bypassing PR detection | ✅ |
| 3.7 | Checkout the repo and run `parse-plan.py` on each detected plan file | ✅ |
| 3.8 | Determine which phase was completed (from `Phase: N` in PR body, `inputs.phase`, or infer from latest ✅ phase; for bootstrap PRs, no completed phase — start at Phase 1) | ✅ |
| 3.9 | Identify next incomplete phase from parser output | ✅ |
| 3.10 | If no plan reference found and no plan files in changed files, exit silently (success, no-op) | ✅ |

### Phase 4: Copilot CLI Delegation ✅

**Goal:** When a next phase is identified, use the Copilot CLI to directly
delegate execution of that phase — no intermediate GitHub issue needed.

| Task | Description | Status |
|---|---|---|
| 4.1 | Install Copilot CLI in the workflow (`npm install -g @github/copilot` or use `gh copilot`) | ✅ |
| 4.2 | Construct the delegation prompt: "Continue to phase N of plan `<path>`. Goal: `<goal>`. Tasks: `<task list>`" | ✅ |
| 4.3 | Invoke `gh copilot` (or `copilot -p`) with the constructed prompt to delegate the task | ✅ |
| 4.4 | Authenticate with Copilot using the `COPILOT_PAT` secret | ✅ |
| 4.5 | If all phases are complete, post a comment on the merged PR: "🎉 All phases of \<plan\> are now complete!" | ✅ |
| 4.6 | If Copilot CLI is unavailable (no `COPILOT_PAT`), degrade gracefully: post a PR comment with the next phase details and a manual prompt suggestion instead | ✅ |
| 4.7 | Log the delegation prompt and Copilot CLI response to `$GITHUB_STEP_SUMMARY` | ✅ |

### Phase 5: Safety Gates & Edge Cases ✅

**Goal:** Handle edge cases and prevent undesired behavior.

| Task | Description | Status |
|---|---|---|
| 5.1 | Skip if the plan file does not exist (post warning comment on PR) | ✅ |
| 5.2 | Skip if the plan has no recognizable phase structure | ✅ |
| 5.3 | Handle plans where phase status is tracked only in task tables (not in headers) | ✅ |
| 5.4 | Add a `skip-continuation` label that, when present on the PR, prevents the workflow from running | ✅ |
| 5.5 | Add concurrency group per plan file to prevent parallel delegation runs | ✅ |
| 5.6 | Log all decisions to `$GITHUB_STEP_SUMMARY` for auditability | ✅ |

### Phase 6: Documentation & Rollout ✅

**Goal:** Document the feature and prepare for merge to the default branch.

| Task | Description | Status |
|---|---|---|
| 6.1 | Add usage instructions to `CONTRIBUTING.md` (plan-linking convention) | ✅ |
| 6.2 | Add inline comments in the workflow YAML explaining each step | ✅ |
| 6.3 | Note that `pull_request` workflows must exist on the default branch to trigger on merge | ✅ |
| 6.4 | Update this plan with ✅ status for completed phases | ✅ |
| 6.5 | Add a section to the writing-plans skill referencing this automation | ✅ |

---

## 5. Plan File Format Assumptions

The parser must handle the plan formats used in this repository. Based on
analysis of all 15 plan files, the following patterns exist:

### Phase Header Formats

```markdown
### Phase 1: Core Workflow Scaffold ✅
### Phase N: Title (Priority: High)              ← priority in header (most plans)
### Phase 1 — Quick wins                         ← dash separator (performance)
```

### Phase Completion Indicators

| Indicator | Location | Example |
|---|---|---|
| ✅ in phase header | Header line | `### Phase 1: Title ✅` |
| All tasks ✅ in table | Task table | Every row has `✅` in Status column |
| Checkbox `[x]` | Milestone section | `- [x] Task description` |

### Task Table Formats

```markdown
| Task | Description | Status |
|---|---|---|
| 1.1 | Create the workflow file | ✅ |
| 1.2 | Add permission check | ❌ |
```

The parser will use a priority order:
1. ✅ in phase header → phase is complete
2. All task rows contain ✅ → phase is complete
3. Otherwise → phase is incomplete

---

## 6. Workflow YAML Design

### 6.1 Trigger & Permissions

```yaml
on:
  pull_request:
    types: [closed]
    branches: [master]

  workflow_dispatch:
    inputs:
      plan_file:
        description: "Path to plan file (e.g. docs/plans/udt-support.md)"
        required: true
        type: string
      phase:
        description: "Completed phase number (or 'auto' to detect from plan)"
        required: false
        default: "auto"
        type: string
```

The workflow runs on every PR close targeting master, but immediately exits
if the PR was not merged (`github.event.pull_request.merged != true`) or
has no plan reference. It can also be dispatched manually via `workflow_dispatch`
for testing — in that mode, the plan file and optional phase number are provided
as inputs, bypassing PR detection entirely (see [§6.4](#64-manual-dispatch--testing)).

**Required permissions:**

| Permission | Scope | Reason |
|---|---|---|
| `contents: read` | Repository | Read plan files from the repo |
| `pull-requests: write` | Repository | Post comments on the merged PR |

### 6.2 Step-by-Step Pseudocode

```
1.  Trigger: pull_request closed (targeting master) OR workflow_dispatch
2.  If workflow_dispatch → use inputs.plan_file and inputs.phase directly (skip steps 2-7)
3.  Guard: was the PR actually merged? (github.event.pull_request.merged)
4.  Guard: does the PR have `skip-continuation` label? → exit
5.  **Bootstrap detection:** List PR changed files via GitHub API; collect any
    docs/plans/*.md files that were added or modified
6.  Extract plan reference from PR body (regex: Plan: docs/plans/<name>.md)
7.  Fallback: extract from branch name (plan/<name>/phase-N)
8.  Merge results: combine plans from steps 5-7, deduplicate
9.  If no plan files found → exit silently (success)
10. Checkout repository at merge commit
11. For each detected plan file:
      a. Run parse-plan.py on the plan file
      b. If plan file not found → post warning comment, continue
      c. Parse JSON output: list of phases with status
      d. Determine completed phase:
           - From PR body "Phase: N" if present
           - For bootstrap PRs (plan file in changed files): none completed yet
           - For workflow_dispatch: inputs.phase (or "auto")
           - Otherwise: latest phase marked complete in the plan
      e. Find next incomplete phase (first phase that is not ✅)
      f. If no next phase → post "all phases complete" comment, continue
      g. Construct delegation prompt:
           "Continue to phase N of plan docs/plans/<name>.md.
            Phase goal: <goal>. Tasks: <task table>"
      h. Invoke Copilot CLI with the delegation prompt
12. Post comment on merged PR with delegation summary (skip if workflow_dispatch)
13. Log summary to $GITHUB_STEP_SUMMARY
```

### 6.3 Draft Workflow YAML

```yaml
name: Plan Phase Continuation

# See docs/plans/plan-phase-continuation-action.md for full design details.
on:
  pull_request:
    types: [closed]
    branches: [master]

  # Manual dispatch for testing — provide plan file path and optional phase.
  workflow_dispatch:
    inputs:
      plan_file:
        description: "Path to plan file (e.g. docs/plans/udt-support.md)"
        required: true
        type: string
      phase:
        description: "Completed phase number (or 'auto' to detect from plan)"
        required: false
        default: "auto"
        type: string

concurrency:
  group: plan-continuation-${{ github.event.pull_request.number || github.run_id }}
  cancel-in-progress: false

jobs:
  continue-plan:
    name: Continue Plan Phase
    runs-on: ubuntu-latest
    # Run if: manually dispatched, OR PR was merged
    if: >-
      github.event_name == 'workflow_dispatch' ||
      github.event.pull_request.merged == true
    permissions:
      contents: read
      pull-requests: write

    steps:
      # ── 0. Handle manual dispatch (workflow_dispatch) ─────────
      - name: Use workflow_dispatch inputs
        if: github.event_name == 'workflow_dispatch'
        id: dispatch
        run: |
          echo "plan_file=${{ inputs.plan_file }}" >> "$GITHUB_OUTPUT"
          echo "phase=${{ inputs.phase }}" >> "$GITHUB_OUTPUT"
          echo "has_plan=true" >> "$GITHUB_OUTPUT"
          echo "📋 Manual dispatch: plan=${{ inputs.plan_file }}, phase=${{ inputs.phase }}"

      # ── 1. Detect plan files from PR changed files (bootstrap) ──
      - name: Detect plan files in PR changed files
        if: github.event_name != 'workflow_dispatch'
        id: changed-plans
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          # List files changed in this PR and filter for docs/plans/*.md
          CHANGED_PLANS=$(gh api \
            "repos/${{ github.repository }}/pulls/${{ github.event.pull_request.number }}/files" \
            --paginate --jq '.[].filename' \
            | grep -E '^docs/plans/.*\.md$' || true)

          echo "files<<EOF" >> "$GITHUB_OUTPUT"
          echo "$CHANGED_PLANS" >> "$GITHUB_OUTPUT"
          echo "EOF" >> "$GITHUB_OUTPUT"
          echo "has_changed_plans=$( [ -n \"$CHANGED_PLANS\" ] && echo true || echo false )" >> "$GITHUB_OUTPUT"

          if [ -n "$CHANGED_PLANS" ]; then
            echo "📄 Plan files found in PR changed files:"
            echo "$CHANGED_PLANS"
          fi

      # ── 2. Extract plan reference from PR body/branch ─────────
      - name: Extract plan reference from PR
        if: github.event_name != 'workflow_dispatch'
        id: plan-ref
        env:
          PR_BODY: ${{ github.event.pull_request.body }}
          PR_BRANCH: ${{ github.event.pull_request.head.ref }}
        run: |
          # Try PR body first: "Plan: docs/plans/<name>.md"
          PLAN_FILE=$(echo "$PR_BODY" | grep -ioP '(?<=Plan:\s)docs/plans/[a-z0-9._-]+\.md' | head -1)

          # Fallback: branch name "plan/<name>/phase-N"
          if [ -z "$PLAN_FILE" ]; then
            PLAN_NAME=$(echo "$PR_BRANCH" | grep -oP '(?<=^plan/)[a-z0-9-]+(?=/phase-)' || true)
            if [ -n "$PLAN_NAME" ]; then
              PLAN_FILE="docs/plans/${PLAN_NAME}.md"
            fi
          fi

          # Extract phase number if present
          PHASE=$(echo "$PR_BODY" | grep -ioP '(?<=Phase:\s)\d+' | head -1)
          if [ -z "$PHASE" ]; then
            PHASE=$(echo "$PR_BRANCH" | grep -oP '(?<=phase-)\d+' || true)
          fi

          # Merge: combine PR body/branch plan with changed-files plans
          CHANGED_PLANS="${{ steps.changed-plans.outputs.files }}"
          ALL_PLANS=$(echo -e "${PLAN_FILE}\n${CHANGED_PLANS}" | grep -v '^$' | sort -u)

          echo "plan_file=${PLAN_FILE}" >> "$GITHUB_OUTPUT"
          echo "phase=${PHASE}" >> "$GITHUB_OUTPUT"
          echo "all_plans<<EOF" >> "$GITHUB_OUTPUT"
          echo "$ALL_PLANS" >> "$GITHUB_OUTPUT"
          echo "EOF" >> "$GITHUB_OUTPUT"
          HAS_PLAN=$( [ -n "$ALL_PLANS" ] && echo true || echo false )
          echo "has_plan=${HAS_PLAN}" >> "$GITHUB_OUTPUT"

      # ── 3. Exit if no plan reference ─────────────────────────
      - name: Skip if no plan reference
        if: >-
          steps.dispatch.outputs.has_plan != 'true' &&
          steps.plan-ref.outputs.has_plan != 'true'
        run: echo "No plan reference found in PR — skipping."

      # ── 3. Checkout repo ─────────────────────────────────────
      - uses: actions/checkout@v4
        if: >-
          steps.dispatch.outputs.has_plan == 'true' ||
          steps.plan-ref.outputs.has_plan == 'true'

      # ── 4. Set up Python ─────────────────────────────────────
      - uses: actions/setup-python@v5
        if: >-
          steps.dispatch.outputs.has_plan == 'true' ||
          steps.plan-ref.outputs.has_plan == 'true'
        with:
          python-version: "3.12"

      # ── 5. Parse plan file ───────────────────────────────────
      - name: Parse plan and find next phase
        if: >-
          steps.dispatch.outputs.has_plan == 'true' ||
          steps.plan-ref.outputs.has_plan == 'true'
        id: parse
        run: |
          PLAN_FILE="${{ steps.dispatch.outputs.plan_file || steps.plan-ref.outputs.plan_file }}"
          COMPLETED_PHASE="${{ steps.dispatch.outputs.phase || steps.plan-ref.outputs.phase }}"

          if [ ! -f "$PLAN_FILE" ]; then
            echo "plan_exists=false" >> "$GITHUB_OUTPUT"
            exit 0
          fi

          echo "plan_exists=true" >> "$GITHUB_OUTPUT"

          # Run the plan parser
          RESULT=$(python .github/scripts/parse-plan.py \
            --plan-file "$PLAN_FILE" \
            --completed-phase "${COMPLETED_PHASE:-auto}")

          echo "next_phase_number=$(echo "$RESULT" | jq -r '.next_phase.number // empty')" >> "$GITHUB_OUTPUT"
          echo "next_phase_title=$(echo "$RESULT" | jq -r '.next_phase.title // empty')" >> "$GITHUB_OUTPUT"
          echo "all_complete=$(echo "$RESULT" | jq -r '.all_complete')" >> "$GITHUB_OUTPUT"

          # Store full phase content for the delegation prompt
          echo "$RESULT" | jq -r '.next_phase.content // empty' > /tmp/next-phase-content.md

      # ── 6. Handle missing plan file ──────────────────────────
      - name: Warn if plan file not found
        if: >-
          (steps.dispatch.outputs.has_plan == 'true' || steps.plan-ref.outputs.has_plan == 'true') &&
          steps.parse.outputs.plan_exists == 'false'
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          PLAN_FILE="${{ steps.dispatch.outputs.plan_file || steps.plan-ref.outputs.plan_file }}"
          echo "⚠️ Plan file not found: ${PLAN_FILE}"
          echo "### ⚠️ Plan File Not Found" >> "$GITHUB_STEP_SUMMARY"
          echo "\`${PLAN_FILE}\` does not exist in the repository." >> "$GITHUB_STEP_SUMMARY"
          # Post PR comment only when triggered by a PR (not manual dispatch)
          if [ "${{ github.event_name }}" = "pull_request" ]; then
            gh pr comment "${{ github.event.pull_request.number }}" \
              --repo "${{ github.repository }}" \
              --body "⚠️ **Plan file not found:** \`${PLAN_FILE}\` referenced in this PR does not exist."
          fi

      # ── 7. All phases complete ───────────────────────────────
      - name: Celebrate completion
        if: >-
          steps.parse.outputs.plan_exists == 'true' &&
          steps.parse.outputs.all_complete == 'true'
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          PLAN_FILE="${{ steps.dispatch.outputs.plan_file || steps.plan-ref.outputs.plan_file }}"
          echo "🎉 All phases of ${PLAN_FILE} are complete!"
          echo "### 🎉 All Phases Complete" >> "$GITHUB_STEP_SUMMARY"
          echo "Every phase in \`${PLAN_FILE}\` is now marked as done." >> "$GITHUB_STEP_SUMMARY"
          # Post PR comment only when triggered by a PR (not manual dispatch)
          if [ "${{ github.event_name }}" = "pull_request" ]; then
            gh pr comment "${{ github.event.pull_request.number }}" \
              --repo "${{ github.repository }}" \
              --body "🎉 **All phases complete!** Every phase in [\`${PLAN_FILE}\`](${PLAN_FILE}) is now marked as done. Great work!"
          fi

      # ── 8. Delegate next phase via Copilot CLI ───────────────
      - name: Delegate next phase to Copilot
        if: >-
          steps.parse.outputs.plan_exists == 'true' &&
          steps.parse.outputs.all_complete != 'true' &&
          steps.parse.outputs.next_phase_number != ''
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          COPILOT_GITHUB_TOKEN: ${{ secrets.COPILOT_PAT }}
        run: |
          PLAN_FILE="${{ steps.dispatch.outputs.plan_file || steps.plan-ref.outputs.plan_file }}"
          PHASE="${{ steps.parse.outputs.next_phase_number }}"
          TITLE="${{ steps.parse.outputs.next_phase_title }}"
          PLAN_NAME=$(basename "$PLAN_FILE" .md)
          PR_NUMBER="${{ github.event.pull_request.number }}"
          PHASE_CONTENT=$(cat /tmp/next-phase-content.md)

          # Install Copilot CLI
          npm install -g @github/copilot 2>/dev/null || true

          # Construct the delegation prompt
          PROMPT="Continue to phase ${PHASE} of plan ${PLAN_FILE}.
          Phase title: ${TITLE}.

          ## Tasks

          ${PHASE_CONTENT}

          ---
          Read the full plan at ${PLAN_FILE} for context.
          Implement all tasks listed above for Phase ${PHASE}."

          # Delegate via Copilot CLI — check exit code explicitly
          EXIT_CODE=0
          RESPONSE=$(copilot -p "$PROMPT" 2>&1) || EXIT_CODE=$?

          # Fallback: if Copilot CLI failed or is unavailable, post a comment
          # with the prompt so a developer can pick it up manually.
          if [ "$EXIT_CODE" -ne 0 ] || [ -z "$RESPONSE" ]; then
            echo "⚠️ Copilot CLI not available (exit code: ${EXIT_CODE})"
            # Post PR comment only when triggered by a PR (not manual dispatch)
            if [ "${{ github.event_name }}" = "pull_request" ] && [ -n "${PR_NUMBER}" ]; then
              gh pr comment "${PR_NUMBER}" \
                --repo "${{ github.repository }}" \
                --body "🔄 **Next phase ready:** Phase ${PHASE}: ${TITLE} of [\`${PLAN_FILE}\`](${PLAN_FILE}).

          Copilot CLI was not available (exit code: ${EXIT_CODE}). Run manually:
          \`\`\`
          copilot -p \"Continue to phase ${PHASE} of plan ${PLAN_FILE}\"
          \`\`\`"
            fi
          else
            if [ "${{ github.event_name }}" = "pull_request" ] && [ -n "${PR_NUMBER}" ]; then
              gh pr comment "${PR_NUMBER}" \
                --repo "${{ github.repository }}" \
                --body "🔄 **Next phase delegated!** Phase ${PHASE}: ${TITLE} of [\`${PLAN_FILE}\`](${PLAN_FILE}) has been sent to Copilot CLI."
            fi
          fi

          # Step summary (truncate response to avoid verbose/sensitive output)
          RESPONSE_SUMMARY=$(echo "${RESPONSE:-'(not available)'}" | head -20)
          {
            echo "### Plan Phase Continuation"
            echo ""
            echo "- **Plan:** \`${PLAN_FILE}\`"
            echo "- **Next phase:** ${PHASE} — ${TITLE}"
            echo "- **Copilot CLI exit code:** ${EXIT_CODE}"
            echo "- **Status:** $( [ "$EXIT_CODE" -eq 0 ] && echo '✅ Delegated' || echo '⚠️ Fallback (manual prompt posted)')"
          } >> "$GITHUB_STEP_SUMMARY"
```

---

### 6.4 Manual Dispatch & Testing

The workflow includes a `workflow_dispatch` trigger so it can be run manually
for testing without needing to merge a PR. This is useful for:

- Verifying the parser works on a specific plan file
- Testing the Copilot CLI delegation end-to-end
- Re-running delegation for a plan that stalled
- Debugging workflow behavior in a branch before merging

#### Triggering via `gh` CLI

```bash
# Basic: run against a plan file (auto-detect next phase)
gh workflow run plan-continuation.yml \
  -f plan_file="docs/plans/udt-support.md"

# Specify which phase was just completed (delegate phase 4 next)
gh workflow run plan-continuation.yml \
  -f plan_file="docs/plans/udt-support.md" \
  -f phase="3"

# Run on a specific branch (useful for testing before merge)
gh workflow run plan-continuation.yml \
  --ref my-feature-branch \
  -f plan_file="docs/plans/performance-improvement.md"

# Dry-run: check which phase would be next without delegation
# (use phase=auto which is the default)
gh workflow run plan-continuation.yml \
  -f plan_file="docs/plans/documentation-plan.md" \
  -f phase="auto"
```

#### Triggering via GitHub UI

1. Go to **Actions** → **Plan Phase Continuation**
2. Click **Run workflow**
3. Fill in:
   - **Plan file path:** e.g. `docs/plans/udt-support.md`
   - **Completed phase:** a number or `auto` (default)
4. Click **Run workflow**

#### Monitoring the run

```bash
# Watch the latest run
gh run watch

# List recent runs of this workflow
gh run list --workflow=plan-continuation.yml

# View logs for a specific run
gh run view <run-id> --log
```

---

## 7. Security Considerations

| Risk | Mitigation |
|---|---|
| Arbitrary file read via plan reference | Plan path is validated against `docs/plans/*.md` pattern; no path traversal possible |
| Copilot CLI prompt injection via plan content | Plan files are committed to the repo and reviewed via PRs; prompt content is repo-controlled, not user-supplied |
| Unauthorized plan continuation | Only merged PRs trigger the workflow; merge permissions are governed by branch protection rules |
| `COPILOT_PAT` secret exposure | The PAT is only exposed via `COPILOT_GITHUB_TOKEN` env var in the delegation step; it is never logged or passed to other steps. If the secret is missing, the workflow degrades gracefully (posts manual prompt instead). This token only needs the **Copilot Requests (Read)** account permission — no repo write access. |
| `GITHUB_TOKEN` scope | Token is limited to `contents: read`, `pull-requests: write` — minimum required permissions |
| Concurrent delegation for same plan | Concurrency group per PR prevents parallel runs |

> **Note:** The `pull_request: closed` trigger runs the workflow from the
> **PR's head branch** for the workflow file, but the `actions/checkout` step
> checks out the **default branch** (post-merge). The workflow YAML must be
> merged to master before it will trigger on subsequent PR merges.

---

## 8. Test Plan

### 8.1 Plan Parser Unit Tests (Phase 1)

| Test Case | Input | Expected Output |
|---|---|---|
| Parse phase with ✅ in header | `### Phase 1: Title ✅` | Phase 1 marked complete |
| Parse phase with priority tag | `### Phase 2: Title (Priority: High)` | Phase 2 marked incomplete |
| Parse phase with all ✅ tasks | Task table where every row has ✅ | Phase marked complete |
| Parse phase with mixed tasks | Task table with ✅ and ❌ | Phase marked incomplete |
| Parse phase with dash separator | `### Phase 1 — Quick wins` | Phase 1 parsed correctly |
| Multiple phases, find next | Phases 1-2 ✅, Phase 3 ❌ | Next phase = 3 |
| All phases complete | All phases have ✅ | `all_complete = true` |
| No phases found | Plan with no `### Phase` headers | Empty phase list |
| Real plan: `udt-support.md` | Actual file | Correctly identifies incomplete phases |

### 8.2 Workflow Integration Tests (Phase 3)

Because this is a workflow, integration testing is primarily manual:

| Test Case | Setup | Expected Result | Phase |
|---|---|---|---|
| **Bootstrap:** PR introduces a new plan file | PR adds `docs/plans/new-feature.md` with 3 phases | Copilot CLI delegates Phase 1 | 3, 4 |
| **Bootstrap:** PR introduces plan, all phases already ✅ | PR adds fully-completed plan file | "All phases complete" comment | 3, 4 |
| PR with plan reference, next phase exists | PR body contains `Plan: docs/plans/udt-support.md` | Copilot CLI invoked with next phase prompt | 3, 4 |
| PR with plan reference, all phases done | PR body contains `Plan:` pointing to a fully-completed plan | "All phases complete" comment | 3, 4 |
| PR with no plan reference and no plan files changed | Normal PR body, no `docs/plans/` files touched | Workflow exits silently | 3 |
| PR with invalid plan path | `Plan: docs/plans/nonexistent.md` | Warning comment posted | 5 |
| PR closed without merge | PR closed via "Close" button | Workflow does not run | 3 |
| Copilot CLI unavailable | No `COPILOT_PAT` secret | Fallback: PR comment with manual prompt | 4 |
| Branch name convention | Branch `plan/udt-support/phase-3` | Plan detected from branch name | 3 |
| `skip-continuation` label | PR has the label | Workflow does not delegate | 5 |
| **Manual dispatch:** `gh workflow run` with plan file | `gh workflow run -f plan_file=docs/plans/udt-support.md` | Workflow runs, parses plan, delegates next phase | 3, 4 |
| **Manual dispatch:** with explicit phase | `gh workflow run -f plan_file=... -f phase=2` | Next phase after 2 is delegated | 3, 4 |
| **Manual dispatch:** nonexistent plan file | `gh workflow run -f plan_file=docs/plans/nope.md` | Step summary shows warning | 5 |

### 8.3 Static Analysis

| Check | Tool | Phase |
|---|---|---|
| Workflow YAML validity | `actionlint` | 3 |
| Python script lint | `ruff` | 1 |
| Python script type check | `ty` / `mypy` | 1 |

---

## 9. References

- [GitHub Actions: `pull_request` event](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#pull_request)
- [GitHub Copilot CLI](https://docs.github.com/en/copilot/github-copilot-in-the-cli)
- [GitHub Copilot coding agent](https://docs.github.com/en/copilot/using-github-copilot/using-copilot-coding-agent)
- [Plan writing conventions](../../.github/skills/writing-plans/SKILL.md)
- [Conventional Commits specification](https://www.conventionalcommits.org/)
