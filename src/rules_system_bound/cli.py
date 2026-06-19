"""Command-line smoke path for the Living Container Framework."""

from __future__ import annotations

import argparse
import json
from typing import Any, Sequence

from . import __version__
from .config import Config
from .container import Container, ContainmentRules
from .idealization import IdealizationManager, IdealizationType
from .interaction import InteractionEmergence, System


def activation_report() -> dict[str, Any]:
    """Build a deterministic report that exercises the public API."""
    root = Container(
        id="framework",
        function="containment",
        purpose="organize bounded systems",
        boundary="porous",
        properties={"scale_range": (0, 100)},
    )
    bounded = Container(
        id="bounded-system",
        function="organized process",
        purpose="demonstrate nested containment",
        boundary="semi_permeable",
        properties={"scale": 1},
    )
    rules = ContainmentRules()
    containment_score = rules.compute_containment_score(root, bounded)
    can_contain = root.can_contain(bounded, rules)
    if can_contain:
        root.add_child(bounded)

    processor = System(
        id="processor",
        function="process",
        purpose="transform inputs",
        scale=1.0,
    )
    store = System(
        id="store",
        function="store",
        purpose="retain state",
        scale=1.5,
    )
    emergence = InteractionEmergence()
    emergence.register_system(processor)
    emergence.register_system(store)
    interactions = emergence.discover_interactions(processor, store)

    manager = IdealizationManager()
    ideal = manager.create_form(
        form_id="container-contract",
        form_type=IdealizationType.WEBERIAN,
        name="Container Contract",
        real_system=root,
    )
    relation = manager.relate(ideal, root)
    config = Config()

    return {
        "package": "rules-system-bound",
        "version": __version__,
        "status": "runnable",
        "exec_path": {
            "from_source": "PYTHONPATH=src python3 -m rules_system_bound --json",
            "after_install": "rules-system-bound --json",
        },
        "containment": {
            "container": root.id,
            "contained": bounded.id,
            "can_contain": can_contain,
            "score": containment_score,
            "lineage": [node.id for node in bounded.get_lineage()],
        },
        "interactions": [
            {
                "id": interaction.id,
                "type": interaction.interaction_type,
                "source": interaction.source.id,
                "target": interaction.target.id,
            }
            for interaction in interactions
        ],
        "idealization": {
            "form": ideal.id,
            "type": ideal.type.value,
            "real": root.id,
            "co_constitutive": relation.is_co_constitutive,
        },
        "config": {
            "domain_family": config.domain_family,
            "primitive_type": config.primitive_type,
            "level_names_emerge": config.level_names_emerge,
        },
    }


def render_text(report: dict[str, Any]) -> str:
    """Render the activation report for humans."""
    containment = report["containment"]
    idealization = report["idealization"]
    return "\n".join(
        [
            f"{report['package']} {report['version']}",
            f"status: {report['status']}",
            (
                "containment: "
                f"{containment['container']} contains {containment['contained']} = "
                f"{'yes' if containment['can_contain'] else 'no'} "
                f"(score {containment['score']:.2f})"
            ),
            f"lineage: {' > '.join(containment['lineage'])}",
            f"interactions: {len(report['interactions'])} discovered",
            (
                "idealization: "
                f"{idealization['form']} ({idealization['type']}) "
                f"co-constitutes {idealization['real']}"
            ),
            f"exec_path: {report['exec_path']['from_source']}",
        ]
    )


def build_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="rules-system-bound",
        description="Run the Living Container Framework activation smoke path.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit machine-readable activation evidence",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the activation smoke path."""
    parser = build_parser()
    args = parser.parse_args(argv)
    report = activation_report()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(render_text(report))
    return 0
