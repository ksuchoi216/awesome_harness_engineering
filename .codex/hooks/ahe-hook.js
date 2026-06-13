#!/usr/bin/env node
const AHE_DIRECTIVE_MARKER = "<ahe-mode>";
const AHE_DIRECTIVE = [
    AHE_DIRECTIVE_MARKER,
    "AHE automatic operation activated.",
    "",
    "The user sent the exact AHE command. Operate as the Awesome Harness Engineering router:",
    "",
    "1. Inspect current harness state before choosing a workflow:",
    "   - Check `AGENTS.md`.",
    "   - Check `docs/`, including `docs/PRODUCT.md`, `docs/constraints.md`, `docs/achitecture.md`, and `docs/todo.md` when present.",
    "   - Check `feature-list.json`.",
    "   - Check `PROGRESS.md`, `SESSION-HANDOFF.md`, `init.sh`, and `.ahe/process_status.json`.",
    "",
    "2. Review code through CodeGraph when available:",
    "   - Check whether `.codegraph/` exists.",
    "   - Prefer CodeGraph MCP or CodeGraph exploration for code review and impact context.",
    "   - If CodeGraph is missing or unavailable, say that CodeGraph is not ready, explain that the user can run `codegraph init`, and continue with normal repo inspection.",
    "",
    "3. Decide the next AHE workflow:",
    "   - If no harness files exist, route to `$ahe-init`.",
    "   - If project purpose, product scope, constraints, or architecture need specification work, route to `$ahe-spec`.",
    "   - If `feature-list.json` is missing or invalid, repair the harness state or route to initialization behavior.",
    "   - If `.ahe/process_status.json` shows an active workflow, resume that workflow before starting another.",
    "   - If any feature in `feature-list.json` has a status other than `done`, continue the first unfinished feature whose dependencies are satisfied.",
    "   - Respect dependencies listed in `feature-list.json`; do not start a dependent feature before prerequisites are done.",
    "   - If all features are `done`, ask the user for the next task.",
    "",
    "4. Ask for clarification instead of guessing:",
    "   - If multiple plausible next steps exist, feature data conflicts, dependencies are unclear, or CodeGraph review points to several valid directions, ask the user a short clarification question with meaningful options.",
    "   - Continue only after one safe next step is clear.",
].join("\n");

function isExactAheCommand(prompt) {
    return prompt.trim().toLowerCase() === "ahe";
}

async function main() {
    let raw = "";
    process.stdin.setEncoding("utf8");
    for await (const chunk of process.stdin) {
        raw += chunk;
    }

    if (!raw.trim()) return;

    let parsed;
    try {
        parsed = JSON.parse(raw);
    } catch (e) {
        return;
    }

    if (
        parsed &&
        parsed.hook_event_name === "UserPromptSubmit" &&
        typeof parsed.prompt === "string"
    ) {
        if (isExactAheCommand(parsed.prompt)) {
            const output = {
                hookSpecificOutput: {
                    hookEventName: "UserPromptSubmit",
                    additionalContext: AHE_DIRECTIVE
                }
            };
            process.stdout.write(JSON.stringify(output) + "\n");
        }
    }
}

main().catch(() => {});
