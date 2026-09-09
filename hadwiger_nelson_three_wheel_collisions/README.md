# All three-wheel sums with coincident labels are four-colourable

Let `W={0,1,omega,omega-1,-1,-omega,1-omega}`, where
`omega=(1+i sqrt(3))/2`. Consider the complete physical architecture
`S(u,v)=W+uW+vW`, for arbitrary complex units `u,v`, identifying coincident
labels and including **every** unit-distance edge.

**Exact computer-assisted theorem.** If the 343 labels are not all distinct,
the physical graph is four-colourable. Outside the pair-alignment conditions
`u in mu6`, `v in mu6`, or `u/v in mu6`, every collision belongs to one of
exactly four congruence classes:

| Collision squared norms | Vertices | Unit edges | Chromatic number |
|---|---:|---:|---:|
| 1, 3, 3 | 301 | 1662 | 4 |
| 1, 4, 4 | 331 | 1797 | 3 |
| 3, 3, 4 | 331 | 1770 | 4 |
| 3, 4, 4 | 337 | 1785 | 3 |

Each class has exactly **216 ordered parameter pairs**, giving **864**
nonaligned collision pairs in total. Pair-aligned members have at most
133 vertices and are four-colourable by the accepted H19-sum containment.
Consequently any non-four-colourable member of this whole architecture must
have **exactly 343 distinct physical points**. Combining this closure with
[h4065's finite reduction](../hadwiger_nelson_three_wheel_architecture/README.md)
removes the separate collision branch and leaves at most **902,481** ordered
parameter pairs. The final refresh consumed HN-3's newly published
[h4071 symmetry reduction](../hadwiger_nelson_three_wheel_symmetry_frontier/README.md):
combined with it, the remaining frontier is at most **5,110 physical classes**,
covered by **800 representative factor pairs**. HN-3 independently identified
the same four collision types; this package supplies their complete physical
chromatic decisions and the exact 864-parameter count. The remaining
injective candidates are not decided here.
There is no five-chromatic candidate or record improvement in this result.

The [proof](PROOF.md) reduces all continuous geometry to ten norm triples;
six are already pair-aligned. The 1,448-byte [certificate](certificate.json)
contains proper physical colour words for the remaining four. Its SHA-256 is
`72ac8d453f2ee0298951ce70dfaa831f5b8a8cb28a8944397443f8f94c021e79`.

From the repository root, using CPython 3.11.2 (standard library only):

```bash
python3 -B hadwiger_nelson_three_wheel_collisions/verify.py --check-expected
python3 -O -B hadwiger_nelson_three_wheel_collisions/verify.py --check-expected
python3 -B hadwiger_nelson_three_wheel_collisions/bridge.py
```

The checker reconstructs exact coordinates, deduplicates all labels, scans
210,996 distinct physical point pairs, checks every unit edge against the
colour words, verifies all four product three-colouring patterns, and
enumerates the parameter symmetry orbits. It rejects twelve corrupted colour
words. Normal and optimized Python give identical output. Expected results,
versions, independent geometry comparisons, and timings are recorded in
[EXPECTED.json](EXPECTED.json) and [VALIDATION.json](VALIDATION.json).
`bridge.py` verifies eight exact identities against h4071's pinned certificate.
The optional independent geometry comparison is reproduced by
`python3 -B hadwiger_nelson_three_wheel_collisions/compare_geometry.py`;
it takes about nine seconds and needs no external package.

Optional witness regeneration needs `python-sat==1.9.dev15` and Glucose42:

```bash
python3 -B hadwiger_nelson_three_wheel_collisions/produce.py --out /tmp/hn-collision-new
python3 -B hadwiger_nelson_three_wheel_collisions/verify.py --certificate /tmp/hn-collision-new/certificate.json
```

Choose a fresh output directory. The producer uses rational biquadratic
multiplication and labelled differences before quotienting, and needs two
SAT calls for four-colour words. Two three-colour words are explicit formulas.
The checker imports neither this producer nor a solver/CAS and uses a direct
integer physical-distance identity. SAT is only witness discovery; no UNSAT
claim is assumed. The geometric classification, colour-lifting argument,
accepted alignment theorem, and Python execution remain the trust boundary.
This is an author-checked result, not a reviewer-1 verdict or formalization.

[HANDOFF.md](HANDOFF.md) supplies the completed collision interface to HN-3.
No new source, fixed-base deletion audit, or second architecture was opened.
