# Independent review: anchor-linked M214/P4 survivor

## Verdict

**Accept with high confidence, within the stated relaxation scope.** At source
commit `11a6ff8ea2421de256a87aca794477f91defbba1`, the contribution gives an
exact feasible point for the complete M214 four-vertex moment LP after the
nine selector exclusions and all 83 anchor equations. Its sole nonzero
selector is \(y_{278}=1\), where root 278 is exactly
\((C77,12,0,BB)\).

The claimed 11,970 neighborhood forbidden-state rows are also valid for every
moment lift of an actual Ramsey graph and strictly separate the displayed
point. The system after adding those rows remains **undecided**.

This is an exact fractional pseudomodel. It does not prove Boolean feasibility
of root 278, construct a 43-vertex Ramsey graph, exclude a Boolean root or
M-slice, or improve a Ramsey bound.

Reviewed source:
[package on main](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_anchor_linked_p4_survivor).
The immutable source identity is the commit above; its package-manifest
SHA-256 is
`8b701fe57bb3896b8779d266187289d1a39b000f2126abc2bc14f68c297c38a6`.

## Reproduction and independent implementation

The author's clean sequential replay regenerated the inherited
511,537,255-byte OPB, the 83 anchor equations and the 11,970 proposed rows,
then returned
`EXACT_COMPLETE_ANCHOR_LINKED_P4_INTEGRAL_SELECTOR_SURVIVOR`. The base,
certificate, link and forbidden-row SHA-256 values were respectively:

- `9a3f66683a9cfad87d4ed0cdeb6bd14e5955540b05a8b48576b9f5653dcbd609`;
- `576f7675a093293dcfb8f03f4bf11540ecfacb485b21d608844d29183e734715`;
- `f2bef9213e141982f863601df3dc57d07ee20b1d5f0b9bcb559799a2187bafa1`;
- `5c1a658ea797e95ab7cb9076373bd6f055220a923c445c00ac38854210f44318`.

The checker in this directory imports none of the contribution modules. It
uses a different reconstruction order: first it expands the 345 canonical
four-class tables and their 3,076 state orbits, then derives every physical
triple and edge marginal, verifies their consistency, and reconstructs all
98,758 inherited coordinates. The certificate expands to 4,699 nonzero
states and has exact common denominator

\[
125368991767988746642012018235328661030993837537249251106759096554753901781865052800.
\]

The independent audit then:

- streams, hashes and evaluates every one of the retained OPB's 2,983,003
  rows, including all 87 equalities;
- independently enumerates the 389 roots, checks the root-table ordering and
  selected root, and matches all 32,287 physical root-unit rows;
- checks 903 red and 903 blue codegree rows, 21,762 coupled-column rows,
  264,560 moment-hull rows, 98,728 triangle-atom rows and 1,806 degree-star
  equalities;
- checks all 123,410 physical four-sets, 7,898,240 nonnegativity rows,
  3,949,120 shared triple marginals and 74,513 footprint identifications;
- reconstructs every coefficient of all 83 anchor equations and verifies the
  nine zero cuts and one-hot selector; and
- derives both 21-vertex anchor neighborhoods, matches all 11,970 source
  five-set clauses and emitted state rows, and exhausts the underlying 2,048
  Boolean five-vertex cases.

The resulting presentation has 8,023,409 variables, 15,417,040 rows and
4,149,019 equalities. All 48 substantive fields shared with the author's
result agree exactly.

## Mathematical audit

Because \(y_{278}=1\) and every other selector is zero, the point lies in the
fully selected continuous root-278 relaxation itself. It therefore lies in
the union—and hence the convex hull—of the existing continuous selected-root
LPs. This justifies the limited conclusion that further convexification of
that unchanged disjunction cannot remove this point. It says nothing about
the convex hull of Boolean Ramsey graphs or root systems with additional
physical constraints.

All 389 roots independently reconstruct to the same anchor-zero star:

\[
N_R(0)=\{1,\ldots,7\}\cup\{15,\ldots,28\},\qquad
N_B(0)=\{8,\ldots,14\}\cup\{29,\ldots,42\}.
\]

If four vertices in \(N_R(0)\) were all mutually red, they and anchor 0
would form a red \(K_5\); the complementary statement holds in
\(N_B(0)\). Thus the all-red or all-blue four-state mass must be zero in
every actual Ramsey graph and in every convex combination of its moment
lifts. This proves the entire family of
\(2\binom{21}{4}=11{,}970\) rows without importing a solver verdict.

The certified point has 3,813 positive forbidden blue masses and no positive
forbidden red mass. In particular, its all-blue mass on
\(\{39,40,41,42\}\) is

\[
\frac{652999482457240645298711994224426575470284590794411979469915505515258922049561}
{5936031807196436867519508439172758571543268822786422874373063283842514288914065}
=0.110006\ldots>\frac{11}{100}.
\]

The new rows are valid consequences of the Boolean graph interpretation, but
not consequences of the continuous LP: the independently checked point
satisfies the latter and violates the former.

## Reproduction commands

Use Python 3.10 or newer and a complete source checkout pinned to the reviewed
source commit. The author replay needs roughly 2 GB of scratch space:

```sh
python3 -B ramsey_r55_m214_anchor_linked_p4_survivor/reproduce.py \
  /scratch/path/author-replay
python3 -B ramsey_r55_m214_anchor_linked_p4_survivor_review1/independent_check.py \
  --source /path/to/math_source_code_open \
  --replay /scratch/path/author-replay
```

The second command emits the JSON in `EXPECTED_RESULT.json`. Both review runs
were sequential; the published certificate needs no solver or network
service. The approximately 488 MiB generated OPB is intentionally omitted and
regenerated from hash-pinned public builders.

## Trust boundary, novelty and readiness

Literal rational feasibility, selector/link satisfaction, the physical P4
marginals and the forbidden-event implication were independently checked.
The Ramsey interpretation still imports the previously reviewed completeness
of the M214 root normalization and P4 coordinate formulation. Treating the
nine zero cuts as valid Ramsey exclusions additionally imports the upstream
local-extrema/catalog premises; literal feasibility with those coordinates
fixed to zero does not. Remaining computational trust lies in two
unformalized implementations, CPython exact integer/rational semantics,
SHA-256 and ordinary hardware.

Candidate-specific searches found no public occurrence of this M214/root-278
certificate or anchor-linked construction. The general techniques—finite
moment relaxations, conditioning on fixed bits and excluding impossible local
events—are classical, so only the exact graph-grounded certificate and its
quantified relaxation failure appear potentially novel. The result is ready
as a reproducible campaign checkpoint, not as evidence for
\(R(5,5)\ge44\). Current primary context remains Angeltveit--McKay's
[upper-bound result](https://arxiv.org/abs/2409.15709).

## Strengthening and improvement opportunities

The complete family of 11,970 rows has an equivalent one-row formulation.
Every P4 atom already satisfies \(p\ge0\), so

\[
-\sum_{A\in\binom{N_R(0)}4}p_{A,63}
-\sum_{A\in\binom{N_B(0)}4}p_{A,0}\ge0
\]

holds if and only if every summand is zero. This replaces 11,970 sparse rows
by one dense row and reduces the next presentation from 15,429,010 to
15,417,041 rows without changing its feasible region. It is a proved
formulation compression, not a stronger inequality; both encodings should be
benchmarked because sparsity may matter more than row count.

The decisive mathematical next step remains an exact survivor or independently
checkable infeasibility certificate for this strengthened system. If it is
feasible, the next certificate should report which additional forbidden
five-vertex events remain positive. If it is infeasible, a Farkas or exact
solver certificate should be published with a small independent checker.
Neither outcome follows from the present review.
