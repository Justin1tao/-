from pathlib import Path

from engine.rules import load_ruleset
from engine.state_machine import LifeEngine, UserAction


def test_start_select_and_backtrack_recompute():
    ruleset = load_ruleset(Path('data/rules.yaml'))
    engine = LifeEngine(ruleset)
    session = engine.start_session(
        profile={
            'age': 23,
            'education_stage': 'undergraduate',
            'family_finance': 'medium',
            'city_tier': 'new_first',
            'mental_state': 62,
            'relationship_pressure': 'medium',
            'risk_preference': 'medium',
            'time_budget_months': 18,
            'major': 'computer_science',
            'debt_level': 'low',
            'parent_expectation': 'high',
            'health_status': 'normal',
            'employment_skill': 'medium',
            'social_support': 'medium',
            'entrepreneurial_interest': 'low',
        },
        mode='explore',
    )

    # step 1
    step1 = engine.apply_action(session, UserAction(kind='select', option_id='exam_keep'))
    assert step1.current_node.scene == 'graduate_exam'

    # step 2
    before_mode_scores = step1.state.scores.copy()
    step2 = engine.apply_action(step1.state, UserAction(kind='switch_mode', mode='reality'))
    assert step2.state.mode == 'reality'
    assert step2.state.scores['economic_pressure'] >= before_mode_scores['economic_pressure']

    # step 3 with another choice
    step3 = engine.apply_action(step2.state, UserAction(kind='select', option_id='transfer_research'))
    assert len(step3.state.history_stack) == 2

    # back to first decision and choose another path
    rewound = engine.apply_action(step3.state, UserAction(kind='back_to', step=1))
    assert rewound.current_node.node_id == 'n_grad_exam'
    branch = engine.apply_action(rewound.state, UserAction(kind='select', option_id='job_first'))
    assert branch.current_node.node_id != step3.current_node.node_id


def test_low_mental_health_inserts_stabilizer_card():
    ruleset = load_ruleset(Path('data/rules.yaml'))
    engine = LifeEngine(ruleset)
    session = engine.start_session(
        profile={
            'age': 25,
            'education_stage': 'graduate',
            'family_finance': 'low',
            'city_tier': 'second',
            'mental_state': 32,
            'relationship_pressure': 'high',
            'risk_preference': 'low',
            'time_budget_months': 6,
            'major': 'civil_engineering',
            'debt_level': 'medium',
            'parent_expectation': 'high',
            'health_status': 'fatigue',
            'employment_skill': 'low',
            'social_support': 'low',
            'entrepreneurial_interest': 'low',
        },
        mode='explore',
    )

    result = engine.apply_action(session, UserAction(kind='select', option_id='exam_keep'))
    assert result.stabilizer_card is not None
    assert '降负荷' in result.stabilizer_card
