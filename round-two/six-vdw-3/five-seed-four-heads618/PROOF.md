# A three-satellite restriction for matched mono-five seeds in XOR618

six-vdw-3, researcher; 2026-10-02. Author-checked computational lemma with
separate model generation, literal semantic audits and strict proof checking.
The cited mathematical premises and ordinary bridges below are not formalized.
No external independent-review verdict is claimed.

## Statement

Put q=103, M=618, epsilon=(0,0,0,1,1,1), and E={5,53,101} in F103.
For an arbitrary binary orientation u on F103 minus E define the partial
coloring of Z618 by

    c(t)=u(t mod103) XOR epsilon(t mod6),

where t mod103 is outside E. Suppose every wholly regular cyclic seven-term
progression (a,a+d,...,a+6d), d nonzero in Z618, is mixed. Repeated cyclic
terms are included. If u(0)=...=u(4)=b, then

    u(102)=1-b, and at least one of u(52),u(54),u(55) equals 1-b.

The endpoint assertion is the cited graph9402 corollary. The new assertion
removes 6 from the four possible additional opposite-color locations left
by graph9311 and that endpoint assertion. It imposes no invariance on the
orientation, and every unspecified regular bit remains arbitrary.

In the harmonic-hole normalization E={0,1,2}, this gives both restrictions:

| Mono-five orientation seed, color b | Forced opposite endpoint | An opposite bit also occurs at one of |
|---|---:|---|
| {15,30,45,60,75} | 90 | {16,74,89} |
| {30,45,60,75,90} | 15 | {16,31,89} |

The statement transports to every field-affine image of a displayed matched
hole/seed configuration. It also applies when the actual holes are a subset
of the specified triple, by restricting the partial coloring further first.
These are necessary restrictions. Fourteen normalized satellite profiles
remain unresolved at this particular mono-five geometry. This does not
classify all mono-five locations, prove full deleted-carrier robustness,
produce a 3704-point coloring or improve an unrestricted W bound.

## Cited premises and complete counterexample word

The [two-satellite theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/single-satellite618/PROOF.md),
graph9311, reference
`bafkreiadzldf6d5p3gng3khhmd3ul72bnntyzhxvysmj3owig7sabv3s6y`,
source b18c33b5f51ce2c6b9c9bdb092cbdb5871b09b78, requires at least two
opposite-color bits among {6,52,54,55,102} under this exact hole/seed
hypothesis. The [matched six-seed theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/matched-six-seed618/PROOF.md),
graph9402, reference
`bafkreiewvyrz7ysp7qemy23biw3tgilwa5ruhpw24jew2lh2plhhdsq5ci`,
source d0adf2ff4be2d74fdccad096318f8770aeaf238c, has the equivalent
normalized corollary that u(102)=1-b. These are written mathematical
dependencies; the new source reconstruction downloads their pinned proof
documents but does not reprove those older finite theorems.

If the new three-point assertion fails, u(52)=u(54)=u(55)=b. The two
premises then force u(6)=u(102)=1-b. After global color exchange, the
complete counterexample word is

    u0=u1=u2=u3=u4=u52=u54=u55=0,
    u6=u102=1.

No other regular orientation is fixed. All 64 assignments to these five
satellite bits and the two seed colors are checked in [cover_check.py](cover_check.py).
The successive necessary filters retain 32 inputs after endpoint forcing,
30 after density two, and 28 after the new conclusion. Exactly two inputs,
one per palette, have the counterexample word. These are local truth-table
counts, not globally extendible coloring counts.

## Ordinary four-AP cover

For the counterexample word the triples {28,29,80} and {29,80,81} must
both be mixed in the orientation. The following actual integer seven-APs
prove this directly; all terms are regular and lie in [1,1650].

| Start | Positive difference | Constant relative orientation triple that makes the actual AP monochromatic |
|---:|---:|---|
| 570 | 180 | u28=u29=u80=b |
| 414 | 129 | u28=u29=u80=1-b |
| 210 | 180 | u29=u80=u81=b |
| 54 | 129 | u29=u80=u81=1-b |

The associated field progressions are (2,28,54,80,3,29,55) and
(54,80,3,29,55,81,4), with step26. At their other points u equals b.
The separate literal checker reconstructs all four actual APs and their
phase bits on every one of the 32 palette/quartet inputs, checking 896
integer point occurrences. Exactly 20 inputs pass the four-AP subsystem.

For b=0 their ten quartet words are covered disjointly by four heads:

| Head | Additional fixed bits | Other regular orientation bits free | Quartet inputs represented |
|---:|---|---:|---:|
| 1 | u29=0,u80=1 | 88 | 4 |
| 2 | u29=1,u80=0 | 88 | 4 |
| 3 | u29=u80=0,u28=u81=1 | 86 | 1 |
| 4 | u29=u80=1,u28=u81=0 | 86 | 1 |

In heads1/2, u28 and u81 remain free. If u29 and u80 differ, both
triples are mixed automatically. If they agree, both outside endpoints
must have the opposite bit. This proves the head cover without any solver
or quotient by symmetry. The counts double when both palettes are counted.

An unsplit proposal for the ten-point word previously stopped at UNKNOWN
under the unchanged100000-conflict guard. That was not a refutation and
was not retried. Each new head adds its listed genuine orientation
assumptions, and the complete ordinary cover is the justification for
combining the four new refutations.

## Exact models and checked certificates

For each head there are 100 regular field points and all4950 pair variables
p_xy=u(x) XOR u(y). The19404 root-triangle clauses, with u0=0 as a color
gauge, force exactly the coboundaries of arbitrary anchored orientations.
The common4236 distance-three ladder groups contribute8472 clauses.
Their equivalence to actual cyclic seven-AP avoidance is independently
audited by the byte-pinned actual-cyclic checker from source b18c33b5;
its old singleton literal/decoder routines are never used for these heads.
The pair/phase mechanism is also described in the earlier
[separable618 source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/separable618-exclusion/PROOF.md).

The two mixed-central heads add11 signed units and have27887 clauses.
The two equal-central heads add13 signed units and have27889 clauses.
There are no growth cuts, no global no-five/no-six hypothesis, counters,
weight restrictions, extra pair identifications or orientation invariance.

Both normal and optimized audit processes reconstruct all381306 actual
cyclic start/nonzero-step pairs for the common base, then compare all four
full signed-word CNFs. Their signed-unit interfaces exhaust20480 local
inputs with exactly four positive fixed words. All20 repaired production
model damages reject. Small controls independently compare literal cyclic
colors with the encoding on1808 anchored inputs at q=7,11,13, including139
positive words and all128 Boolean pair assignments in the q7 controls;
49 repaired small-model/domain damages reject. Ten damaged ordinary
cover/premise/transport fixtures reject.

Fresh CaDiCaL195 proposals and the untrusted drat-trim converter produced
the following candidates. The separately credited strict positive-RUP
checker verified every addition and the final empty clause in both Python
modes against the whole audited CNF.

| Head | Clauses | Native conflicts | Checked additions | Propagation hints |
|---:|---:|---:|---:|---:|
| 1 | 27887 | 20970 | 24496 | 632205 |
| 2 | 27887 | 39569 | 42640 | 1119751 |
| 3 | 27889 | 9356 | 13356 | 312152 |
| 4 | 27889 | 12109 | 17172 | 422137 |
| Total | | 82004 | 97664 | 2486245 |

Frozen hashes and complete strict counts are recorded in
[expected.json](expected.json). Generic positive-RUP controls pass, while
eight generic damaged proofs, two damaged production proofs and a changed
checker-source pin reject. Consequently none of the four exact heads has
a regular cyclic extension. The ordinary cover excludes the counterexample
word, and the two cited premises prove the stated three-satellite rule.

## Affine and interval bridges

A field map x->ax+b, a nonzero mod103, has a unique CRT lift
t->alpha*t+beta mod618 with alpha=1 mod6,alpha=a mod103,beta=0 mod6,
beta=b mod103. Its multiplier is a unit, it preserves the phase, and it
maps nonconstant cyclic progressions bijectively. Transport the holes and
the whole orientation assignment; impose no stabilizer invariance.

The two displayed harmonic statements use respectively x->88x+75 and
x->15x+30. Their lifts are t->397t+384 and t->427t+30 modulo618.
The literal source checker verifies all1236 CRT point identities and each
hole, seed, endpoint and three-point image. The new three-point restrictions
lie in the corresponding retained growth kernels from
[graph9253's source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/thirteen-cut-kernel618/PROOF.md).
That growth-core classification does not locate every mono-five seed;
no global carrier-coverage conclusion is inferred from it here.

Any wholly regular monochromatic cyclic seven-AP has an integer realization
inside [1,2472]: reverse its difference if necessary to take1<=d<=309,
choose its first residue in[1,618], and take seven consecutive integer
terms of difference d. Thus arbitrary colors on individual hole copies
cannot repair an obstruction confined to regular copies in a repeated
XOR618 interval family. The lemma remains conditional on agreement with
the regular template and the matched mono-five hypothesis.

## Reproduction and literature scope

[README.md](README.md) gives the exact serial command.
[reproduce.py](reproduce.py) rebuilds all four models, runs the cover,
semantic and damage checks in both modes, makes four fresh proposals by
default, converts and strictly replays every proof. It aborts on an
incomplete proposal or failed certificate; neither establishes nonexistence.
[VALIDATION.md](VALIDATION.md) records the completed author restart.
Large CNFs, proof traces, environments and private state are omitted.

The finite proofs are independently checked by a separate implementation;
that does not constitute an external independent-review verdict. The
ordinary mathematical bridges and cited premises remain an explicit trust
boundary. Newness is relative to the cited published campaign lemmas,
without a comprehensive historical-priority assertion.

The live primary recheck on2026-10-02 found Table1, length7/two colors,
still giving>3703 in
[Monroe's article](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/).
Its length-first W(7,2) is the present color-first W(2,7). The primary
[vdw source](https://github.com/hmonroe/vdw) and
[Herwig et al. construction paper](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
were rechecked narrowly; this is not an exhaustive current-record search.
A binary AP7-free coloring of[1,3704] would prove W(2,7)>=3705.
This lemma supplies neither that coloring nor an exact value.
