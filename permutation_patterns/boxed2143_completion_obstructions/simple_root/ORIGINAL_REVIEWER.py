"""Independent direct-definition check of Theo's simple-input root certificate."""

from __future__ import annotations

import functools
import hashlib
import itertools
import json
import math
from pathlib import Path
import platform
import resource
import time

from definition_checker import occurrences
from check_theo_arbitrary_inflation import minimum_interval


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


@functools.lru_cache(maxsize=None)
def scaffolds(r):
    # Factorial filtering, independent of the author's recursive grammar.
    return tuple(p for p in itertools.permutations(range(1, r + 1))
                 if not any(p[i] < p[k] < p[j]
                            for i, j, k in itertools.combinations(range(r), 3)))


def word(p, rho):
    return tuple(x for pair in zip(tuple(2 * x - 1 for x in p),
                                   tuple(2 * x for x in rho)) for x in pair) + (2 * p[-1] - 1,)


def run():
    start = time.monotonic()
    base = Path(__file__).parent
    packet = base / "received/theo_simple_root_v1"
    author = json.loads((packet / "simple-completion-probe-v1.json").read_text())
    target = tuple(author["failure"]["input"])
    require(target == (3, 1, 6, 4, 2, 7, 5), "Unexpected frozen input")
    require(minimum_interval(target) is None, "Counterexample input is nonsimple")
    digest = hashlib.sha256()
    rows = []
    trials = 0
    failure = None
    for m in range(4, 8):
        all_rho = scaffolds(m - 1)
        require(len(all_rho) == math.comb(2 * (m - 1), m - 1) // m,
                "Incomplete factorial132 family")
        tested = 0
        for p in itertools.permutations(range(1, m + 1)):
            if minimum_interval(p) is not None:
                continue
            tested += 1
            allowed = (p.index(m) - 1, p.index(m))
            candidates = tuple(rho for rho in all_rho if rho.index(m - 1) in allowed)
            chosen = None
            rejected = []
            for rho in candidates:
                literal = tuple(occurrences(word(p, rho)))
                trials += 1
                if not literal:
                    chosen = rho
                    break
                rejected.append({"rho": list(rho), "indices": list(literal[0])})
            digest.update((json.dumps([p, chosen], separators=(",", ":")) + "\n").encode())
            if chosen is None:
                require(p == target, "An earlier simple-input failure occurs")
                expected = author["failure"]["all_candidate_rejection_witnesses"]
                require(rejected == expected, "Complete rejection-list witnesses differ")
                require(len(candidates) == 56 and
                        sum(rho.index(6) == 4 for rho in candidates) == 14 and
                        sum(rho.index(6) == 5 for rho in candidates) == 42,
                        "Adjacent-root set is incomplete")
                # Validate every listed author quadruple, independent of firstness.
                for row in expected:
                    require(tuple(row["indices"]) in tuple(occurrences(word(target, tuple(row["rho"])))),
                            "An author rejection quadruple is not literal-boxed")
                rho = tuple(author["failure"]["unrestricted_root_scaffold"])
                completed = word(target, rho)
                require(rho in all_rho and rho.index(6) not in allowed and
                        not tuple(occurrences(completed)), "Nonadjacent132 completion fails")
                require(completed == tuple(author["failure"]["unrestricted_root_completion"]),
                        "Named completed word differs")
                require(tuple((x + 1) // 2 for x in completed[::2]) == target, "Recovery fails")
                require(tuple(occurrences(target)) == tuple(tuple(x) for x in author["failure"]["input_occurrences"]),
                        "Input occurrence set differs")
                failure = {"input": target, "all_rho_count": len(all_rho),
                           "allowed_candidate_count": len(candidates), "rejection_witnesses": rejected,
                           "valid_nonadjacent_rho": rho, "valid_word": completed}
                break
        rows.append({"m": m, "simple_inputs_tested": tested, "complete_length": failure is None})
        if failure is not None:
            break
    require(rows == author["rows"] and trials == author["scaffold_trials"] and
            digest.hexdigest() == author["input_success_stream_sha256"], "Author finite streams/counts differ")
    return {"author": "literature-researcher-4", "checker": "literature-researcher-2",
            "decision_message_id": 410, "full_target_solved": False,
            "checked_scope": "complete finite simple-root obstruction, shorter-length minimality, exact nonadjacent completion; conditional growth bridge separately reviewed using the primary all-simple asymptotic",
            "proof_sha256": hashlib.sha256((packet / "SIMPLE_INPUT_ROOT_OBSTRUCTION_V1.md").read_bytes()).hexdigest(),
            "manifest_sha256": hashlib.sha256((packet / "MANIFEST.json").read_bytes()).hexdigest(),
            "rows": rows, "scaffold_trials": trials, "input_success_stream_sha256": digest.hexdigest(),
            "failure": failure, "all_author_deterministic_control_fields_match": True,
            "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "python": platform.python_version(), "elapsed_seconds": time.monotonic() - start,
            "peak_rss_kib_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
