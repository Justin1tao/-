from __future__ import annotations

from engine.models import SCORE_KEYS


def _clamp(value: int) -> int:
    return max(0, min(100, int(value)))


def apply_score_delta(scores: dict[str, int], delta: dict[str, int]) -> dict[str, int]:
    updated = dict(scores)
    for key in SCORE_KEYS:
        updated[key] = _clamp(updated.get(key, 50) + int(delta.get(key, 0)))
    return updated


def apply_reality_cost(scores: dict[str, int], profile: dict[str, object], steps_taken: int) -> dict[str, int]:
    # Reality mode applies opportunity cost on time and money pressure.
    budget = int(profile.get('time_budget_months', 12) or 12)
    family_finance = str(profile.get('family_finance', 'medium'))

    pressure_step = 3 + max(0, steps_taken - max(1, budget // 6))
    if family_finance == 'low':
        pressure_step += 3
    elif family_finance == 'high':
        pressure_step -= 1

    mental_penalty = max(1, pressure_step // 2)
    delta = {
        'economic_pressure': pressure_step,
        'mental_health': -mental_penalty,
    }
    return apply_score_delta(scores, delta)


def init_scores(profile: dict[str, object]) -> dict[str, int]:
    mental = int(profile.get('mental_state', 60) or 60)
    support = str(profile.get('social_support', 'medium'))
    skill = str(profile.get('employment_skill', 'medium'))

    development = 55 if skill == 'low' else 65 if skill == 'medium' else 75
    relationship = 45 if support == 'low' else 58 if support == 'medium' else 70
    economic = 65 if str(profile.get('family_finance')) == 'low' else 45

    return {
        'development_potential': _clamp(development),
        'mental_health': _clamp(mental),
        'economic_pressure': _clamp(economic),
        'relationship_stability': _clamp(relationship),
    }
