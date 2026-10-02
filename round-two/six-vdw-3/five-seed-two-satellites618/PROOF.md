# A two-satellite restriction for matched mono-five seeds in XOR618

six-vdw-3, researcher; 2026-10-02. Author-checked computer-assisted lemma.
Separate generation, actual cyclic-color audits and strict positive-RUP
checking are used. The ordinary bridges and cited premise are not formalized;
an external independent-review verdict is not claimed.

## Statement

Let q=103, M=618, epsilon=(0,0,0,1,1,1), and E={5,53,101} in F103.
For arbitrary binary u on F103 minus E put

    c(t)=u(t mod103) XOR epsilon(t mod6)

outside the hole columns. Suppose every wholly regular cyclic seven-term
arithmetic progression in Z618 with nonzero difference is mixed. Progressions
with repeated cyclic terms are included. If u(0)=...=u(4)=b, then

    u(102)=1-b, and u(54)=1-b OR u(55)=1-b.

The endpoint assertion is inherited. The new assertion strengthens the
[committed three-satellite rule](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/five-seed-four-heads618/PROOF.md),
graph9457, by eliminating52 as the sole opposite location among52,54,55.
No invariance of u or additional restrictions on unspecified bits are imposed.

For harmonic holes E={0,1,2}, the two transported conclusions are:

| Mono-five orientation seed, color b | Opposite endpoint | An opposite also occurs at one of |
|---|---:|---|
| {15,30,45,60,75} | 90 | {74,89} |
| {30,45,60,75,90} | 15 | {16,31} |

Every field-affine image of a displayed matched hole/seed configuration has
the corresponding restriction. The statement also applies if actual holes
form a subset of the displayed triple, by restricting to that triple first.
These are necessary local restrictions. Twelve relative satellite profiles
remain at this geometry; their global extendibility is not asserted.
The result gives neither full deleted-carrier robustness nor a3704-point
coloring or an improved unrestricted two-color/seven-term W bound.

## Complete joint counterexample domain

The mathematical premise is graph9457,
`bafkreie57fszbji6sez2l42kd53mx2dxs7bsvgnmzpai33lvqig4fmb5k4`,
source00dd57d625b56fd84901cd0a14862b90034ad73f. It forces102 opposite
and an opposite among52,54,55 under exactly the present hole/seed hypothesis.
Its endpoint follows from the earlier
[matched six-seed theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/matched-six-seed618/PROOF.md),
graph9402. This restart downloads the pinned9457 proof document; it does not
reprove that mathematical premise or its ancestors.

Failure of the new assertion gives u54=u55=b, so9457 forces u52=u102=1-b.
After global color exchange the complete nine-point parent word is

    u0=u1=u2=u3=u4=u54=u55=0,
    u52=u102=1.

Crucially, u6 is free. This joins both older masks2 and3, whose only difference
is u6. The other91 regular orientations have no fixed-word units.
[cover_check.py](cover_check.py) exhausts all64 assignments to the five
satellites{6,52,54,55,102} and both seed colors. Endpoint forcing leaves32;
the9457 ternary rule leaves28; the new binary rule leaves24. The four
counterexample inputs comprise both palettes and both u6 choices. These
are local truth-table counts, not globally extendible-coloring counts.

## Ordinary four-AP cover

The following actual integer APs are wholly regular and lie in[1,1650].
They force both orientation triples{28,29,80} and{29,80,81} to be mixed.

| Start | Positive difference | Relative constant triple giving a monochromatic actual AP |
|---:|---:|---|
| 570 | 180 | u28=u29=u80=b |
| 414 | 129 | u28=u29=u80=1-b |
| 210 | 180 | u29=u80=u81=b |
| 54 | 129 | u29=u80=u81=1-b |

The corresponding field rows, of step26, are
(2,28,54,80,3,29,55) and(54,80,3,29,55,81,4).
Only u2=u3=u4=u54=u55=b is needed for this cover; neither u6 nor u52
is used in its literal AP argument. The cover was first exhibited in9457;
here it applies to a different parent domain with one fewer fixed orientation.
The independent checker imports neither a generator nor native solver:
all32 palette/quartet inputs and896 integer point occurrences are checked.
Exactly20 inputs satisfy the four-AP subsystem.

In the anchored palette b=0 the surviving ten quartet inputs have this
complete disjoint cover:

| Head | Additional fixed bits | Other regular bits free | Quartet inputs |
|---:|---|---:|---:|
| 1 | u29=0,u80=1 | 89 | 4 |
| 2 | u29=1,u80=0 | 89 | 4 |
| 3 | u29=u80=0,u28=u81=1 | 87 | 1 |
| 4 | u29=u80=1,u28=u81=0 | 87 | 1 |

If29 and80 differ, both triples are automatically mixed and28/81 stay free.
If29 and80 agree, both outside endpoints must be opposite. Thus every
counterexample belongs to one of these four exact models. In every head u6
remains free; no input symmetry quotient is used.

## Exact encodings and checked refutations

The common mechanism is credited to the
[single-satellite source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/single-satellite618/PROOF.md),
source b18c33b5f51ce2c6b9c9bdb092cbdb5871b09b78. The signed-word frontend
and pipeline extend source00dd57d6. Each model has100 regular field columns,
4950 pair variables p_xy=u(x) XOR u(y),19404 root-triangle clauses and4236
distance-three ladder groups contributing8472 clauses. The root triangles
force precisely the anchored coboundaries of arbitrary orientations, with
u0=0 as a global palette gauge. The distance-three ladder equivalence to
actual cyclic seven-AP avoidance is explained in the
[separable618 source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/separable618-exclusion/PROOF.md)
and independently reconstructed by the pinned actual cyclic checker.
The older helper's singleton literal/decoder interfaces are never used.

The mixed-central heads add10 signed units and have27886 clauses;
the equal-central heads add12 units and have27888 clauses. There are no
growth cuts, no global no-five/no-six assumption, counters, weight bounds,
pair identifications, reflection or stabilizer invariance.

Both Python modes reconstruct all381306 actual cyclic start/nonzero-step
pairs for the common base and compare all four complete CNFs. The new unit
interfaces exhaust10240 inputs, with four positive fixed words. An additional
20480 unit checks explicitly toggle u6 without changing those interfaces.
Twenty-four repaired production-model damages reject, including an extra u6
unit in every head. Small exact controls cover1808 anchored inputs at q7/11/13,
139 positive words and all128 q7 pair assignments, with two consistent fixed
words. Forty-nine repaired small-model damages and twelve ordinary
cover/premise/transport/joint-domain damages reject.

Fresh native proposals and untrusted DRAT conversion yield the following
strict positive-RUP checks. Every addition and final empty clause is checked
against the entire audited CNF in both normal and optimized Python modes.

| Head | Clauses | Native conflicts | Checked additions | Propagation hints |
|---:|---:|---:|---:|---:|
| 1 | 27886 | 43949 | 40165 | 1161711 |
| 2 | 27886 | 48607 | 44360 | 1258740 |
| 3 | 27888 | 15012 | 18266 | 485631 |
| 4 | 27888 | 13470 | 17435 | 450640 |
| Total | | 121038 | 120226 | 3356722 |

[expected.json](expected.json) freezes all model/proof hashes and source pins.
A positive RUP control passes; eight generic damaged proofs, two damaged
production traces and a changed checker pin reject. The four exact refutations
and the complete ordinary cover exclude the joint counterexample. With9457
this proves the new two-satellite assertion for either palette.

No old incomplete model was retried. In particular, the earlier unsplit
mask1 native UNKNOWN remains an incomplete native receipt; its mathematical
exclusion was supplied separately by9457. The four current heads have new
CNFs and join two other, previously unproposed profile domains.

## Affine and interval consequences

For a nonzero field multiplier a, the map x->ax+b has the unique CRT lift
t->alpha*t+beta mod618 with alpha=1 mod6,alpha=a mod103,beta=0 mod6,
beta=b mod103. Its multiplier is a unit, its phase is preserved, and it maps
nonconstant cyclic APs bijectively. Transport the holes and whole orientation;
do not impose invariance of an individual orientation.

The harmonic maps are x->88x+75 and x->15x+30, lifted respectively to
397t+384 and427t+30. The literal checker verifies all1236 CRT point identities
and each hole, seed, endpoint and two-point image. The new restrictions are
contained in the retained growth-kernel context of
[graph9253](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/thirteen-cut-kernel618/PROOF.md).
That result classifies irredundant growth cores, not every mono-five seed
location. It supplies no global seed-coverage premise here.

A wholly regular monochromatic cyclic AP has a nonconstant integer
realization in[1,2472]: reverse the difference if needed to take1<=d<=309,
choose the first residue in[1,618], and take seven integer terms. Independently
recoloring individual hole copies cannot repair this regular obstruction in
an interval coloring agreeing with the repeated regular template. The matched
mono-five and template hypotheses remain essential.

## Reproduction and literature scope

[README.md](README.md) gives the exact serial command.
[reproduce.py](reproduce.py) fetches six pinned public dependencies, compiles
an untrusted converter, reconstructs all audits/controls and makes four fresh
proposals by default. It strictly checks every candidate in both Python modes.
[VALIDATION.md](VALIDATION.md) records the completed source restart.
Large models, proof traces, environments, binaries and private state are omitted.
The ordinary bridges and imported9457 theorem are an explicit trust boundary.
Separate algorithms from one author are not an external independent review.
Newness is relative to the cited committed campaign lemmas; comprehensive
historical priority is not asserted.

A narrow live primary recheck on2026-10-02 found Table1, length7/two colors,
still reporting>3703 in
[Monroe's article](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/).
Its length-first W(7,2) is the present color-first W(2,7). The
[primary vdw repository](https://github.com/hmonroe/vdw) and
[Herwig et al. construction paper](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
were also rechecked narrowly; this is not an exhaustive latest-record survey.
A binary AP7-free coloring of[1,3704] would prove W(2,7)>=3705. The present
lemma supplies neither that coloring nor an exact value.
