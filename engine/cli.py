from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from engine.rules import RuleValidationError, load_ruleset


def cmd_verify() -> int:
    project_root = Path(__file__).resolve().parents[1]
    rules_path = project_root / 'data' / 'rules.yaml'

    result = {
        'python': sys.version.split()[0],
        'rules_file': str(rules_path),
        'rules_ok': False,
        'node_count': 0,
    }

    try:
        ruleset = load_ruleset(rules_path)
        result['rules_ok'] = True
        result['node_count'] = len(ruleset.nodes)
    except FileNotFoundError:
        print('ERROR: rules file not found', file=sys.stderr)
        return 2
    except RuleValidationError as exc:
        print(f'ERROR: invalid rules - {exc}', file=sys.stderr)
        return 3
    except Exception as exc:  # pragma: no cover - defensive
        print(f'ERROR: verify failed - {exc}', file=sys.stderr)
        return 4

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog='life-skill')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('verify', help='Run self-check for the skill package')

    args = parser.parse_args(argv)
    if args.command == 'verify':
        return cmd_verify()

    return 1


if __name__ == '__main__':
    raise SystemExit(main())
