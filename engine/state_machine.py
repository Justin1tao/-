from __future__ import annotations

from copy import deepcopy

from engine.models import EngineResult, SessionState, UserAction
from engine.rules import RuleSet
from engine.safety import SafetyGuard
from engine.scoring import apply_reality_cost, apply_score_delta, init_scores


class LifeEngine:
    def __init__(self, ruleset: RuleSet) -> None:
        self.ruleset = ruleset
        self.guard = SafetyGuard()

    def start_session(self, profile: dict[str, object], mode: str = 'explore') -> SessionState:
        return SessionState(
            mode=mode,
            current_node_id=self.ruleset.start_node,
            scores=init_scores(profile),
            history_stack=[],
            risk_flags=[],
            profile=profile,
        )

    def apply_action(self, state: SessionState, action: UserAction) -> EngineResult:
        if action.kind == 'check_text':
            alert = self.guard.check_text(action.text)
            if alert.is_crisis:
                return EngineResult(
                    state=state,
                    current_node=self.ruleset.nodes[state.current_node_id],
                    crisis_message=alert.message,
                )
            return EngineResult(state=state, current_node=self.ruleset.nodes[state.current_node_id])

        if action.kind == 'switch_mode':
            new_state = deepcopy(state)
            if action.mode not in {'explore', 'reality'}:
                raise ValueError('mode must be explore or reality')
            new_state.mode = action.mode
            if new_state.mode == 'reality':
                new_state.scores = apply_reality_cost(
                    new_state.scores,
                    new_state.profile,
                    steps_taken=len(new_state.history_stack) + 1,
                )
            return EngineResult(state=new_state, current_node=self.ruleset.nodes[new_state.current_node_id])

        if action.kind == 'back_to':
            if action.step is None or action.step < 1 or action.step > len(state.history_stack):
                raise ValueError('invalid step for back_to')
            new_state = deepcopy(state)
            snapshot = deepcopy(new_state.history_stack[action.step - 1])
            new_state.current_node_id = snapshot['current_node_id']
            new_state.scores = snapshot['scores']
            new_state.mode = snapshot['mode']
            new_state.history_stack = new_state.history_stack[: action.step]
            return EngineResult(state=new_state, current_node=self.ruleset.nodes[new_state.current_node_id])

        if action.kind == 'back':
            if not state.history_stack:
                return EngineResult(state=state, current_node=self.ruleset.nodes[state.current_node_id])
            return self.apply_action(state, UserAction(kind='back_to', step=len(state.history_stack) - 1))

        if action.kind != 'select':
            raise ValueError(f'unsupported action: {action.kind}')

        node = self.ruleset.nodes[state.current_node_id]
        if action.option_id not in node.options:
            raise ValueError(f'option {action.option_id} not found in node {node.node_id}')

        option = node.options[action.option_id]
        new_state = deepcopy(state)
        new_state.scores = apply_score_delta(new_state.scores, option.score_delta)
        if new_state.mode == 'reality':
            new_state.scores = apply_reality_cost(
                new_state.scores,
                new_state.profile,
                steps_taken=len(new_state.history_stack) + 1,
            )

        new_state.current_node_id = option.next
        new_state.history_stack.append(
            {
                'current_node_id': new_state.current_node_id,
                'scores': deepcopy(new_state.scores),
                'mode': new_state.mode,
                'option_id': option.option_id,
            }
        )

        stabilizer = None
        if new_state.scores['mental_health'] < self.ruleset.low_mental_health_threshold:
            stabilizer = self.guard.stabilizer_message()

        return EngineResult(
            state=new_state,
            current_node=self.ruleset.nodes[new_state.current_node_id],
            trajectory_card=(
                f"当前选择：{option.text}\n"
                f"3年后状态：{option.three_year_state}\n"
                f"代价：{option.cost}\n"
                f"补救动作：{option.repair_actions}"
            ),
            stabilizer_card=stabilizer,
        )
