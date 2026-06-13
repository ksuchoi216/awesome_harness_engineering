#!/usr/bin/env node
const AHE_PATTERN = /\bahe\b/i;
const AHE_DIRECTIVE_MARKER = "<ahe-mode>";
const AHE_DIRECTIVE = `${AHE_DIRECTIVE_MARKER}
AHE routing activated. The user is invoking the Awesome Harness Engineering framework.
Please route their intent to the correct AHE workflow or suggest using $ahe-help for a list of commands.`;

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
        if (AHE_PATTERN.test(parsed.prompt)) {
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
