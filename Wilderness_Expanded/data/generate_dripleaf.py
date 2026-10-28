
import json
from pathlib import Path

OUTPUT = Path(
    "data/wilderness_expanded/worldgen/feature/marsh"
)

DIRECTIONS = ("north", "south", "east", "west")


def water_aware_provider(block_id, facing, is_leaf=False):
    def block_state(waterlogged):
        properties = {
            "facing": facing,
            "waterlogged": str(waterlogged).lower()
        }

        if is_leaf:
            properties["tilt"] = "none"

        return {
            "type": "minecraft:simple",
            "state": {
                "id": block_id,
                "properties": properties
            }
        }

    return {
        "type": "minecraft:rule_based",
        "rules": [
            {
                "if_true": {
                    "type": "minecraft:matching_blocks",
                    "blocks": "minecraft:water"
                },
                "then": block_state(True)
            }
        ],
        "fallback": block_state(False)
    }


def create_column(facing, tall):
    stem_height = (
        {
            "type": "minecraft:uniform",
            "min_inclusive": 1,
            "max_inclusive": 2
        }
        if tall else 1
    )

    return {
        "type": "minecraft:block_column",
        "direction": "up",
        "allowed_placement": {
            "type": "minecraft:any_of",
            "predicates": [
                {
                    "type": "minecraft:matching_block_tag",
                    "tag": "minecraft:air"
                },
                {
                    "type": "minecraft:matching_blocks",
                    "blocks": "minecraft:water"
                }
            ]
        },
        "layers": [
            {
                "height": stem_height,
                "provider": water_aware_provider(
                    "minecraft:big_dripleaf_stem",
                    facing
                )
            },
            {
                "height": 1,
                "provider": water_aware_provider(
                    "minecraft:big_dripleaf",
                    facing,
                    is_leaf=True
                )
            }
        ],
        "prioritize_tip": True
    }


def create_feature(tall):
    return {
        "type": "minecraft:simple_random_selector",
        "features": [
            {
                "feature": create_column(facing, tall),
                "placement": []
            }
            for facing in DIRECTIONS
        ]
    }


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)

    for name, tall in [
        ("big_dripleaf_tall", True),
        ("big_dripleaf_short", False)
    ]:
        path = OUTPUT / f"{name}.json"

        with path.open("w", encoding="utf-8") as file:
            json.dump(
                create_feature(tall),
                file,
                indent=2
            )

        print(f"Updated: {path}")


if __name__ == "__main__":
    main()
