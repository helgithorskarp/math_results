# A matched monochromatic six-seed is impossible in partial XOR618 colorings

six-vdw-3, researcher; 2026-10-02. Author-checked computer-assisted lemma.
The mathematical premises are cited explicitly. Separate field-ladder,
actual-cyclic, literal control and strict positive-RUP mechanisms are used;
external independent review and formalization are not claimed.

Let `q=103`, `M=618`, `epsilon=(0,0,0,1,1,1)` on Z6, and
`E={6,54,102}` in F103. For an arbitrary orientation
`u:F103\E -> {0,1}`, define the partial coloring

    c(t)=u(t mod103) XOR epsilon(t mod6),  t in Z618,

whenever `t mod103` is outside E. Assume every wholly regular cyclic
seven-term arithmetic progression with nonzero step in Z618 has both colors.
The hypothesis includes cyclic progressions with repeated points.

**Lemma.** The six orientation values `u(0),...,u(5)` cannot all be equal.
The lemma also holds when the seed and hole set are transported together by
any invertible field-affine map. Values at the other regular points remain
arbitrary; invariance under a local reflection is not a hypothesis.

**Endpoint corollary.** For holes `{0,1,2}`, the regular field progression
`{15,30,45,60,75,90}` must be mixed. Thus a monochromatic five-seed
`{30,45,60,75,90}` of color b forces `u(15)=1-b`, and a monochromatic
five-seed `{15,30,45,60,75}` forces `u(90)=1-b`.

Equivalently, with holes `{5,53,101}`, a monochromatic seed `0..4` forces
`u(102)=1-b`; with holes `{6,54,102}`, it forces `u(5)=1-b`.
These statements concern a specified partial XOR618 construction. They
do not exclude all three-hole geometries or give a length3704 witness or
an improved symmetric two-color/seven-term van der Waerden lower bound.

## Complete necessary input domain

Suppose for contradiction that `u(0)=...=u(5)=b`. Exchange the two colors
so b=0. The two explicit mathematical premises are:

* [9311, four-geometry two-satellite rule](../single-satellite618/PROOF.md),
  contribution `bafkreiadzldf6d5p3gng3khhmd3ul72bnntyzhxvysmj3owig7sabv3s6y`,
  source `b18c33b5f51ce2c6b9c9bdb092cbdb5871b09b78`.
* [9359, matched six-seed three-satellite rule](../six-seed-satellite618/PROOF.md),
  contribution `bafkreif6ri5nsn5tquosbma5hny3myl4dhhg5iaobsamkfo6ayp6l3a3l4`,
  source `a15b0aa3377c30ede798a56ad5d2141c510302c4`.

These premises, including9311's earlier [9205 input](../five-seed-satellites618/PROOF.md),
are not reproved by this source restart. Their written proofs are byte-pinned
in expected.json. From9311 applied to the adjacent five-seeds `0..4` and
`1..5`, at least two opposite values occur in each of

    F={101,52,53,55},  G={7,53,55,56}.

For the second application translate the five-seed by minus one, giving
the fully covered holes `{5,53,101}`. Its satellite102 is the first seed's
monochromatic endpoint0. The remaining four satellites transport to G.
For the first application the extra endpoint5 is monochromatic, leaving F.
Premise9359 also forces at least three opposite values in

    Q=F union G={7,52,53,55,56,101}.

Among all64 binary inputs on Q, exactly34 satisfy these necessary rules.
Their weights3,4,5,6 occur12,15,6,1 times. Reflection `x -> 5-x` stabilizes
the matched seed and E and reverses the ordered Q word. Its quotient has
19 classes:6,9,3,1 by weight, with four reflection-fixed inputs. The
stabilizer consists of identity and that reflection; cover_check.py verifies
all10506 field-affine maps. Fixed local inputs still leave the other88
orientation bits unrestricted, including at all four fixed inputs.

The generator enumerates combinations and reverses their words. The
separate cover checker enumerates all64 masks, evaluates the actual field
reflection, verifies every orbit member in cover.json and verifies every
transported fixed word. This is complete necessary input coverage rather
than a count of global extensions. Any proposed counterexample must belong
to one of these34 inputs, hence one of the19 explicitly refuted classes.

## CRT transport and exact model

For a field map `x -> ax+b`, choose A,B with `A=1 mod6`, `A=a mod103`,
`B=0 mod6`, `B=b mod103`. For `a!=0`, A is coprime to618. The bijection
`t -> At+B` preserves epsilon and nonzero cyclic steps. Transporting the
entire orientation through its inverse preserves the regular cyclic
hypothesis. Four specific lifts are checked at all618 points each:

| Field action | CRT action modulo618 | Use |
| --- | --- | --- |
| `x -> x-1` | `t -> t+102` | Adjacent five-seed premise |
| `x -> 4-x` | `t -> 205t+210` | Production normalization |
| `x -> 5-x` | `t -> 205t+108` | Input reflection |
| `x -> 15x+15` | `t -> 427t+324` | Holes0,1,2 endpoint corollary |

The last field map sends E to `{0,1,2}` and `0..5` to
`{15,30,45,60,75,90}`, proving the stated corollary once the lemma is proved.

Production models use reflection `x -> 4-x`. The holes become `{5,53,101}`,
and every fixed twelve-point core is

    (0,1,2,3,4,6,51,52,54,55,100,102).

Points `0,1,2,3,4,102` are all zero. Each representative prescribes three
through six ones among `(6,51,52,54,55,100)`, exactly as recorded in
cover.json and independently listed in check.py.

There are100 regular field columns. For each unordered regular pair,
introduce `p_xy=u(x) XOR u(y)`, giving4950 variables. Gauge `u(0)=0` is
allowed by global color exchange. Four clauses for each triangle
`(0,x,y)` forbid odd parity and force `p_xy=p_0x XOR p_0y`. There are19404
such clauses, so consistent pair assignments are in bijection with anchored
orientations.

For each wholly regular field seven-AP `x_j=a+jd`, require the four parities
`p_(x_j,x_(j+3))`, j=0..3, to be mixed, with one positive and one negative
four-literal clause. Field steps1..51 suffice by reversal. The4236 distinct
ladders give8472 clauses. Eleven signed root-pair units fix the remaining
core values. Each of the19 CNFs has4950 variables/27887 clauses and88 free
orientation bits. The fixed local input represents all `2^88` assignments
to those other bits. No global weight counter, outside symmetry constraint,
extra growth cut or global no-five/no-six hypothesis is added.

The independent auditor byte-pins the credited actual-cyclic base checker
from9311/sourceb18. It enumerates all381306 actual `(start,step)` pairs in
Z618:73314 meet holes;307992 are retained. Of these3000 have constant field
coordinate and are automatically mixed by epsilon. The other phase relations
give4236 distinct field-order groups. For each group, actual phase words
and their complements are exactly the16 orientation words where the four
distance-three parities agree. Thus the signed ladder clauses precisely
forbid monochromatic regular cyclic progressions.

The actual-cyclic base is reconstructed once per Python mode and compared
with every signed model. The old singleton literal/decoder is never used.
This source has a literal actual-cyclic checker and pair decoder for all
new words. Additionally it checks every rooted twelve-bit input against
the eleven units of each model:38912 inputs, exactly19 matching words.

## Nineteen strict refutations

All19 new instances returned native UNSAT proposals below the unchanged
100000-conflict/35-second guard; the maximum was47381 conflicts. Solver
output and DRAT conversion are untrusted. Each converted candidate was
replayed normally and under Python `-O` by the
[credited positive-only RUP checker7428](../../../van_der_waerden_618_binary_fibers/check_rup_lrat.py),
source `223f0eaa45d24ff924e10edaa1e327fbf8a7259f`, SHA256
`55543f905d42aaf0955906f97a8484ec8522a182512b1d2e8fe132bb45cb545c`.
The checker enforces domains, fresh increasing addition IDs, valid deletions,
all positive propagation hints and a checked empty clause; negative RAT
hints are rejected. The complete19-proof totals per mode are606173 checked
additions and16178753 propagation hints. Individual hashes/counts are frozen
in [expected.json](expected.json). Every model has a strictly checked empty
clause, so none of the34 necessary inputs has any outside-cyclic extension.
Together with9311/9359 this proves the matched six-seed exclusion.

Source was frozen before a standalone reconstruction of all19 models,
the complete cover, literal signed-unit inputs, small positive controls and
strict refutations in both modes. That reconstruction treats18 cached
proof candidates as untrusted and freshly solves/converts case19. All19
original research proposals were fresh. Default reproduce.py regenerates
all19 proposals; cached candidates are optional and always checked strictly.
See [VALIDATION.md](VALIDATION.md) and [verification.json](verification.json).
Large CNFs, DRAT/LRAT corpora, binaries and logs are regenerated outside Git.

For the4096 joint twelve-point words, the earlier two mixed-core cuts
accept4082, the cited two-satellite rules accept4022, and adding complete
matched six-seed exclusion leaves3952. The intervening9359 filter left4020.
These are necessary local filter counts; no surviving word is asserted to
extend to a global coloring.

## Applicability and trust boundaries

Every wholly regular monochromatic cyclic seven-AP has an integer
representative in1..2472: reverse if needed to make the positive difference
at most309 and choose a start in1..618. Its last point is at most
`618+6*309=2472`. Therefore arbitrary colors at actual hole copies cannot
repair this forbidden regular pattern in a proposed XOR618-structured
length3704 coloring. This remains conditional on the regular structure.

The field model/actual-cyclic audit, complete finite coverage, ordinary CRT
and pair-parity arguments, cited mathematical premises and exact RUP kernel
are explicit trust boundaries. The pair mechanism is credited to
[8985](../separable618-exclusion/PROOF.md); its intact-carrier exclusion is
not a premise. Same-author separate algorithms are not external review.
No prior UNKNOWN model was retried or reinterpreted, and caps were unchanged:
one serial CPU-intensive job, all threads one,1CPU/2GiB; conversion25 seconds
internal/30 external and strict replay50 seconds per child stage. Timeout,
UNKNOWN or incomplete enumeration would provide no mathematical exclusion.

[Monroe's primary Tables1 and2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/),
the [author source](https://github.com/hmonroe/vdw), and
[Herwig et al.'s construction paper](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
were live rechecked2026-10-02: two colors/length seven `>3703` is the lane
seed. Monroe's length-first W(7,2) is our color-first W(2,7). Asymmetric
red3/bluek progressions are a different problem. These bounded checks are
not an exhaustive current-record or historical-priority claim.
