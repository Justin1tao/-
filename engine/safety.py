from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class SafetyAlert:
    is_crisis: bool
    message: str


class SafetyGuard:
    def __init__(self) -> None:
        self._crisis_patterns = [
            r'活不下去',
            r'不想活',
            r'想(要)?死',
            r'伤害自己',
            r'自杀',
        ]

    def check_text(self, text: str | None) -> SafetyAlert:
        if not text:
            return SafetyAlert(False, '')

        for pattern in self._crisis_patterns:
            if re.search(pattern, text):
                return SafetyAlert(
                    True,
                    (
                        '你现在的安全最重要。请立即联系你信任的人并保持有人陪伴，'
                        '如果存在紧急风险，请立即联系当地急救电话。'
                        '请立即联系专业支持后再继续。'
                    ),
                )

        return SafetyAlert(False, '')

    def stabilizer_message(self) -> str:
        return (
            '你当前心理负荷较高：先做 10 分钟降负荷动作（呼吸、补水、离开屏幕、联系可信任的人），'
            '再继续推演会更稳。'
        )
