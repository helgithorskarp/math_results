#!/usr/bin/env python3
"""Small arithmetic cover supporting the written global separator proof."""
import argparse
from itertools import combinations_with_replacement, product
import json
from pathlib import Path


def require(test, message):
    if not test:
        raise ValueError(message)


def produce():
    # A component with independence a has order at most R(5,a+1)-1.
    upper_order = {1: 4, 2: 13, 3: 24}
    rows = set()
    for components in range(2, 5):
        for alphas in combinations_with_replacement(range(1, 4), components):
            if sum(alphas) > 4:
                continue
            for sizes in product(*(range(a, upper_order[a]+1) for a in alphas)):
                separator = 43-sum(sizes)
                if not 0 <= separator <= 17:
                    continue
                if any(size-1+separator < 18 for size in sizes):
                    continue
                rows.add((separator, tuple(sorted(zip(sizes, alphas)))))
    certificate = []
    for separator, parts in sorted(rows):
        row = {"separator": separator, "components": [list(part) for part in parts]}
        cliques = [size for size, alpha in parts if alpha == 1]
        if cliques:
            size = min(cliques)
            require(size in (2, 3, 4), "Unexpected singleton survived degree bound")
            lower = size*(18-size+1)-(size-1)*separator
            upper = {2: 13, 3: 4, 4: 0}[size]
            require(lower > upper, "Clique case not excluded")
            row.update(rule="clique_common_neighbors", clique_order=size,
                       common_neighbor_lower=lower, common_neighbor_upper=upper)
        else:
            require(separator == 17 and parts == ((13, 2), (13, 2)), "Uncovered nonclique case")
            row.update(rule="two_saturated_components", outside_vertex_exists=True,
                       red_neighbors_in_each_at_most=8, blue_neighbors_in_each_at_least=5,
                       blue_pair_in_each=True)
        certificate.append(row)
    return {"status": "SEPARATOR18_ARITHMETIC_CERTIFICATE", "vertices": 43,
            "minimum_degree_at_least": 18, "clique_number_at_most": 4,
            "independence_number_at_most": 4, "separator_orders": [0, 17],
            "component_order_bounds_by_independence": upper_order,
            "rows": certificate, "whole_separator_branch_excluded": True,
            "classifies_separators_of_order18": False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    text = json.dumps(produce(), indent=2)+"\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
