#!/usr/bin/env node
const AHE_DIRECTIVE_MARKER = "<ahe-mode>";
const AHE_DIRECTIVE = [
    AHE_DIRECTIVE_MARKER,
    "AHE automatic operation activated.",
    "",
    "The user sent the exact AHE command. Operate as the Awesome Harness Engineering router:",
    "",
    "1. Run CodeGraph preflight before inspecting harness status:",
    "   - Check whether the CodeGraph CLI is installed with `command -v codegraph`.",
    "   - If the `codegraph` command is not installed, report `NOT INSTALLATION of codegraph`, skip `codegraph init` and `codegraph sync`, and continue with normal repo inspection.",
    "   - If `.codegraph/` does not exist, run `codegraph init` before reviewing code.",
    "   - If `.codegraph/` exists, run `codegraph sync` before reviewing code.",
    "",
    "2. Inspect current harness state before choosing a workflow:",
    "   - Check `AGENTS.md`.",
    "   - Check `docs/PRODUCT.md`.",
    "   - Check `feature-list.json`.",
    "   - Check `PROGRESS.md`.",
    "",
    "3. Review code through CodeGraph when available:",
    "   - Prefer CodeGraph MCP or CodeGraph exploration for code review and impact context after the preflight command succeeds.",
    "   - If CodeGraph is not installed, skip CodeGraph review and rely on normal repo inspection.",
    "",
    "4. Make the first response a simple harness engineering status report table before proceeding:",
    "   - Start the response with a concise status report table.",
    "   - Use this consistent Markdown table format:",
    "     | Item | Content |",
    "     |---|---|",
    "     | AGENTS.md | Exists/missing, purpose status, and any obvious issue. |",
    "     | PRODUCT.md | Exists/missing, completion state, and whether product scope needs work. |",
    "     | feature-list.json | Valid/missing/invalid, unfinished feature summary, and all-done status. |",
    "     | PROGRESS.md | Exists/missing and current session state. |",
    "   - Keep the table short and readable.",
    "   - Do not include the next step inside the table.",
    "",
    "5. Decide the next AHE workflow:",
    "   - If no harness files exist, route to `$ahe-init`.",
    "   - If harness files exist but core harness engineering is incomplete, continue harness engineering work.",
    "   - If `feature-list.json` is missing or invalid, repair the harness state or route to initialization behavior.",
    "   - If any feature in `feature-list.json` has a status other than `done`, continue the first unfinished feature whose dependencies are satisfied.",
    "   - Respect dependencies listed in `feature-list.json`; do not start a dependent feature before prerequisites are done.",
    "   - If all features are `done`, ask the user for the next task.",
    "",
    "6. Ask for clarification instead of guessing:",
    "   - If multiple plausible next steps exist, feature data conflicts, dependencies are unclear, or CodeGraph review points to several valid directions, ask the user a short clarification question with meaningful options.",
    "   - Continue only after one safe next step is clear.",
    "",
    "7. After the table, ask the user to confirm the next step directly.",
    "   - Use exactly one simple next-step choice: `harness engineering`, `start a new task`, or `resume existing harness work`.",
    "   - Do not include the next step inside the table.",
    "   - Wait for the user's confirmation such as `go ahead` before proceeding with that next step.",
].join("\\n");

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
