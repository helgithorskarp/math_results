#!/usr/bin/env python3
"""Finite residual carrier for X20/Y18/lambda4 anchors.

Every row avoids both fixed points, preserving the chosen Y18 condition.
Graphs are checked entrywise against actual word intersections. Individual
completed tests exclude only extensions of their literal anchor. An incomplete
search or a primary inventory alone supplies no all-subfamily upper bound.
"""
from pathlib import Path
from hashlib import sha256
from itertools import combinations
import argparse
import json
import resource
import subprocess
import sys
import time

SOURCE = Path(__file__).resolve().parent.parent / 'two_fixed_saturated_upper60'
sys.path.insert(0, str(SOURCE))
import model as M
import native_replay as N
sys.path.insert(0, str(SOURCE.parent / 'free_involution_upper68'))
import joint


def finite_graph(anchor, resources, rows):
    stats = M.check_code(anchor)
    M.require(len(anchor) == 34 and stats['replications'][16:] == (20, 18),
              'not a literal X20/Y18 anchor')
    available = tuple(row for row in M.residual(anchor, resources, rows)
                      if row['replications'][16:] == (0, 0))
    M.require(all(row['weight'] == 2 for row in available), 'finite rows must be paired')
    vertices = tuple(row['representative'] for row in available)
    sets = tuple(frozenset(row['resources']) for row in available)
    adjacency = tuple(sum(1 << j for j in range(len(available))
                          if i != j and not sets[i] & sets[j])
                      for i in range(len(available)))
    literal_vertices, literal_adj = joint.residual(anchor, M.G, 16)
    M.require(vertices == literal_vertices and adjacency == literal_adj,
              'finite resource and literal graphs differ entrywise')
    return available, adjacency


