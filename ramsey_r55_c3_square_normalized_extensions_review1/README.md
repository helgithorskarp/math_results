# Independent review of the normalized C3-square closure

This is reviewer-1's independent review of Discovery Net lemma
`bafkreiarcapyjjkofhas4uljy3wt5w5abbjl23hxnxphqacxacb5njggdi`, using
the submitted source at commit
`2263dc0a2195a242106af5db73aa33570ad85575`.

## Verdict and scope

Accepted: no Ramsey `(5,5;43)` graph admits a subgroup of automorphisms
isomorphic to `C_3 x C_3`. Combined with the previously reviewed exclusion of
an element of order nine, this proves globally that nine does not divide the
automorphism-group order. In particular, every nontrivial 3-subgroup has order
three and is cyclic.

This is a symmetry obstruction, not a construction. It produces no 43-vertex
Ramsey graph and does not prove `R(5,5) >= 44`. The further factorization
`|Aut(G)| = 2^a 3^b`, with `b <= 1`, imports the project's separate
prime-divisor exclusions; those were not rerun here.

## Centralizer normalization

The independently reviewed parent classification leaves exactly actions 9
and 10. Each has one fixed vertex, two quotient three-orbits, and four regular
nine-orbits for `H = F_3^2`; the quotient stabilizer lines respectively agree
or differ.

The added normalization is valid. Four regular `H`-sets may be permuted while
carrying coordinates identically. Because `H` is abelian, an independent
translation on a regular copy commutes with the diagonal `H`-action, as does a
cyclic translation of either quotient. These operations give the following
normal form after global complementation sets `x_1`, the color of the fixed
vertex to the first quotient, to one:

1. Permute the regular copies to sort their five-bit fixed/internal profiles.
2. Leave the first regular origin as anchor and translate each other regular
   copy to minimize its nine-bit word from that anchor.
3. Rotate each quotient to minimize its three-bit word from the same anchor.

Translations preserve every five-bit profile. A translation or quotient
rotation changes only its own constrained anchor word, so these choices do not
undo earlier ones. Moving the anchor is unnecessary because translating each
target copy already realizes every relative displacement. No linear basis
change on any regular copy is used.

[independent_check.py](independent_check.py) constructs both literal actions
from their stabilizer kernels and checks all 57 elementary maps used in the
normal-form procedure: 24 coordinate-identical regular-copy permutations, 27
translations of the three nonanchor copies, and six quotient rotations. Each
map commutes with both generators of `H` and induces a well-defined permutation
of pair orbits. The checker exhausts all `32^4 = 1,048,576` profile tuples per
action, all 512 regular words, and all eight quotient words. It obtains 64 and
four translation classes respectively. The `157,464` reported normalization
choices are sequential choices, not the order of a claimed subgroup.

## Formula and certificate audit

The submitted workflow was rerun serially with one worker. It regenerated both
formulas and proof traces byte-identically to the published values, excluded
indices 9 and 10, and left no open case. The run took 53.750705 seconds and its
largest child peak RSS was 140,392 KiB.

The clean-room checker imports no submitted module. For each action it:

* reconstructs all literal pair orbits under two independently built vertex
  generators;
* reconstructs the positive and negative Ramsey clauses from all
  `C(43,5) = 962,598` literal five-sets;
* verifies complement symmetry and the single valid normalization unit;
* reconstructs every profile comparator and local translation clause by truth
  table, obtaining exactly `1,488 + 1,344 + 8 = 2,840` tail clauses;
* compares every parent and tail DIMACS line, not merely aggregate counts or
  hashes; and
* freshly replays both proof traces with drat-trim.

The exact results are:

| action | variables | parent / full clauses | full CNF SHA256 | proof bytes | RAT core lemmas |
|---:|---:|---:|---|---:|---:|
| 9 | 105 | 211,323 / 214,163 | `e58d139ede296b86b44cb5d452c2cc80d374e0805e936dadfed5deb94cd7162f` | 4,359,167 | 138 |
| 10 | 103 | 210,907 / 213,747 | `3f583630b73b13026e24415838526984f376315aae9e0f5cc33a5f24e48c3420` | 5,517,636 | 88 |

Both replays returned `s VERIFIED`. The nonzero RAT counts confirm that these
are general DRAT certificates, not merely reverse-unit-propagation proofs.
The deterministic full audit is recorded in [report.json](report.json).

## Group-theoretic consequence

Suppose nine divided `|Aut(G)|`. A Sylow 3-subgroup would have order at least
nine, and the standard subgroup theorem for finite p-groups gives a subgroup
of order nine. Every group of order nine is either cyclic or elementary
abelian. A cyclic subgroup supplies an element of order nine, excluded by the
previously reviewed cyclic result. An elementary abelian subgroup is one of
the 18 actions in the independently reviewed parent cover: sixteen have
replayed parent certificates and the two residual actions have the checked
certificates above. Both alternatives are impossible.

Thus `9` does not divide `|Aut(G)|`. This deduction imports the accepted
18-action cover and its sixteen exclusions, the minimum-eleven motion theorem
used by that cover, and the independently reviewed cyclic order-nine
exclusion.

## Reproduce

First reproduce the submitted formulas and proofs, using an empty work
directory outside Git:

```sh
python3 ../ramsey_r55_c3_square_normalized_extensions/run.py \
  --work /scratch/r55-c3-square-normalized-review/submitted \
  --kissat /path/to/kissat/build/kissat \
  --drat-trim /path/to/drat-trim/drat-trim \
  --workers 1 --solve-seconds 180 --replay-seconds 300
```

Then run the clean-room review:

```sh
python3 independent_check.py \
  --source ../ramsey_r55_c3_square_normalized_extensions \
  --work /scratch/r55-c3-square-normalized-review/submitted \
  --drat-trim /path/to/drat-trim/drat-trim \
  --report /scratch/r55-c3-square-normalized-review/report.json
cmp report.json /scratch/r55-c3-square-normalized-review/report.json
sha256sum -c SHA256SUMS
```

The review used Python 3.11.2, Kissat source commit
`8af8e56f174b778aef3aa45af9f739b2a5f492c2`, and drat-trim source commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. The local binaries had SHA256
values `9193d0d788f70d11046c7e965657c7096c9471ea96db2552a7d1544e925307cb`
and `9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`
respectively.

## Trust boundary

This review independently checks the two new finite formulas, their complete
normalization layer, and their proof traces. Remaining trust lies in the
previously reviewed parent action classification and sixteen certificates,
the previously reviewed order-nine element obstruction, and ultimately the
minimum-eleven theorem's imported value `R(4,5)=25`. Computational trust lies
in this reviewer source, exact CPython semantics, SHA256, drat-trim, the
compiler/runtime, and ordinary hardware. It is not a proof-assistant
formalization.

The generated 30 MiB working state is intentionally outside Git at
`/scratch/research-team-v2/tmp/reviewer-1/r55_c3_square_normalized_review1_20260905`.
All processes completed; no background computation remains.
