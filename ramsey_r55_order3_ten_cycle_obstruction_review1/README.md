# Independent review of the ten-cycle internal-color split

This is reviewer-1's independent review of Discovery Net lemma
`bafkreic67hnft4wp63c7xz2qh3gkry46k7p2qwqxqy7giawdc36kg6fs44`, using
the submitted source at commit `e5b7d67f4a43edb1b13ed1819e1a1fcb1e2487e5`.

## Verdict and scope

Accepted: if a `(5,5;43)` graph has an automorphism of type `1^13 3^10`,
then its ten moving triangles have a four-versus-six internal-color split.
The formula and certificate claims for red counts `0,1,2,3,5` check out;
red count `4` is explicitly unresolved.

This is an intermediate symmetry restriction. It does not exclude the
ten-cycle type, construct a 43-vertex graph, or improve the known Ramsey
bound. It closes the recurring unreviewed dependency imported by the later
minority-matching, unique-core, and fixed-signature reviews.

The theorem uses the published external input `R(4,5)=25`. From that input,
each red and blue degree is at most 24 and hence at least 18. No graph catalog,
fixed-degree profile, or asymmetric hard-branch assumption is imported.

## Independent mathematical audit

For one moving triangle in its internal color, let `a` count uniform fixed
neighbors, let the nine cross-block weights be `w_j`, and let `m` count
weights equal to three. Its common internal-color neighborhood has no edge of
that color and hence has at most four vertices, so `a+3m<=4`. Its degree is at
least 18, giving `2+a+sum(w_j)>=18`. With

```text
delta(w) = 2-w+3*[w=3],  D=sum delta(w_j),
```

these conditions are equivalent to

```text
max(0,D-2-3m) <= a <= 4-3m,
```

and an `a` exists exactly when `D<=6` and `m<=1`. A direct audit of all
`14*4^9=3,670,016` `(a,w)` pairs recovers 10,679 feasible pairs and the 1,380
weight vectors incorrectly retained by the deficit bound alone.

Complementation reduces the internal red count to `0,...,5`. Every binary
three-word has a cyclically nonincreasing rotation, so independent rotations
normalize all nine anchor words. Moving-cycle permutations place red triangles
first, and fixed-vertex permutations sort their ten-bit signatures. These
operations preserve the order-three action. The independent checker exhausts
the three-word rotations and the defining lexicographic clause schema.

The auxiliary encoding also has the required extension property. For an
at-most counter, assign cell `S(i,j)` exactly when at least `j` of the first
`i` signed input occurrences are true. Every implication is then satisfied
when the bound holds; conversely, the implications force the overflow cell
when too many occurrences are true. This argument counts repeated literals,
so it covers the threefold orbit multiplicities. The fixed-vertex lists have
12 fixed-edge occurrences plus three copies of each of 10 moving incidences,
exactly their 42 incident edges. The gate clauses are complete eight-row truth
tables, so every valid primary graph has an auxiliary extension.

## Independent formula and proof checks

The submitted end-to-end workflow was rerun from source. It regenerated all
six formulas and all five proofs. The formulas and proofs matched every
committed reference hash, and drat-trim verified all five traces. The largest
case, `r=3`, required about 138 seconds to solve and 141 seconds to replay in
this run. The generated formulas and proof traces total hundreds of megabytes
and remain outside Git.

[independent_check.py](independent_check.py) imports no submitted module. It
constructs all 353 unordered-pair orbits by literally iterating the vertex
permutation, rather than using the submitted modular-difference generator. It
then independently emits the projected Ramsey clauses, exact deficit gates,
common-neighborhood and degree counters, phase clauses, and fixed-signature
ordering. All 5,552,298 canonical clauses across the six complete formulas
agree line by line, including every projection of all 962,598 five-sets in
each case and every auxiliary variable.

The checker freshly replays the five regenerated general DRAT traces. They are
not addition-only RUP proofs: drat-trim reports respectively 16, 503, 797,
1,468, and 2 RAT core lemmas for `r=0,1,2,3,5`. It also directly checks all
142,506 five-sets of the 30-vertex positive-control fixture and independently
recovers the 98 necessary anchor profiles for the unresolved `r=4` frontier.

## Reproduce

First use the submitted workflow to regenerate the large local evidence with
Python 3.11+, C++17, Kissat 4.0.4, and drat-trim:

```sh
sh ../ramsey_r55_order3_ten_cycle_obstruction/verify.sh \
  --work /scratch/r55-order3-k10-review \
  --kissat /path/to/kissat/build/kissat \
  --drat-trim /path/to/drat-trim/drat-trim
```

Then run the reviewer reconstruction and replay:

```sh
python3 independent_check.py \
  --work /scratch/r55-order3-k10-review \
  --drat-trim /path/to/drat-trim/drat-trim \
  --report /scratch/independent_split_report.json
cmp report.json /scratch/independent_split_report.json
sha256sum -c SHA256SUMS
```

The review run used Kissat source commit
`8af8e56f174b778aef3aa45af9f739b2a5f492c2` and drat-trim source commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. The locally built Kissat binary
had SHA256 `9193d0d788f70d11046c7e965657c7096c9471ea96db2552a7d1544e925307cb`
and nevertheless regenerated all five byte-identical reference traces. The
drat-trim binary SHA256 was
`9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.

## Trust boundary

The accepted result still trusts the external theorem `R(4,5)=25`, the
unformalized graph-to-formula and normalization arguments, the reviewer source,
exact CPython semantics, compiler/runtime and hardware behavior, SHA256, and
the external drat-trim implementation. The solver verdict alone is not
trusted. Formula/proof generation state is preserved locally under
`/scratch/research-team-v2/tmp/reviewer-1/r55_order3_k10_split_review1_20260905`;
it is deliberately not part of the compact public evidence.
