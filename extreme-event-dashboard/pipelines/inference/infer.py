import argparse
import json
from typing import Dict

from ml.floods.model import FloodRiskModel
from ml.fires.model import WildfireRiskModel


def main() -> None:
    parser = argparse.ArgumentParser(description="Inference pipeline")
    parser.add_argument("--task", choices=["flood", "fire"], required=True)
    parser.add_argument("--features", required=True, help="JSON string of features")
    args = parser.parse_args()

    features: Dict[str, float] = json.loads(args.features)

    if args.task == "flood":
        model = FloodRiskModel()
    else:
        model = WildfireRiskModel()

    score = model.predict(features)
    print(json.dumps({"task": args.task, "score": score}))


if __name__ == "__main__":
    main()

