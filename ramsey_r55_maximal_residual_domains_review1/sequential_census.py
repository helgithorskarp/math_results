"""Run the submitted complete census with one child process at a time.

The submitted census uses a four-worker thread pool only as a scheduling
convenience.  Review policy permits one heavy proof/checking process at once,
so this wrapper replaces that executor by the ordinary serial map while
leaving the submitted per-order computation and receipt generation intact.
"""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path


class SerialExecutor:
    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def map(self, function, items):
        return list(map(function, items))


def load_target(path: Path):
    spec = importlib.util.spec_from_file_location("submitted_census", path)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load submitted census")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("target")
    parser.add_argument("data")
    parser.add_argument("out")
    parser.add_argument("producer")
    parser.add_argument("checker")
    args = parser.parse_args()

    target = load_target(Path(args.target).resolve())
    target.concurrent.futures.ThreadPoolExecutor = SerialExecutor
    result = target.run(args.data, args.out, args.producer, args.checker)
    print(target.json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
