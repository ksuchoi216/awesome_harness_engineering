# Project Objectives
The following commends can be used in codex chat.
you should prepare like "npm install ahe or brew install ahe" because you should install skills or hooks or agents in .codex with configs.

## ahe stage structure.
```
[x] AGENTS.md
    - [x] Project name
    - [x] Project objectives
    - [x] PRIMARY_VERIFICATION_COMMAND
    - [x] VERIFICATION_COMMANDS
[ ] init.sh
[ ] feature-list.json
[ ] progress.md

```

## To build commands
1. if user commend "ahe init", then ask for project name and project objectives one by one.
after completing user's input, then generate AGENTS.md in working directory.

2. if user commend "ahe docs", then generate empty docs/ folder and create README.md.
the README.md is like if the specifcation is too large in agents.md, then recommend user's requirement or demanded specifcation to be placed in docs/README.md.

3. if user commend "ahe check", then check current stage.
for example, the following text to be presented after execution of this command.
```
[x] AGENTS.md
    - [x] Project name
    - [x] Project objectives
[ ] init.sh
[ ] feature-list.json
[ ] progress.md
...
```