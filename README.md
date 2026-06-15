# Awesome Harness Engineering (ahe-codex)

Codex chat workflow skill installer for Awesome Harness Engineering.

This project provides a set of Codex skills and templates to automatically build project harnesses. It is designed to be used directly within a Codex chat conversation, guiding users through the engineering workflow.

## Installation

### For End Users
To install the Codex skills in your current workspace, run:

```bash
npx --yes --package=ahe-codex ahe install
```

Alternatively, you can install it globally:

```bash
npm install -g ahe-codex
ahe install
```

### For Local Development
If you have cloned the repository and want to install it locally:

```bash
npx --yes --package=file:. ahe install
```

## Usage

Once installed, the `ahe` skills will be added to your `.codex` directory.

1. **Open Codex chat** in your workspace.
2. Use the `ahe init` skill to start a new harness.
3. Use exact `ahe` skills (like `ahe-conversation`, `ahe-thinking`, `ahe-spec`, `ahe-update`) to continue your existing harness work.

### Available CLI Commands

The command-line interface is primarily used for the installation and maintenance of the Codex skills:

- `ahe install [--force] [--backup]`: Installs or updates the skills in your `.codex/` directory.
- `ahe doctor`: Checks the health and integrity of your AHE skill installation.
- `ahe version`: Prints the current version.

## Project Structure

- `bin/ahe`: The main CLI executable for installing the skills.
- `.codex/skills/`: Contains the managed Codex skills (`ahe-init`, `ahe-conversation`, `ahe-thinking`, `ahe-spec`, `ahe-update`).
- `.codex/ahe-shared/`: Contains shared assets like `templates` and `schemas`.
- `AGENTS.md`: Defines the project objectives, global rules, and startup workflow.

## Agent Working Rules

If you are an AI agent working on this repository, please strictly follow the guidelines in [AGENTS.md](AGENTS.md). It includes critical instructions regarding the definition of done, verification commands, and file modification rules (e.g., you must update `PROGRESS.md` and `feature-list.json` appropriately).

## License

MIT
