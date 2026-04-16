from engine.safety import SafetyGuard


def test_high_risk_phrase_triggers_crisis_mode():
    guard = SafetyGuard()
    alert = guard.check_text('我真的活不下去了，想伤害自己')
    assert alert.is_crisis is True
    assert '请立即联系' in alert.message


def test_non_crisis_text_passes():
    guard = SafetyGuard()
    alert = guard.check_text('我现在只是有点焦虑，但还想继续做选择')
    assert alert.is_crisis is False
