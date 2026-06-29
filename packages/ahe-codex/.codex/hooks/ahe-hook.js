#!/usr/bin/env node
const AHE_DIRECTIVE_MARKER = "<ahe-mode>";

const STATUS_TABLE_LINES = [
  "   - Start the response with a concise status report table.",
  "   - Use this consistent Markdown table format:",
  "     | Item | Content |",
  "     |---|---|",
  "     | AGENTS.md | Exists/missing, purpose status, and any obvious issue. |",
  "     | product.md | Exists/missing, completion state, and whether product scope needs work. |",
  "     | INSTRUCTIONS.md | Exists/missing, and whether instruction boundaries need work. |",
  "     | feature-list.json | Valid/missing/invalid, unfinished feature summary, and all-done status. |",
  "     | progress.md | Exists/missing and current session state. |",
  "   - Keep the table short and readable.",
  "   - Do not include the next step inside the table.",
];

const COMMON_ROUTING_LINES = [
  "1. Run CodeGraph preflight before inspecting harness status:",
  "   - Check whether the CodeGraph CLI is installed with `command -v codegraph`.",
  "   - If the `codegraph` command is not installed, report `NOT INSTALLATION of codegraph`, skip `codegraph init` and `codegraph sync`, and continue with normal repo inspection.",
  "   - If `.codegraph/` does not exist, run `codegraph init` before reviewing code.",
  "   - If `.codegraph/` exists, run `codegraph sync` before reviewing code.",
  "",
  "2. Inspect current harness state before choosing a workflow:",
  "   - Check `AGENTS.md`.",
  "   - Read all existing `docs/*.md` files as supporting project context, even when `AGENTS.md` does not name them directly.",
  "   - Check `docs/product.md` and `docs/INSTRUCTIONS.md` as the product/specification source of truth.",
  "   - Treat `docs/product.md` as overview context and optional `docs/product1.md`, `docs/product2.md`, and later numeric suffix files as ordered product stages.",
  "   - Ignore non-numeric product docs such as `docs/product-alpha.md` when choosing product stage order.",
  "   - Choose the active product source by numeric suffix order: first `docs/product1.md`, then `docs/product2.md`, and so on, using the first stage whose derived work is not complete.",
  "   - Always derive features from only the active product stage; keep future product stages as context until earlier stages are done.",
  "   - Check `feature-list.json` as a derived tracker.",
  "   - Check `progress.md`.",
  "   - Use `think` as the internal decision layer before choosing the next action.",
  "   - Before reading large harness files wholesale, let `think` run the `compress` size detector and test-overlap detector. Call `compress` if compression is required.",
  "   - For explicit `ahe compress`, run both compression detectors before choosing the next action.",
  "",
  "3. Review code through CodeGraph when available:",
  "   - Prefer CodeGraph MCP or CodeGraph exploration for code review and impact context after the preflight command succeeds.",
  "   - If CodeGraph is not installed, skip CodeGraph review and rely on normal repo inspection.",
  "",
  "4. Make the first response a simple harness engineering status report table before proceeding:",
  ...STATUS_TABLE_LINES,
];

const AHE_PROGRESS_DIRECTIVE = [
  AHE_DIRECTIVE_MARKER,
  "AHE automatic operation activated.",
  "",
  "The user sent the exact AHE command. Operate as the Awesome Harness Engineering router:",
  "",
  ...COMMON_ROUTING_LINES,
  "",
  "5. Decide the next AHE workflow with `think`:",
  "   - If no harness files exist, route to `$new`.",
  "   - If `docs/product.md` or `docs/INSTRUCTIONS.md` is missing or empty, classify the state as `harness engineering not enough`.",
  "   - If `feature-list.json` is missing or invalid, generating an empty one from template is allowed, but do not write specific features until `docs/product.md` and `docs/INSTRUCTIONS.md` are created and organized.",
  "   - When numbered product stages exist, derive feature-list items from only the active product stage.",
  "   - Advance from `docs/product1.md` to `docs/product2.md` only after all feature-list items derived from `docs/product1.md` are `done`; repeat this rule for later numeric stages.",
  "   - If any feature in `feature-list.json` has a status other than `done`, classify the state as `in the middle of building features` and continue the first unfinished feature whose dependencies are satisfied.",
  "   - If all features are `done` and no obvious harness gap remains, classify the state as `completed all` and ask the user for the next task.",
  "   - Call `review` when repo or code understanding is needed.",
  "   - Call `converse` when the next safe step is blocked on user input.",
  "   - Call `harness` when product docs, instructions, tracking, todo sync, or compression-aware harness maintenance must change.",
  "   - Call `solve` when the next job is solving or planning a feature.",
  "",
  "6. After the table, classify the harness into exactly one state.",
  "   - Use exactly one state: `harness engineering not enough`, `in the middle of building features`, or `completed all`.",
  "   - Do not include the next step inside the table.",
  "   - Continue automatically after classification.",
];

const AHE_NEW_DIRECTIVE = [
  AHE_DIRECTIVE_MARKER,
  "AHE automatic operation activated.",
  "",
  "The user sent the exact AHE new command. Treat this as a possible new start request:",
  "",
  "1. Route to `$new` first.",
  "2. If no AHE-managed harness files exist, start initialization normally.",
  "3. If any AHE-managed harness file exists, read the existing files, summarize the current project purpose and product specification state, and ask what restart scope the user wants.",
  "4. Do not remove, overwrite, or refresh existing harness files before the user answers the restart-scope question.",
  "5. If the chosen restart scope replaces prior harness history, summarize that replaced state in the refreshed tracking artifacts instead of creating backup copies.",
  "6. Interpret the restart scope from the user's free-form answer; examples like `purpose` and `product` are not a closed list.",
  "7. Product/instructions specification details belong in `docs/product.md` and `docs/INSTRUCTIONS.md`, not `AGENTS.md`.",
  "8. After setup, call `harness` to build the initial product, instructions, and tracking state.",
  "9. Use `think` before clarification when the next setup step is uncertain.",
  "10. If clarification is needed, call `converse` for the exact missing detail.",
].join("\n");

const AHE_SHIP_DIRECTIVE = [
  AHE_DIRECTIVE_MARKER,
  "AHE plan export activated.",
  "",
  "The user invoked `$ship` / `ahe ship`.",
  "",
  "Use the independent `ship` skill only:",
  "1. Detect if the current conversation is still in Plan Mode.",
  "2. If Plan Mode is active, exit Plan Mode first before continuing.",
  "3. Use the most recent `<proposed_plan>` already visible in this conversation.",
  "4. Do not ask for the plan again when the latest plan is unambiguous.",
  "5. Derive `plan_name` from the plan title and create `.plans/{plan_name}.md`.",
  "6. Add compact handoff context for Antigravity or another LLM platform.",
  "7. Use `.codex/skills/ship/scripts/write_plan.py` to write the final markdown and stop.",
  "",
  "Do not route through `think`, do not call other AHE agents, and do not run the normal AHE harness workflow.",
].join("\n");

const AHE_FIX_DIRECTIVE = [
  AHE_DIRECTIVE_MARKER,
  "AHE fix planning activated.",
  "",
  "The user invoked `$fix` / `ahe fix`.",
  "",
  "Use the dedicated `fix` skill only:",
  "1. Understand the user's error, bug, mismatch, or intended change from the current conversation and repository context.",
  "2. Create a concrete fix plan for fixing errors or following the user's intention when it differs from normal AHE continuation.",
  "3. If the fix goal, scope, or success criteria are unclear, call `converse` and ask one focused question before writing the plan.",
  "4. Derive `plan_name` from the fix goal and create `.plans/{plan_name}.md`.",
  "5. Use `.codex/skills/fix/scripts/write_fix_plan.py` to write the final markdown.",
  "",
  "Do not route through `think` and do not run the normal AHE harness workflow.",
].join("\n");

function getQueryDirective(prompt) {
  return [
    AHE_DIRECTIVE_MARKER,
    "AHE automatic operation activated.",
    "",
    `Original prompt: "${prompt}"`,
    "",
    "The user sent an explicit AHE query. Route it through `think`:",
    "",
    ...COMMON_ROUTING_LINES,
    "",
    "5. Decide the next AHE workflow with `think` based on the original prompt:",
    "   - Use `review` for code or harness review work.",
    "   - Use `harness` for product, instructions, progress, feature-list, todo, or compression maintenance.",
    "   - When product stages exist, derive features from only the active product stage and advance numeric stages only after the current stage's derived feature-list items are `done`.",
    "   - For `ahe compress`, run both compression detectors before choosing the next action.",
    "   - If the harness-size detector signals compression pressure, replace old completed feature entries with one summarized done feature, preserve unfinished details, and reconcile `feature-list.json` against `docs/product.md`.",
    "   - If the stale-test detector signals overlap, call `review` for stale-test confirmation and keeper selection, then `solve` or `harness` as needed.",
    "   - If no new feature can be derived from `docs/product.md`, call `converse` to ask what next feature, product direction, or goal should be tracked.",
    "   - Use `solve` for feature-solving work.",
    "   - If multiple plausible next steps remain, use `converse` to ask the minimum question needed.",
    "",
    "6. After the table, classify the harness into exactly one state.",
    "   - Use exactly one state: `harness engineering not enough`, `in the middle of building features`, or `completed all`.",
    "   - Do not include the next step inside the table.",
    "   - Continue automatically after classification.",
  ].join("\n");
}

function normalizePrompt(prompt) {
  return prompt.trim().toLowerCase();
}

function isExactAheCommand(prompt) {
  return normalizePrompt(prompt) === "ahe";
}

function isExactAheNewCommand(prompt) {
  const normalizedPrompt = normalizePrompt(prompt);
  return (
    normalizedPrompt === "ahe new" ||
    normalizedPrompt === "new" ||
    normalizedPrompt === "$new"
  );
}

function isExactAheShipCommand(prompt) {
  const normalizedPrompt = normalizePrompt(prompt);
  return (
    normalizedPrompt === "ahe ship" ||
    normalizedPrompt === "ship" ||
    normalizedPrompt === "$ship"
  );
}

function isExactAheFixCommand(prompt) {
  const normalizedPrompt = normalizePrompt(prompt);
  return (
    normalizedPrompt === "ahe fix" ||
    normalizedPrompt === "fix" ||
    normalizedPrompt === "$fix"
  );
}

function isExplicitAheQuery(prompt) {
  const normalizedPrompt = normalizePrompt(prompt);
  if (
    isExactAheCommand(prompt) ||
    isExactAheNewCommand(prompt) ||
    isExactAheShipCommand(prompt) ||
    isExactAheFixCommand(prompt)
  ) {
    return false;
  }
  return normalizedPrompt.startsWith("ahe ");
}

async function main() {
  let raw = "";
  process.stdin.setEncoding("utf8");
  for await (const chunk of process.stdin) {
    raw += chunk;
  }

  if (!raw.trim()) {
    return;
  }

  let parsed;
  try {
    parsed = JSON.parse(raw);
  } catch {
    return;
  }

  if (
    parsed &&
    parsed.hook_event_name === "UserPromptSubmit" &&
    typeof parsed.prompt === "string"
  ) {
    if (isExactAheCommand(parsed.prompt)) {
      process.stdout.write(
        JSON.stringify({
          hookSpecificOutput: {
            hookEventName: "UserPromptSubmit",
            additionalContext: AHE_PROGRESS_DIRECTIVE.join("\n"),
          },
        }) + "\n"
      );
      return;
    }

    if (isExactAheNewCommand(parsed.prompt)) {
      process.stdout.write(
        JSON.stringify({
          hookSpecificOutput: {
            hookEventName: "UserPromptSubmit",
            additionalContext: AHE_NEW_DIRECTIVE,
          },
        }) + "\n"
      );
      return;
    }

    if (isExactAheShipCommand(parsed.prompt)) {
      process.stdout.write(
        JSON.stringify({
          hookSpecificOutput: {
            hookEventName: "UserPromptSubmit",
            additionalContext: AHE_SHIP_DIRECTIVE,
          },
        }) + "\n"
      );
      return;
    }

    if (isExactAheFixCommand(parsed.prompt)) {
      process.stdout.write(
        JSON.stringify({
          hookSpecificOutput: {
            hookEventName: "UserPromptSubmit",
            additionalContext: AHE_FIX_DIRECTIVE,
          },
        }) + "\n"
      );
      return;
    }

    if (isExplicitAheQuery(parsed.prompt)) {
      process.stdout.write(
        JSON.stringify({
          hookSpecificOutput: {
            hookEventName: "UserPromptSubmit",
            additionalContext: getQueryDirective(parsed.prompt),
          },
        }) + "\n"
      );
    }
  }
}

main().catch(() => {});
