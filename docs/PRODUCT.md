# Project Objectives
The following commends can be used in codex chat.
you should prepare like "npm install ahe or brew install ahe" because you should install skills or hooks or agents in .codex with configs.

## ahe stage structure.
```
[x] AGENTS.md
    - [x] Project name
    - [x] Project objectives
    - [x] GLOBAL_CONSTRAINTS
    - [x] PRIMARY_VERIFICATION_COMMAND
    - [x] VERIFICATION_COMMANDS
[ ] init.sh
[ ] feature-list.json
[ ] PROGRESS.md
```


## main commands
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
[ ] PROGRESS.md
...
```


## optional commands
1. "ahe arch {dir_name}": create architecture.md file in certain directory

2. "ahe const {dir_name}": create constraints.md file in certain directory

3. "ahe agent": to keep abt 600 lines in AGENTS.md. 