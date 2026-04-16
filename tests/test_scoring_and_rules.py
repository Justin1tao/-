from pathlib import Path

import pytest

from engine.rules import RuleValidationError, load_ruleset
from engine.scoring import apply_score_delta, apply_reality_cost


def test_score_boundaries_clamped():
    scores = {
        'development_potential': 95,
        'mental_health': 4,
        'economic_pressure': 98,
        'relationship_stability': 10,
    }
    updated = apply_score_delta(scores, {
        'development_potential': 20,
        'mental_health': -20,
        'economic_pressure': 10,
        'relationship_stability': -30,
    })
    assert updated['development_potential'] == 100
    assert updated['mental_health'] == 0
    assert updated['economic_pressure'] == 100
    assert updated['relationship_stability'] == 0


def test_reality_cost_increases_pressure_and_decreases_mental_health():
    scores = {
        'development_potential': 70,
        'mental_health': 70,
        'economic_pressure': 30,
        'relationship_stability': 55,
    }
    profile = {'time_budget_months': 12, 'family_finance': 'low'}
    updated = apply_reality_cost(scores, profile, steps_taken=3)
    assert updated['economic_pressure'] > scores['economic_pressure']
    assert updated['mental_health'] < scores['mental_health']


def test_rules_missing_required_fields_fails(tmp_path):
    bad_file = tmp_path / 'rules.yaml'
    bad_file.write_text(
        'version: 1\nstart_node: n1\nnodes:\n  - node_id: n1\n    scene: career\n',
        encoding='utf-8',
    )
    with pytest.raises(RuleValidationError):
        load_ruleset(bad_file)


def test_rules_cover_seven_scenes_with_at_least_two_nodes_each():
    ruleset = load_ruleset(Path('data/rules.yaml'))
    scene_count = {}
    for node in ruleset.nodes.values():
        scene_count[node.scene] = scene_count.get(node.scene, 0) + 1

    expected_scenes = {
        'education',
        'graduate_exam',
        'career',
        'city',
        'relationship',
        'family',
        'entrepreneurship',
    }
    assert expected_scenes.issubset(scene_count.keys())
    for scene in expected_scenes:
        assert scene_count[scene] >= 2
