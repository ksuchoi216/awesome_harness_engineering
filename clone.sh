#!/usr/bin/env bash
set -e

# 1. 저장소 클론
echo "Cloning oh-my-openagent..."
# 만약 이미 폴더가 존재한다면 삭제하거나, 클론을 생략할 수 있습니다.
if [ ! -d "oh-my-openagent" ]; then
  git clone git@github.com:code-yeongyu/oh-my-openagent.git
fi

cd oh-my-openagent

echo "Cleaning up unnecessary packages..."

# 2. 유지할 패키지 목록 (순수하게 코드 분석용으로 타겟만 남김)
KEEP_PACKAGES=(
  "omo-codex"
  "omo-opencode"
  "git-bash-mcp"
  "ast-grep-mcp"
)

# packages 폴더 내에서 KEEP_PACKAGES에 없는 폴더/파일 삭제
for pkg in packages/*; do
  if [ -e "$pkg" ]; then
    pkg_name=$(basename "$pkg")
    keep=false
    for kp in "${KEEP_PACKAGES[@]}"; do
      if [ "$pkg_name" = "$kp" ]; then
        keep=true
        break
      fi
    done
    if [ "$keep" = false ]; then
      echo "Deleting package: $pkg_name"
      rm -rf "$pkg"
    fi
  fi
done

echo "Cleaning up script/ directory..."
# 3. script 폴더 정리 (build-codex-install.ts 제외하고 삭제)
for s in script/*; do
  if [ "$(basename "$s")" != "build-codex-install.ts" ] && [ "$(basename "$s")" != "tsconfig.json" ]; then
    echo "Deleting script: $(basename "$s")"
    rm -rf "$s"
  fi
done

# 4. 루트 디렉토리의 불필요한 폴더 및 파일 삭제
echo "Cleaning up root directory..."
for item in .*; do
  if [ "$item" != "." ] && [ "$item" != ".." ] && [ "$item" != ".git" ] && [ "$item" != ".gitignore" ]; then
    rm -rf "$item"
  fi
done

for item in *; do
  if [ "$item" != "packages" ] && [ "$item" != "script" ] && [ "$item" != "package.json" ] && [ "$item" != "tsconfig.json" ] && [ "$item" != "bun.lock" ] && [ "$item" != "bunfig.toml" ]; then
    rm -rf "$item"
  fi
done

echo "Cleanup complete! Only codex-related packages remain."