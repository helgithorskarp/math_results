#!/usr/bin/env python3
"""Build an endpoint e(X)=512 CNF for one exact t=5 residual branch."""

import argparse
import itertools
import json
from pathlib import Path

from pysat.card import CardEnc, EncType

import closure_t5_127


def edge_variables(order=43):
    pairs = list(itertools.combinations(range(order), 2))
    return pairs, {pair: index + 1 for index, pair in enumerate(pairs)}


def add_cardinality(clauses, literals, lower, upper, top_id):
    if lower > upper or lower > len(literals) or upper < 0:
        raise ValueError("inconsistent cardinality")
    lower = max(0, lower)
    upper = min(len(literals), upper)
    count = 0
    if lower:
        encoding = CardEnc.atleast(literals, bound=lower, top_id=top_id,
                                   encoding=EncType.seqcounter)
        top_id = max(top_id, encoding.nv)
        clauses.extend(encoding.clauses)
        count += len(encoding.clauses)
    if upper < len(literals):
        encoding = CardEnc.atmost(literals, bound=upper, top_id=top_id,
                                  encoding=EncType.seqcounter)
        top_id = max(top_id, encoding.nv)
        clauses.extend(encoding.clauses)
        count += len(encoding.clauses)
    return top_id, count


def build(catalog, physical_path, ct_path, residual_index, delta_index):
    physical = json.loads(Path(physical_path).read_text())
    ct = json.loads(Path(ct_path).read_text())
    ct_result = next(item for item in ct["results"]
                     if item["residual_index"] == residual_index)
    delta = tuple(ct_result["ct_witnesses"][delta_index]["delta"])
    item = physical["survivors"][residual_index]
    rows = Path(catalog).read_bytes().splitlines()
    graphs = {index: closure_t5_127.nx.from_graph6_bytes(rows[index])
              for index in (item["left_catalog_index"],
                            item["right_catalog_index"])}
    fixed, active_order = closure_t5_127.fixed_gluing(item, graphs)
    pairs, variables = edge_variables()
    clauses = [[variables[pair] if value else -variables[pair]]
               for pair, value in fixed.items()]
    top_id = 903

    red_five_clauses = 0
    blue_five_clauses = 0
    for chosen in itertools.combinations(range(43), 5):
        chosen_pairs = tuple(itertools.combinations(chosen, 2))
        if not any(fixed.get(pair) == 0 for pair in chosen_pairs):
            clause = [-variables[pair] for pair in chosen_pairs
                      if pair not in fixed]
            if not clause:
                raise ValueError("fixed red K5")
            clauses.append(clause)
            red_five_clauses += 1
        if not any(fixed.get(pair) == 1 for pair in chosen_pairs):
            clause = [variables[pair] for pair in chosen_pairs
                      if pair not in fixed]
            if not clause:
                raise ValueError("fixed blue K5")
            clauses.append(clause)
            blue_five_clauses += 1

    degree_clauses = 0
    common = tuple(range(2, 2 + len(delta)))
    exact_degree = {vertex: 24 - delta[index]
                    for index, vertex in enumerate(common)}
    for vertex in range(43):
        incident = [pair for pair in pairs if vertex in pair]
        fixed_degree = sum(fixed[pair] for pair in incident if pair in fixed)
        free = [variables[pair] for pair in incident if pair not in fixed]
        if vertex in exact_degree:
            lower = upper = exact_degree[vertex] - fixed_degree
        else:
            lower = 18 - fixed_degree
            upper = 24 - fixed_degree
        top_id, count = add_cardinality(
            clauses, free, lower, upper, top_id)
        degree_clauses += count

    free_variables = [variables[pair] for pair in pairs if pair not in fixed]
    target = 512 - sum(fixed.values())
    encoding = CardEnc.equals(free_variables, bound=target, top_id=top_id,
                              encoding=EncType.cardnetwrk)
    top_id = max(top_id, encoding.nv)
    clauses.extend(encoding.clauses)
    metadata = {
        "residual_index": residual_index,
        "delta_index": delta_index,
        "delta_C": delta,
        "profile_pair_index": item["profile_pair_index"],
        "left_catalog_index": item["left_catalog_index"],
        "left_root": item["left_root"],
        "right_catalog_index": item["right_catalog_index"],
        "right_root": item["right_root"],
        "right_common_images": item["right_common_images"],
        "active_order": active_order,
        "fixed_edges": len(fixed),
        "fixed_red_edges": sum(fixed.values()),
        "unknown_edges": len(free_variables),
        "unknown_red_edge_target": target,
        "variables": top_id,
        "clauses": len(clauses),
        "red_five_clauses": red_five_clauses,
        "blue_five_clauses": blue_five_clauses,
        "degree_clauses": degree_clauses,
        "global_cardinality_clauses": len(encoding.clauses),
    }
    return clauses, metadata


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--physical", required=True)
    parser.add_argument("--ct", required=True)
    parser.add_argument("--residual", type=int, required=True)
    parser.add_argument("--delta", type=int, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    args = parser.parse_args()
    clauses, metadata = build(args.catalog, args.physical, args.ct,
                              args.residual, args.delta)
    with args.cnf.open("w") as stream:
        stream.write("p cnf %d %d\n" % (metadata["variables"], len(clauses)))
        for clause in clauses:
            stream.write(" ".join(map(str, clause)) + " 0\n")
    args.metadata.write_text(json.dumps(metadata, sort_keys=True) + "\n")
    print(json.dumps(metadata, sort_keys=True))


if __name__ == "__main__":
    main()
