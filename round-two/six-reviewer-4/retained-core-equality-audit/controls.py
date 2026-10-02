import argparse
from copy import deepcopy
from itertools import combinations
import json
from pathlib import Path
from independent import adjacency, bits, core_oracle, domain, encoded, merge, require, validate_words


def complete_record(record):
    core = record["core"]
    oracle = core_oracle(core)
    require(record["universe_words"] == len(oracle) == 8568, "universe coverage")
    full = record["full_core"]
    require(full["words"] == domain(oracle, ()), "full candidate coverage")
    tails = full["tails"]
    require(full["maximum"] == [12, 84] and len(tails) == 84, "full maximum")
    require(tails == sorted(tails) and len({tuple(t) for t in tails}) == 84, "tail inventory")
    for tail in tails:
        require(len(tail) == 12 and not set(core) & set(tail), "full tail")
        validate_words(core + tail)
    pairs = record["two_deleted"]
    require([r["deleted"] for r in pairs] == [list(t) for t in combinations(range(57), 2)],
            "all pair cases exactly once")
    for r in pairs:
        deleted = r["deleted"]
        require(r["candidate_words"] == domain(oracle, deleted), "pair candidate coverage")
        require(len(r["optima"]) == 4, "four forbidden cases")
        forbidden = [[], [core[deleted[0]]], [core[deleted[1]]], [core[i] for i in deleted]]
        retained = [w for i, w in enumerate(core) if i not in deleted]
        for j, (size, count, tail) in enumerate(r["optima"]):
            require(type(size) is int and type(count) is int and count > 0, "exact readout types")
            require(len(tail) == size and set(tail) <= set(r["candidate_words"]), "tail alignment")
            require(not set(tail) & set(forbidden[j]), "forbidden core retained")
            validate_words(retained + tail)
        require(r["optima"][0][:2] == [14, 84], "unrestricted pair optimum")
        require(all(r["optima"][j][0] == 13 for j in (1, 2)), "restoration strictness")
        require(r["optima"][3][0] in (12, 13), "exact55 maximum")
        known = {tuple(sorted(t + [core[i] for i in deleted])) for t in tails}
        require(len(known) == r["optima"][0][1], "positive maxima count")
    require([r["deleted"] for r in record["one_deleted"]] == list(range(57)), "single coverage")
    for r in record["one_deleted"]:
        i = r["deleted"]
        require(r["candidate_words"] == domain(oracle, (i,)), "single candidate coverage")
        require(r["optima"][0][:2] == [13, 84] and r["optima"][1][0] == 12, "single maxima")
        for j, (size, count, tail) in enumerate(r["optima"]):
            require(type(count) is int and count > 0 and len(tail) == size, "single readout")
            require(set(tail) <= set(r["candidate_words"]), "single tail coverage")
            require(j == 0 or core[i] not in tail, "single forbidden")
            validate_words([w for k, w in enumerate(core) if k != i] + tail)


def controls(record):
    small = 0
    for n in range(6):
        edges = list(combinations(range(n), 2))
        for encoding in range(1 << len(edges)):
            rows = [0] * n
            for k, (i, j) in enumerate(edges):
                if encoding >> k & 1:
                    rows[i] |= 1 << j
                    rows[j] |= 1 << i
            forbidden = tuple(range(1 << n))
            answer = merge(rows, forbidden)
            independent = [m for m in range(1 << n)
                           if all(not rows[i] & m for i in bits(m))]
            for f, (a, count, witness) in zip(forbidden, answer["optima"]):
                choices = [m for m in independent if not m & f]
                best = max(m.bit_count() for m in choices)
                maxima = [m for m in choices if m.bit_count() == best]
                require([a, count] == [best, len(maxima)] and witness in maxima, "small graph exhaustive oracle")
            small += 1
    complete_record(record)
    damages = []
    def rejected(name, function):
        try:
            function()
        except (ValueError, KeyError, IndexError):
            damages.append(name)
        else:
            raise ValueError("damage accepted: " + name)
    rejected("self loop", lambda: merge([1]))
    rejected("asymmetric graph", lambda: merge([2, 0]))
    rejected("boolean adjacency", lambda: merge([False]))
    rejected("negative forbidden mask", lambda: merge([0], (-1,)))
    rejected("out-of-domain word", lambda: validate_words([1 << 19 | 15]))
    rejected("boolean word", lambda: validate_words([True]))
    rejected("duplicate word", lambda: validate_words([31, 31]))
    rejected("intersecting words", lambda: validate_words([31, 47]))
    def damage(name, mutator):
        r = deepcopy(record)
        mutator(r)
        rejected(name, lambda: complete_record(r))
    damage("universe gap", lambda r: r.update(universe_words=8567))
    damage("candidate gap", lambda r: r["two_deleted"][0]["candidate_words"].pop())
    damage("pair gap", lambda r: r["two_deleted"].pop())
    damage("duplicated pair", lambda r: r["two_deleted"].append(r["two_deleted"][0]))
    damage("single gap", lambda r: r["one_deleted"].pop())
    damage("maximum tail gap", lambda r: r["full_core"]["tails"].pop())
    damage("duplicated maximum tail", lambda r: r["full_core"]["tails"].__setitem__(0, r["full_core"]["tails"][1]))
    damage("nonpositive count", lambda r: r["two_deleted"][0]["optima"][0].__setitem__(1, 0))
    damage("boolean count", lambda r: r["two_deleted"][0]["optima"][0].__setitem__(1, True))
    damage("unsupported restoration equality", lambda r: r["two_deleted"][0]["optima"][1].__setitem__(0, 14))
    core = record["core"]
    permutations = [list(reversed(range(18))), [(5 * i + 3) % 18 for i in range(18)],
                    [*range(1, 18), 0]]
    transport_checks = 0
    for permutation in permutations:
        require(sorted(permutation) == list(range(18)), "actual point bijection")
        def image(word):
            return sum(1 << permutation[i] for i in bits(word))
        transported = [image(w) for w in core]
        new = core_oracle(transported)
        old = core_oracle(core)
        require(dict(new) == {image(w): m for w, m in old}, "complete transported oracle")
        for tail in record["full_core"]["tails"]:
            validate_words(transported + [image(w) for w in tail])
            transport_checks += 1
        for i, j in ((0, 1), (55, 56)):
            words = domain(old, (i, j))
            actual = sorted(image(w) for w in words)
            require(actual == domain(new, (i, j)), "actual pair transport")
            f, g = (1 << actual.index(transported[k]) for k in (i, j))
            result = merge(adjacency(actual), (0, f, g, f | g))
            before = record["two_deleted"][list(combinations(range(57), 2)).index((i, j))]
            require([o[:2] for o in result["optima"]] == [o[:2] for o in before["optima"]], "transported max/count")
            transport_checks += 1
    return {"complete_record_validated": True, "small_graphs_orders0_to5": small,
            "small_forbidden_domains": sum(2 ** (n * (n - 1) // 2) * 2 ** n for n in range(6)),
            "damages_rejected": damages, "actual_transported_oracles": len(permutations),
            "positive_transports": transport_checks}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("record", type=Path)
    p.add_argument("out", type=Path)
    args = p.parse_args()
    result = controls(json.loads(args.record.read_bytes()))
    args.out.write_bytes(encoded(result))
    print(json.dumps(result, sort_keys=True))
