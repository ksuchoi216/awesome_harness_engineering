#!/usr/bin/env node
const AHE_DIRECTIVE_MARKER = "<ahe-mode>";
const AHE_PROGRESS_DIRECTIVE = [
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
    "   - Check `docs/PRODUCT.md` and `docs/INSTRUCTIONS.md` as the product/specification source of truth.",
    "   - Check `feature-list.json` as a derived tracker.",
    "   - Check `PROGRESS.md`.",
    "   - Use `ahe-thinking` as the internal decision layer before choosing the next action.",
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
    "     | INSTRUCTIONS.md | Exists/missing, and whether instruction boundaries need work. |",
    "     | feature-list.json | Valid/missing/invalid, unfinished feature summary, and all-done status. |",
    "     | PROGRESS.md | Exists/missing and current session state. |",
    "   - Keep the table short and readable.",
    "   - Do not include the next step inside the table.",
    "",
    "5. Decide the next AHE workflow with `ahe-thinking`:",
    "   - If no harness files exist, route to `$ahe-init`.",
    "   - If `docs/PRODUCT.md` or `docs/INSTRUCTIONS.md` is missing or empty, classify the state as `harness engineering not enough` and prioritize product/instructions specification.",
    "   - If `feature-list.json` is missing or invalid, generating an empty one from template is allowed, but do not write specific features until `docs/PRODUCT.md` and `docs/INSTRUCTIONS.md` are created and organized.",
    "   - If any feature in `feature-list.json` has a status other than `done`, classify the state as `in the middle of building features` and continue the first unfinished feature whose dependencies are satisfied.",
    "   - Respect dependencies listed in `feature-list.json`; do not start a dependent feature before prerequisites are done.",
    "   - If all features are `done` and no obvious harness gap remains, classify the state as `completed all` and ask the user for the next task.",
    "   - Judge the active `project`, `feature`, or `sub-feature` before moving forward.",
    "   - For a `project`, require `Why`, `What`, and `How` by default.",
    "   - For a `feature` or `sub-feature`, require only the minimum of `Why`, `What`, and `How` needed to proceed safely.",
    "",
    "6. Ask for clarification instead of guessing:",
    "   - If multiple plausible next steps exist, feature data conflicts, dependencies are unclear, or CodeGraph review points to several valid directions, use `ahe-thinking` to judge the missing detail.",
    "   - If clarity is missing, call `ahe-conversation` for the exact missing `Why`, `What`, or `How`.",
    "   - Continue only after one safe next step is clear.",
    "",
    "7. After the table, classify the harness into exactly one state.",
    "   - Use exactly one state: `harness engineering not enough`, `in the middle of building features`, or `completed all`.",
    "   - Do not include the next step inside the table.",
    "   - Continue automatically after classification.",
    "   - Follow this loop: `thinking -> conversation if needed -> execution -> thinking`.",
].join("\\n");

const AHE_INIT_DIRECTIVE = [
    AHE_DIRECTIVE_MARKER,
    "AHE automatic operation activated.",
    "",
    "The user sent the exact AHE init command. Treat this as a possible new start request:",
    "",
    "1. Route to `$ahe-init` first.",
    "2. If no AHE-managed harness files exist, start initialization normally.",
    "3. If any AHE-managed harness file exists, read the existing files, summarize the current project purpose and product specification state, and ask what restart scope the user wants.",
    "4. Do not back up, remove, overwrite, or refresh existing harness files before the user answers the restart-scope question.",
    "5. Interpret the restart scope from the user's free-form answer; examples like `purpose` and `product` are not a closed list.",
    "6. Product/instructions specification details belong in `docs/PRODUCT.md` and `docs/INSTRUCTIONS.md`, not `AGENTS.md`.",
    "7. Use `ahe-thinking` before clarification when the next setup step is uncertain.",
    "8. If clarification is needed, call `ahe-conversation` for the exact missing detail.",
    "9. Continue through initialization work until the new start path is clear.",
].join("\\n");

function isExactAheCommand(prompt) {
    return normalizePrompt(prompt) === "ahe";
}

function isExactAheInitCommand(prompt) {
    const normalizedPrompt = normalizePrompt(prompt);
    return (
        normalizedPrompt === "ahe init" ||
        normalizedPrompt === "ahe-init" ||
        normalizedPrompt === "$ahe-init"
    );
}

function isBroadAheIntent(prompt) {
    if (isExactAheCommand(prompt) || isExactAheInitCommand(prompt)) {
        return false;
    }
    
    const p = normalizePrompt(prompt);
    
    const hasAction = /(add|new|update|change|track|manage)/.test(p);
    const hasTarget = /(product|feature|instruction|requirement|spec|work|todo)/.test(p);
    
    if (!(hasAction && hasTarget)) {
        return false;
    }
    
    const falsePositives = [
        /what is/,
        /explain/,
        /how to/,
        /how do/,
        /fix/,
        /bug/,
        /code/,
        /file/,
        /error/,
        /issue/
    ];
    
    for (const fp of falsePositives) {
        if (fp.test(p)) return false;
    }
    
    return true;
}

function getAdaptiveDirective(prompt) {
    return [
        AHE_DIRECTIVE_MARKER,
        "AHE automatic operation activated.",
        "",
        `Original prompt: "${prompt}"`,
        "",
        "The user provided a broad natural-language AHE work intent.",
        "Operate as the Awesome Harness Engineering router with an adaptive workflow:",
        "",
        "1. Run CodeGraph preflight before inspecting harness status:",
        "   - Check whether the CodeGraph CLI is installed with `command -v codegraph`.",
        "   - If the `codegraph` command is not installed, report `NOT INSTALLATION of codegraph`, skip `codegraph init` and `codegraph sync`, and continue with normal repo inspection.",
        "   - If `.codegraph/` does not exist, run `codegraph init` before reviewing code.",
        "   - If `.codegraph/` exists, run `codegraph sync` before reviewing code.",
        "",
        "2. Inspect current harness state before choosing a workflow:",
        "   - Check `AGENTS.md`.",
        "   - Check `docs/PRODUCT.md` and `docs/INSTRUCTIONS.md` as the product/specification source of truth.",
        "   - Check `feature-list.json` as a derived tracker.",
        "   - Check `PROGRESS.md`.",
        "   - Use `ahe-thinking` as the internal decision layer before choosing the next action.",
        "",
        "3. Review code through CodeGraph when available.",
        "",
        "4. Make the first response a simple harness engineering status report table before proceeding:",
        "   - Start the response with a concise status report table.",
        "   - Use this consistent Markdown table format:",
        "     | Item | Content |",
        "     |---|---|",
        "     | AGENTS.md | Exists/missing, purpose status, and any obvious issue. |",
        "     | PRODUCT.md | Exists/missing, completion state, and whether product scope needs work. |",
        "     | INSTRUCTIONS.md | Exists/missing, and whether instruction boundaries need work. |",
        "     | feature-list.json | Valid/missing/invalid, unfinished feature summary, and all-done status. |",
        "     | PROGRESS.md | Exists/missing and current session state. |",
        "   - Keep the table short and readable.",
        "   - Do not include the next step inside the table.",
        "",
        "5. Decide the next AHE workflow with `ahe-thinking` based on the original prompt:",
        "   - Classify the user intent from the original prompt as: `product/spec changes`, `instruction changes`, `feature/todo tracking`, or `unclear AHE work`.",
        "   - Route product/spec changes to `ahe-spec`.",
        "   - Route instruction changes to `ahe-spec`, and create `docs/INSTRUCTIONS.md` from the template when needed.",
        "   - Route feature/todo tracking to `ahe-update`.",
        "   - Route unclear AHE work to `ahe-conversation`.",
        "",
        "6. Ask for clarification instead of guessing:",
        "   - If the request is vague, ask exactly one detail question before editing.",
        "   - Call `ahe-conversation` for missing `Why`, `What`, or `How`.",
        "   - Continue only after one safe next step is clear.",
        "",
        "7. After the table, classify the harness into exactly one state.",
        "   - Use exactly one state: `harness engineering not enough`, `in the middle of building features`, or `completed all`.",
        "   - Do not include the next step inside the table.",
        "   - Continue automatically after classification.",
        "   - Follow this loop: `thinking -> conversation if needed -> execution -> thinking`.",
    ].join("\\n");
}

function normalizePrompt(prompt) {
    return prompt.trim().toLowerCase();
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
                    additionalContext: AHE_PROGRESS_DIRECTIVE
                }
            };
            process.stdout.write(JSON.stringify(output) + "\n");
        } else if (isExactAheInitCommand(parsed.prompt)) {
            const output = {
                hookSpecificOutput: {
                    hookEventName: "UserPromptSubmit",
                    additionalContext: AHE_INIT_DIRECTIVE
                }
            };
            process.stdout.write(JSON.stringify(output) + "\n");
        } else if (isBroadAheIntent(parsed.prompt)) {
            const output = {
                hookSpecificOutput: {
                    hookEventName: "UserPromptSubmit",
                    additionalContext: getAdaptiveDirective(parsed.prompt)
                }
            };
            process.stdout.write(JSON.stringify(output) + "\n");
        }
    }
}

main().catch(() => {});
