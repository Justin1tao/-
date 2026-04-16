# Troubleshooting

## 1) `python -m engine verify` 失败
- 先确认 Python 版本：`python --version`（建议 3.10+）。
- 确认当前目录含 `data/rules.yaml`。
- 若提示 `No module named yaml`，执行：`pip install -r requirements.txt`。

## 2) 安装脚本权限问题（macOS）
- 运行：`chmod +x scripts/install.sh`。
- 再执行：`bash scripts/install.sh`。

## 3) Windows 执行策略阻止脚本
- 运行：
  `powershell -ExecutionPolicy Bypass -File scripts/install.ps1`

## 4) 回退到第 N 步报错
- N 必须在历史步数内且从 1 开始计数。
- 先让会话至少完成一次选择再回退。
