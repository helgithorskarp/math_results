"""Exhaustive small proof controls and deliberate production corruptions."""
import argparse
import itertools
import json
from pathlib import Path
import tempfile

from audit import audit, cover_controls, direct_edges, read_cnf
from check_rup_lrat import verify
from sign_audit import audit as sign_audit, direct_clause_sets


def require(condition, message):
    if not condition:
        raise ValueError(message)


def hints(clauses, assumptions):
    values = dict(assumptions)
    result = []
    while True:
        changed = False
        for cid, c in enumerate(clauses, 1):
            if any(abs(v) in values and values[abs(v)] == (v > 0) for v in c):
                continue
            free = {v for v in c if abs(v) not in values}
            if not free:
                return result+[cid]
            if len(free) == 1:
                v = free.pop()
                values[abs(v)] = v > 0
                result.append(cid)
                changed = True
        if not changed:
            return None


def must_reject(call, name):
    try:
        call()
    except (ValueError, KeyError, IndexError, TypeError):
        return name
    raise ValueError("invalid input accepted: "+name)


def small_proof_controls(work):
    possible = [(1,), (-1,), (2,), (-2,), (1, 2),
                (1, -2), (-1, 2), (-1, -2)]
    sat = unsat = 0
    for mask in range(256):
        clauses = [possible[j] for j in range(8) if mask >> j & 1]
        exists = any(all(any(bits[abs(v)-1] == (v > 0) for v in c) for c in clauses)
                     for bits in itertools.product((False, True), repeat=2))
        cnf, proof = work/"small.cnf", work/"small.lrat"
        cnf.write_text(f"p cnf 2 {len(clauses)}\n"+
                       "".join(" ".join(map(str, c))+" 0\n" for c in clauses))
        if exists:
            proof.write_text(f"{len(clauses)+1} 0 "+" ".join(map(str, range(1, len(clauses)+1)))+" 0\n")
            must_reject(lambda: verify(cnf, proof), "forged SAT refutation")
            sat += 1
        else:
            rows = []
            conflict = hints(clauses, {})
            if conflict is None:
                # In an unsatisfiable two-variable CNF, assigning x leaves
                # an unsatisfiable one-variable formula, which UP closes.
                conflict = hints(clauses, {1: False})
                require(conflict is not None, "incomplete two-variable branch")
                rows.append(f"{len(clauses)+1} 1 0 "+" ".join(map(str, conflict))+" 0")
                clauses.append((1,))
                conflict = hints(clauses, {})
                require(conflict is not None, "second branch did not close")
            rows.append(f"{len(clauses)+1} 0 "+" ".join(map(str, conflict))+" 0")
            proof.write_text("\n".join(rows)+"\n")
            require(verify(cnf, proof)["mathematical_exclusion"], "valid small proof rejected")
            unsat += 1
    return {"exhaustive_two_variable_formulas": sat+unsat,
            "SAT_forged_proofs_rejected": sat, "UNSAT_proofs_checked": unsat}


def production_controls(cnf, proof, work):
    variables, _ = read_cnf(cnf)
    rows = proof.read_text().splitlines()
    first = next(i for i, row in enumerate(rows) if row.split()[1] != "d")
    parts = rows[first].split()
    separator = parts.index("0", 1)
    require(separator+1 < len(parts)-1, "first addition has no hints")
    mutations = []
    def bad_first(name, change):
        altered = parts.copy()
        change(altered)
        mutations.append((name, rows[:first]+[" ".join(altered)]+rows[first+1:]))
    bad_first("unknown propagation hint", lambda p: p.__setitem__(separator+1, "999999999"))
    bad_first("unsupported RAT hint", lambda p: p.__setitem__(separator+1, "-1"))
    bad_first("literal outside domain", lambda p: p.__setitem__(1, str(variables+1)))
    bad_first("missing terminator", lambda p: p.pop())
    mutations.append(("absent empty conclusion",
                      [r for r in rows if not (r.split()[1] == "0")]))
    mutations.append(("unknown deletion", ["1 d 999999999 0"]+rows))
    rejected = []
    target = work/"corrupt.lrat"
    for name, corrupted in mutations:
        target.write_text("\n".join(corrupted)+"\n")
        rejected.append(must_reject(lambda: verify(cnf, target), name))
    edges, _, _ = direct_edges()
    original = cnf.read_text().splitlines()
    bad = work/"corrupt.cnf"
    variants = []
    truncated = original.copy()
    truncated[0] = f"p cnf {variables} {len(original)-2}"
    variants.append(("omitted boundary unit", truncated[:-1]))
    changed = original.copy()
    changed[-1] = "-77 0"
    variants.append(("reversed boundary unit", changed))
    changed = original.copy()
    changed[1] = "1 0"
    variants.append(("replaced field progression clause", changed))
    omitted_window = original.copy()
    omitted_window[0] = f"p cnf {variables} {len(original)-2}"
    del omitted_window[52977]
    variants.append(("omitted cyclic-window clause", omitted_window))
    for name, corrupted in variants:
        bad.write_text("\n".join(corrupted)+"\n")
        rejected.append(must_reject(lambda: audit(bad, 7, edges), name))
    return {"production_corruptions_rejected": len(rejected), "cases": rejected}


def signed_controls(cnf, work):
    expected = direct_clause_sets()
    rows = cnf.read_text().splitlines()
    target = work/"corrupt-sign.cnf"
    rejected = []
    variants = []
    changed = rows.copy()
    values = list(map(int, changed[1].split()))
    values[0] = -values[0]
    changed[1] = " ".join(map(str, values))
    variants.append(("reversed signed AP literal", changed))
    changed = rows.copy()
    changed[0] = f"p cnf 44 {len(rows)-2}"
    del changed[1]
    variants.append(("omitted signed AP clause", changed))
    changed = rows.copy()
    changed[-1] = "1 0"
    variants.append(("reversed signed normalization unit", changed))
    for name, corrupted in variants:
        target.write_text("\n".join(corrupted)+"\n")
        rejected.append(must_reject(lambda: sign_audit(target, "anti", expected), name))
    rejected.append(must_reject(lambda: sign_audit(cnf, "one-opposed-pair", expected),
                                "mismatched sign profile"))
    return {"signed_encoding_corruptions_rejected": len(rejected), "cases": rejected}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cnf", type=Path)
    ap.add_argument("proof", type=Path)
    ap.add_argument("--work", type=Path, required=True)
    ap.add_argument("--signed-cnf", type=Path, required=True)
    args = ap.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="controls-", dir=args.work) as temporary:
        work = Path(temporary)
        result = {"cover": cover_controls(), "proofs": small_proof_controls(work),
                  "production": production_controls(args.cnf, args.proof, work),
                  "signed": signed_controls(args.signed_cnf, work)}
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
