#!/usr/bin/env node
const AHE_DIRECTIVE_MARKER = "<ahe-mode>";

const STATUS_TABLE_LINES = [
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
  "   - Check `docs/PRODUCT.md` and `docs/INSTRUCTIONS.md` as the product/specification source of truth.",
  "   - Check `feature-list.json` as a derived tracker.",
  "   - Check `PROGRESS.md`.",
  "   - Use `ahe-thinker` as the internal decision layer before choosing the next action.",
  "   - Before reading large harness files wholesale, let `ahe-thinker` run the `ahe-compression` size detector and call `ahe-compression` if compression is required.",
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
  "5. Decide the next AHE workflow with `ahe-thinker`:",
  "   - If no harness files exist, route to `$ahe-init`.",
  "   - If `docs/PRODUCT.md` or `docs/INSTRUCTIONS.md` is missing or empty, classify the state as `harness engineering not enough`.",
  "   - If `feature-list.json` is missing or invalid, generating an empty one from template is allowed, but do not write specific features until `docs/PRODUCT.md` and `docs/INSTRUCTIONS.md` are created and organized.",
  "   - If any feature in `feature-list.json` has a status other than `done`, classify the state as `in the middle of building features` and continue the first unfinished feature whose dependencies are satisfied.",
  "   - If all features are `done` and no obvious harness gap remains, classify the state as `completed all` and ask the user for the next task.",
  "   - Call `ahe-reviewer` when repo or code understanding is needed.",
  "   - Call `ahe-conversator` when the next safe step is blocked on user input.",
  "   - Call `ahe-harness` when product docs, instructions, tracking, todo sync, or compression-aware harness maintenance must change.",
  "   - Call `ahe-solver` when the next job is solving or planning a feature.",
  "",
  "6. After the table, classify the harness into exactly one state.",
  "   - Use exactly one state: `harness engineering not enough`, `in the middle of building features`, or `completed all`.",
  "   - Do not include the next step inside the table.",
  "   - Continue automatically after classification.",
];

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
  "7. After setup, call `ahe-harness` to build the initial product, instructions, and tracking state.",
  "8. Use `ahe-thinker` before clarification when the next setup step is uncertain.",
  "9. If clarification is needed, call `ahe-conversator` for the exact missing detail.",
].join("\n");

function getQueryDirective(prompt) {
  return [
    AHE_DIRECTIVE_MARKER,
    "AHE automatic operation activated.",
    "",
    `Original prompt: "${prompt}"`,
    "",
    "The user sent an explicit AHE query. Route it through `ahe-thinker`:",
    "",
    ...COMMON_ROUTING_LINES,
    "",
    "5. Decide the next AHE workflow with `ahe-thinker` based on the original prompt:",
    "   - Use `ahe-reviewer` for code or harness review work.",
    "   - Use `ahe-harness` for product, instructions, progress, feature-list, todo, or compression maintenance.",
    "   - For `ahe compress feature-list`, compress completed feature items, preserve unfinished details, and reconcile `feature-list.json` against `docs/PRODUCT.md`.",
    "   - If no new feature can be derived from `docs/PRODUCT.md`, call `ahe-conversator` to ask what next feature, product direction, or goal should be tracked.",
    "   - Use `ahe-solver` for feature-solving work.",
    "   - If multiple plausible next steps remain, use `ahe-conversator` to ask the minimum question needed.",
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

function isExactAheInitCommand(prompt) {
  const normalizedPrompt = normalizePrompt(prompt);
  return (
    normalizedPrompt === "ahe init" ||
    normalizedPrompt === "ahe-init" ||
    normalizedPrompt === "$ahe-init"
  );
}

function isExplicitAheQuery(prompt) {
  const normalizedPrompt = normalizePrompt(prompt);
  if (isExactAheCommand(prompt) || isExactAheInitCommand(prompt)) {
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

    if (isExactAheInitCommand(parsed.prompt)) {
      process.stdout.write(
        JSON.stringify({
          hookSpecificOutput: {
            hookEventName: "UserPromptSubmit",
            additionalContext: AHE_INIT_DIRECTIVE,
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
