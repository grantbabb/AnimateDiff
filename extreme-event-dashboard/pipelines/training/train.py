import argparse
from typing import Dict


def train_flood_model(output_path: str) -> None:
    # Placeholder: simulate training and save artifact
    with open(output_path, "w", encoding="utf-8") as fp:
        fp.write("flood_model_parameters: {}\n")


def train_fire_model(output_path: str) -> None:
    # Placeholder: simulate training and save artifact
    with open(output_path, "w", encoding="utf-8") as fp:
        fp.write("fire_model_parameters: {}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Training pipeline")
    parser.add_argument("--task", choices=["flood", "fire"], required=True)
    parser.add_argument("--output", required=True, help="Path to save trained model artifact")
    args = parser.parse_args()

    dispatch: Dict[str, callable] = {
        "flood": train_flood_model,
        "fire": train_fire_model,
    }
    dispatch[args.task](args.output)


if __name__ == "__main__":
    main()

