#!/usr/bin/env python3
"""Exact arithmetic for the written global cut proof; no graph search."""
import json


def produce():
    return {"order": 43, "minimum_degree": 18, "maximum_degree": 24,
            "clique_number_at_most": 4,
            "cuts": [{"smaller_side": a, "internal_edges_at_most": 3*a*a//8,
                      "boundary_at_least": 18*a-2*(3*a*a//8)} for a in range(1, 22)],
            "both_sides_at_least_two_cut_lower": 34,
            "both_sides_at_least_three_cut_lower": 48,
            "vertex_boundary_upper": 24, "edge_boundary_upper": 46,
            "all_minimum_edge_cuts_isolate_minimum_degree_vertex": True,
            "all_minimum_restricted_edge_cuts_isolate_minimum_edge_degree_edge": True,
            "target_graph_found": False}


if __name__ == "__main__":
    print(json.dumps(produce(), indent=2))
