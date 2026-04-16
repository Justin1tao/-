# GitHub 发布检查清单

## 1. 仓库基础
- [ ] 仓库名与简介已设置
- [ ] `README.md` 可直接说明用途与安装
- [ ] `LICENSE` 已确认
- [ ] `CHANGELOG.md` 与 release notes 已更新

## 2. 质量验证
- [ ] 执行 `pytest -q` 全部通过
- [ ] 执行 `python -m engine verify` 返回 `rules_ok=true`
- [ ] 在 macOS 本地运行 `bash scripts/install.sh` 成功
- [ ] 在 Windows 机器运行 `install.ps1` 成功

## 3. 发布材料
- [ ] 准备 3 张截图：安装成功、自检输出、一次轨迹卡示例
- [ ] 准备 30-60 秒演示视频（按 `docs/demo-video-script.md`）
- [ ] GitHub Release 描述粘贴 `docs/releases/v0.1.0.md`

## 4. 发布动作
- [ ] 打标签：`v0.1.0`
- [ ] 创建 GitHub Release
- [ ] 在 release 里附上安装命令和故障排查链接
