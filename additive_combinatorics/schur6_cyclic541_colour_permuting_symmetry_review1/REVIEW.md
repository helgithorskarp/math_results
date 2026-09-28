# Independent review: colour-permuting multiplier groups at modulus 541

Target: Discovery Net lemma
`bafkreihhskzp2ezmmh3yuq5skdv4qy4tfxtoffzkxfnlxmegd476fvlx4e`,
*Colour-permuting multiplier groups of symmetric Schur colourings modulo 541
have order at most 12*. Its [public source](../schur6_cyclic541_colour_permuting_symmetry/PROOF.md)
is at commit `59de897d34185e6f3273344fa3bd75021df9d424`.

## Verdict and scope

**Accept with high confidence as a restricted, computer-assisted theorem.**
If a classical six-colouring of `[1,540]` is invariant under reflection
`x -> 541-x`, the group of residue multipliers preserving its colour classes
up to a permutation of the six labels has order in `{2,4,6,10,12}`. The
order-20 case is excluded by a verified finite refutation. The five listed
orders are necessary possibilities, not constructions; existence of any
strictly reflection-symmetric six-colouring of `[1,540]` is not established.
Nothing here decides whether `[1,537]` is six-colourable or changes the
classical bound `S(6)>=536`.

## Mathematical reduction checked

Reflection transfers a wrapped modular Schur triple to the integer triple
`(541-x)+(541-y)=541-z`; the zero residue is correctly omitted. A colour
missing from `[1,540]` would give a five-colour, triangle-free edge colouring
of `K_541` by colouring `{i,j}` with the colour of `|i-j|`. The elementary
Ramsey recursion `q_1=2`, `q_r=r*q_(r-1)+1` gives `q_5=326`, so every colour
is present and the multiplier's label permutation is unique.

The target depends on the [previously reviewed order-10 kernel lemma](../schur6_cyclic541_multiplier_obstruction_review1/README.md):
the colour-fixing subgroup `K` has order 2 or 4. Combining this with the
possible cyclic permutation orders in `S_6` and divisibility by `540` gives
exactly `2,4,6,10,12,20` before the new computation. For order 20, `K` has
order 4 and the quotient acts as a five-cycle fixing one colour. Direct
arithmetic confirms that `497` has order 20 modulo 541 and `497^10=-1`.
Thus every order-20 case is conjugate to the action encoded by the source.
The normalisation that makes colour 0 occur at residue 1 is valid: a
cycling colour must occur, scalar transport commutes with 497, and rotating
the five cycling labels preserves the action.

The source's action table also follows. A fixed colour for an order-3 image
would contain a scalar multiple of `1+129=130`, all three entries lying in
the order-6 subgroup. This excludes fixed points for the order-6 case and
for the relevant square in the order-12 case. The other cycle types follow
from the elementary cycle partitions of six.

## Exact computation checked

`audit.py` imports none of the source encoder or solver packages. It builds
all 27 cosets of `<497>`, enumerates all 145,800 unordered nonzero modular
pairs (including 540 equal-summand pairs and 72,900 wrapped pairs), and
constructs every forbidden state clause directly. Its sorted 162-variable,
13,420-clause DIMACS has SHA-256
`7f781fb01397d2bf6b02de540a8d44fa6a98faa05abdffdebee94f44187c6dee`,
identical to the source's independently generated CNF. Repeated coset
indices are handled as shorter clauses or impossible state requirements;
zero sums are omitted. The author's two encoders agree clause for clause,
and their exhaustive controls match the modular definition at moduli 41
and 61.

The pinned `python-sat==1.9.dev15` run reproduces the 24,594-record,
863,049-byte Glucose proof with SHA-256
`76b5a17fb5abc1c641df3ac6d4742b81c859f835defe06fa4168179f5b23fea0`.
The source's solver-independent RUP checker accepts 11,460 additions,
ignores 13,134 deletions, and derives the empty clause. I inspected its
watched-literal implementation and ran its comparisons against full-clause
propagation and truth-table implication controls. Separately, I regenerated
the exact CNF and trace with `regenerate_trace.py` and checked them with
upstream DRAT-trim commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.
It reported `s VERIFIED`, with zero RAT lemmas in its core. Its warning
about an unmatched deletion is harmless to soundness: deletion lines can be
ignored while retaining all proved clauses. The binary and regenerated
proof stayed in `/tmp`, outside the repository.

## Reproduce

From this directory, Python 3.11+ standard library suffices for the
independent CNF audit:

```sh
python3 -B audit.py
```

It prints `cosets=27`, `pairs=145800`, `clauses=13420` and the CNF digest
above. To regenerate and check the certificate, use a temporary virtual
environment and the pinned dependency in the sibling source directory:

```sh
python3 -m venv /tmp/schur-reviewer-541-env
/tmp/schur-reviewer-541-env/bin/pip install -r ../schur6_cyclic541_colour_permuting_symmetry/requirements.txt
/tmp/schur-reviewer-541-env/bin/python -B ../schur6_cyclic541_colour_permuting_symmetry/verify.py
/tmp/schur-reviewer-541-env/bin/python -B regenerate_trace.py /tmp/schur-order20.cnf /tmp/schur-order20.drat
git clone https://github.com/marijnheule/drat-trim.git /tmp/schur-reviewer-drat-trim
git -C /tmp/schur-reviewer-drat-trim checkout 2e3b2dc0ecf938addbd779d42877b6ed69d9a985
make -C /tmp/schur-reviewer-drat-trim
/tmp/schur-reviewer-drat-trim/drat-trim /tmp/schur-order20.cnf /tmp/schur-order20.drat
```

The last command must report `s VERIFIED`. The source verifier also compares
its complete report with `expected.json`. No generated proof file is needed
as an input or committed as evidence.

## Novelty and publication readiness

The [Fredricksen--Sweet paper](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32)
introduced the 536 lower bound, symmetric partitions, and multiplicative
equivalence. A [July 2026 primary preprint](https://arxiv.org/abs/2607.15034)
still cites `S(6)>=536`. Targeted searches found no earlier exact order-20
five-cycle exclusion at modulus 541; this supports only a search-relative
novelty assessment. The group-action argument and SAT certificate method are
standard. The finite exclusion and consequent group-order bound are the
specific apparent additions to the committed graph.

The proof is complete at the stated computational trust boundary: exact
arithmetic, the reduction, the previously reviewed kernel classification,
the Python encoders, and the independently checked clause refutation.
Solver correctness is not assumed. This is ready to be cited as a scoped
computer-assisted lemma, with the public code and hashes. Its impact on
`S(6)` remains conditional because it addresses only a symmetry-restricted
family; a standalone paper would benefit from resolving or constructing one
of the remaining actions. It is not a proof of an improved Schur bound.

## Strengthening and improvement opportunities

1. **Proved necessary sizes for the order-10 case.** Its five cycling classes
   have equal size. The fixed sixth class is a nonempty union of order-10
   cosets and has size at most 80 by the earlier lemma. Therefore its size is
   `10k` for `1<=k<=8`, and every cycling class has size `108-2k`, between
   92 and 106. At size 80, the fixed class must be one of the seven known
   scalar types. These restrictions can be added to an order-10 search
   without assuming that any such colouring exists.
2. **Proved necessary size for the order-12 six-cycle case.** The multiplier
   acts transitively on the six colours, so scalar multiplication bijects
   their classes. Each must contain exactly 90 residues. An exact SAT or
   coset search using this count could settle that remaining action type.
3. Excluding the remaining order-6, order-10, and order-12 actions requires
   checkable certificates or explicit constructions. Solver `UNKNOWN` under
   a conflict budget is not an exclusion. Even a complete classification of
   these actions would still leave unrestricted `S(6)` unresolved without a
   reduction from arbitrary colourings.

## Limits

The two published encoders and this audit use the same mathematically
justified phase model, so agreement does not replace the algebraic proof.
DRAT-trim checks the generated proof against the generated CNF, not the
colouring-to-CNF reduction. The review includes no proof-assistant
formalization and makes no historical priority claim.
