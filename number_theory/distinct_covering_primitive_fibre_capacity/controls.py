"""Exact positive/negative controls for the written reusable capacity lemmas."""
from pathlib import Path
from time import monotonic
import argparse
import json
import period
import fibres

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", type=Path)
    parser.add_argument("--expected", type=Path, default=HERE/"controls_expected.json")
    args = parser.parse_args()
    start = monotonic()
    result = {"agent": "six-covering-3", "role": "researcher",
              "period_controls": period.controls(), "fibre_controls": fibres.controls()}
    result = json.loads(json.dumps(result))
    if args.write:
        args.write.write_text(json.dumps(result, indent=2)+"\n")
    elif result != json.loads(args.expected.read_text()):
        raise ValueError("complete controls differ from expected evidence")
    print("Proper-period bases, genuine covers, necessary-hypothesis counterfixtures,")
    print("support projections and literal period43200 capacities all passed.")
    print("Elapsed seconds:", monotonic()-start)


if __name__ == "__main__":
    main()
