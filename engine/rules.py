from __future__ import annotations

from pathlib import Path

import yaml

from engine.models import NodeSpec, OptionSpec, RuleSet


class RuleValidationError(ValueError):
    pass


_REQUIRED_NODE_FIELDS = {'node_id', 'scene', 'prompt', 'options'}
_REQUIRED_OPTION_FIELDS = {
    'option_id',
    'text',
    'next',
    'score_delta',
    'three_year_state',
    'cost',
    'repair_actions',
}


def _validate_node(raw_node: dict, all_nodes: set[str]) -> NodeSpec:
    missing = _REQUIRED_NODE_FIELDS - set(raw_node.keys())
    if missing:
        raise RuleValidationError(f"node {raw_node.get('node_id', '<unknown>')} missing fields: {sorted(missing)}")

    options_map = {}
    for raw_opt in raw_node['options']:
        opt_missing = _REQUIRED_OPTION_FIELDS - set(raw_opt.keys())
        if opt_missing:
            raise RuleValidationError(
                f"option {raw_opt.get('option_id', '<unknown>')} missing fields: {sorted(opt_missing)}"
            )
        if raw_opt['next'] not in all_nodes:
            raise RuleValidationError(
                f"option {raw_opt['option_id']} points to unknown next node {raw_opt['next']}"
            )

        options_map[raw_opt['option_id']] = OptionSpec(
            option_id=raw_opt['option_id'],
            text=raw_opt['text'],
            next=raw_opt['next'],
            score_delta=dict(raw_opt.get('score_delta', {})),
            three_year_state=raw_opt['three_year_state'],
            cost=raw_opt['cost'],
            repair_actions=raw_opt['repair_actions'],
            evidence_note=raw_opt.get('evidence_note', ''),
            constraints=dict(raw_opt.get('constraints', {})),
        )

    return NodeSpec(
        node_id=raw_node['node_id'],
        scene=raw_node['scene'],
        prompt=raw_node['prompt'],
        options=options_map,
        tags=list(raw_node.get('tags', [])),
    )


def load_ruleset(path: Path) -> RuleSet:
    raw = yaml.safe_load(path.read_text(encoding='utf-8'))
    if not isinstance(raw, dict):
        raise RuleValidationError('rules file must be a mapping')

    for key in ('version', 'start_node', 'nodes'):
        if key not in raw:
            raise RuleValidationError(f'missing top-level field: {key}')

    raw_nodes = raw['nodes']
    if not isinstance(raw_nodes, list) or not raw_nodes:
        raise RuleValidationError('nodes must be a non-empty list')

    all_node_ids = {node.get('node_id') for node in raw_nodes if isinstance(node, dict)}
    if raw['start_node'] not in all_node_ids:
        raise RuleValidationError('start_node not found in nodes')

    nodes = {}
    for node in raw_nodes:
        if not isinstance(node, dict):
            raise RuleValidationError('each node must be a mapping')
        parsed = _validate_node(node, all_node_ids)
        nodes[parsed.node_id] = parsed

    return RuleSet(
        version=int(raw['version']),
        start_node=str(raw['start_node']),
        low_mental_health_threshold=int(raw.get('low_mental_health_threshold', 40)),
        nodes=nodes,
    )
