#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_ROOT="${CODEX_HOME:-$HOME/.codex}/skills"
TARGET_DIR="$TARGET_ROOT/distilled-cn-life-skill"

mkdir -p "$TARGET_ROOT"
rm -rf "$TARGET_DIR"
cp -R "$PROJECT_ROOT" "$TARGET_DIR"

PYTHON_BIN=""
if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "[ERROR] 未找到 Python，请先安装 Python 3.10+。"
  exit 2
fi

set +e
"$PYTHON_BIN" -m engine verify >/tmp/life_skill_verify.json 2>/tmp/life_skill_verify.err
VERIFY_CODE=$?
set -e

if [ "$VERIFY_CODE" -ne 0 ]; then
  echo "[ERROR] 自检失败，详情："
  cat /tmp/life_skill_verify.err
  exit "$VERIFY_CODE"
fi

echo "[OK] 安装完成: $TARGET_DIR"
echo "[OK] 版本信息: $("$PYTHON_BIN" --version)"
echo "[OK] 自检结果:"
cat /tmp/life_skill_verify.json

echo
echo "启动命令（可复制）："
echo "cd '$TARGET_DIR' && $PYTHON_BIN -m engine verify"
echo "排查文档: https://github.com/Justin1tao/被蒸馏的中国人的一生#troubleshooting"
