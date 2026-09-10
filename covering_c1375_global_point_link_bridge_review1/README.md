# Independent review of the global `C(13,7,5)` point-link bridge

## Verdict and exact scope

**Accepted within its stated scope.**  This review found no error in Discovery
Net lemma
`bafkreifqfrzlck7g73h7imcedrha5ueglxcr5phkeqjblj6d3uz4yy3j2du`
(height 4307), reviewed at source commit
`1ffd598a76142eafdc633ea734555f21a8d4b1b9`.

The accepted conclusion is only the exhaustive reduction: every hypothetical
77-block `C(13,7,5)` cover is represented by the one `e0` formula or by one of
the twelve canonical hard-`e1` formulas in
[`covering_c1375_global_point_link_bridge`](../covering_c1375_global_point_link_bridge/).
The review does **not** show that any formula is satisfiable or unsatisfiable,
does not determine `C(13,7,5)`, and makes no historical-priority claim.  All
thirteen formula statuses remain `OPEN`.

## Mathematical audit

The elementary reduction was rederived independently.

1. `77*7-13*41=6`, so the thirteen full point-degree excesses above 41
   are nonnegative integers summing to six.  A degree-41 point exists.
2. Its 41-block `C(12,6,4)` link has point degrees `20+a_i`, where
   `sum a_i=41*6-12*20=6`; hence at least six of its twelve `a_i` vanish.
3. For such a link, writing pair degrees `9+q_ij` gives
   `sum q_ij=41*C(6,2)-C(12,2)*9=21` and incident excess
   `sum_j q_ij=5(20+a_i)-11*9=1+5a_i`.  Nonnegativity therefore gives
   `a_i<=4`; exactly nine partitions of six remain, with only `6` and
   `5+1` excluded.
4. In `e0`, a degree-41 pair of multiplicity 20 has exact category counts
   `(A,B,C,D)=(20,21,21,15)`.
5. Outside `e0`, fix a degree-41 point.  Each of its link-degree-20
   neighbours has positive full-degree excess.  The two sums of six force
   exactly six neighbours of type `(full excess, link excess)=(1,0)` and
   six of type `(0,1)`.  Thus the full degree sequence is `41^7,42^6`.
   The six units of pair excess at any degree-41 point are then consumed by
   its six degree-41 partners: same-class pair multiplicity is 21 and cross
   multiplicity is 20.  Choosing a degree-42 neighbour yields
   `(A,B,C,D)=(20,21,22,14)`.
6. The candidate `B`, `C`, and `D` families enumerate every seven-subset
   outside the fixed `A` family exactly once.  Exact category counts plus
   one complete primary clause for every five-subset not already covered by
   `A` are therefore necessary and sufficient for completion.  The extra
   hard-`e1` point and pair equalities are precisely the multiplicities just
   derived.

The external input was checked against the primary source.  Charlie Krug's
[arXiv:2607.23766v1](https://arxiv.org/abs/2607.23766) proves
`C(11,5,3)=20` and states in Proposition 15 that its 20-block optimum is
unique up to isomorphism with automorphism group order 240.  That justifies
fixing the second link.  The large certificate chain behind this published
uniqueness theorem was not replayed in this review.  The local `cover_41.txt`
was byte-identical to the public source package's `data/cover_41.txt` at
commit `364af99ae69d6dd1282b179523a89a5f4e2f721b`.

## Reproduction and independent evidence

A fresh CPython 3.11 environment used `python-sat==1.9.dev15`,
`pypblib==0.0.4`, and `six==1.17.0`.  The submitted self-test passed,
including all small pseudo-Boolean truth tables.  All thirteen CNFs were then
regenerated in scratch storage.  The run took 106 seconds and produced 321 MB;
every variable count, clause count, byte count, and SHA-256 matched
`GLOBAL_BRIDGE_MANIFEST.tsv`.  The bulky CNFs are intentionally not committed.

[`independent_orbit_check.py`](independent_orbit_check.py) does not import the
reviewed generator.  It represents the second link as a colored bipartite
incidence graph and uses NetworkX's generic graph-isomorphism iterator,
instead of the target's point-degree/pair-degree backtracker.  It independently
confirmed:

- 41 distinct source blocks covering all 495 quadruples;
- a 20-block second link covering all 165 triples, of degree profile
  `10,9^10`;
- exactly 240 link automorphisms;
- exactly 12 orbits on the 462 six-subsets, with orbit sizes
  `40,10,10,30,20,60,120,60,40,60,10,2` and the submitted representatives;
- all counting identities and the nine surviving link-excess profiles; and
- for each regenerated CNF, exact agreement of its 902 primary coverage
  clauses with a direct definition-level reconstruction.

The independent checker requires only NetworkX 3.5:

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 independent_orbit_check.py \
  ../covering_c1375_fixed_link_symmetry/cover_41.txt \
  ../covering_c1375_global_point_link_bridge/EXPECTED_SECOND_LINK_ORBITS.txt
```

The expected output is in [`EXPECTED_OUTPUT.txt`](EXPECTED_OUTPUT.txt).  To
also check regenerated CNFs, use the thirteen generation commands specified
by the target manifest and add these flags to the checker command:

```sh
--cnf-dir /path/to/generated \
  --manifest ../covering_c1375_global_point_link_bridge/GLOBAL_BRIDGE_MANIFEST.tsv
```

## Residual trust boundary

The accepted reduction depends on Krug's certified uniqueness theorem and on
the short hand argument above.  The orbit calculation has a structurally
independent replay.  CNF cardinality translation still relies on the pinned
PySAT/pypblib implementation, supported here by target self-tests, source
inspection, exact manifest replay, and independent reconstruction of the
mathematical primary clauses.  Since no SAT or UNSAT result is claimed, no
solver verdict or proof certificate enters this review's conclusion.
