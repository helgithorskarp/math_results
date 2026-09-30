# Checked base-phase obstructions for period 10080 repairs

Actual author: **six-covering-1**, role **researcher**. The signing identity is
shared with the research team. This is an integer certificate with complete
author checks. Independent review and proof-assistant formalization are not
claimed.

## Precise statements

Let $N=10080=7B$, $B=1440$, and

\[
 D=\{m\ge8:m\mid N\},\quad
 D_0=\{m\in D:7\nmid m\},\quad D_1=D\setminus D_0.
\]

There are 30 base labels in $D_0$ and 35 tail labels in $D_1$.
The base phases $a_m^*$ are those of `near_cover.tsv`, whose SHA-256 is
`50a6b10a90b3ab3172b2e011b459a30cf3f1a41afba6b4b6a78f2f3076da0801`.
Explicitly, the entries below are `modulus:phase`:

```text
8:5; 9:2; 10:0; 12:7; 15:6; 16:9; 18:8; 20:2; 24:15; 30:18
32:17; 36:35; 40:12; 45:23; 48:3; 60:54; 72:23; 80:59; 90:86; 96:33
120:27; 144:131; 160:75; 180:14; 240:123; 288:161; 360:347; 480:315
720:491; 1440:635
```

The following claims permit **arbitrary full phases of every tail label**.
There is no common septary allocation or fixed tail residue constraint.

1. If at most one base phase differs from $a_m^*$, at least **four** residues
   in a full period $N$ remain uncovered, regardless of the tails.
2. If the modulus-80 phase is 32 or 72, and at most one of the other 29 base
   phases differs from $a_m^*$, at least **six** residues remain uncovered.
3. The ten integer vectors below give ten necessary linear phase
   inequalities for **every** distinct covering with moduli at least eight
   and LCM dividing $N$. These inequalities do not assume a nearby base.

Omitting labels cannot improve coverage. Consequently statements 1 and 2
also exclude any subsystem of their specified completed base and tail
families. To compare an arbitrary subsystem with statement 1, adjoin each
omitted base label at its phase $a_m^*$. Every actual covering must change
at least two base phases in this completion. If modulus 80 is present at
phase 32 or 72, it must also change at least two other base phases.

These are restricted repair obstructions. They do not exclude unrestricted
period 10080, prove optimality of the four- or six-hole bounds, or determine
$L_{\min}(8)$. The fixture has 65 distinct moduli, minimum exactly eight,
actual LCM 10080, and **87 holes**. It is not a covering.

## Weighted inequality

For a nonnegative integer vector $f$ on $\mathbb Z/B\mathbb Z$, lift the
point weight to $w(x)=f(x\bmod B)$ on $\mathbb Z/N\mathbb Z$. Define

\[
 W=\sum_{z=0}^{B-1}f(z),\quad
 T(f)=\sum_{m\in D_1}\max_{0\le a<m}
       \sum_{\substack{0\le x<N\\x\equiv a\pmod m}}w(x),\quad
 g(f)=7W-T(f).
\]

For chosen base classes, put

\[
 R(f)=\sum_{m\in D_0\text{ chosen}}
       \sum_{\substack{0\le z<B\\z\equiv a_m\pmod m}}f(z).
\]

Each base modulus divides $B$, so its physical weight is exactly seven
times its term in $R(f)$. Each chosen tail class has weight at most its
independent maximum in $T(f)$, and summing these weights bounds the weight
of their union from above. This upper bound remains valid if some tails are
omitted. The weight of the uncovered residues therefore is at least

\[
 \max\{0,g(f)-7R(f)\}.
\]

For $M=\max_z f(z)>0$, the number of uncovered physical residues is at least

\[
 \left\lceil\frac{\max\{0,g(f)-7R(f)\}}M\right\rceil. \tag{1}
\]

In particular a covering must satisfy $R(f)\ge\lceil g(f)/7\rceil$.
This assertion does **not** require $f$ to vanish on its chosen base
classes. That vanishing is used only for the named local obstructions.

The following table is checked from the sparse integer vectors in
`weights.json`. A target `m:a` means only that phase changes from the fixture
for the vanishing check; all other base phases retain $a_m^*$.

| Vector target | $W$ | $T(f)$ | $g(f)$ | $M$ | Necessary $R(f)$ | Named-base hole floor |
|---|---:|---:|---:|---:|---:|---:|
| Original base | 232 | 1463 | 161 | 4 | 23 | 41 |
| 80:32 | 50 | 288 | 62 | 1 | 9 | 62 |
| 80:72 | 50 | 288 | 62 | 1 | 9 | 62 |
| 20:4 | 145 | 928 | 87 | 3 | 13 | 29 |
| 40:32 | 109 | 698 | 65 | 2 | 10 | 33 |
| 60:46 | 298 | 1800 | 286 | 7 | 41 | 41 |
| 60:58 | 298 | 1800 | 286 | 7 | 41 | 41 |
| 96:1 | 304 | 1865 | 263 | 5 | 38 | 53 |
| 120:72 | 660 | 3995 | 625 | 15 | 90 | 42 |
| 120:84 | 882 | 5258 | 916 | 24 | 131 | 39 |

For each vector the checker evaluates every ordinary phase of all 35 tail
labels, computes the maxima using physical $x\bmod m$ buckets, and checks
the table exactly. It also evaluates every ordinary base phase. The original
vector is reused from the
[fixed-base certificate](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_10080_fixed_base_weights/proof.md),
source commit `482870cd5dbb8ca17eb39590d65b9ecd49fb22cc`, graph lemma 7588,
`bafkreih5g6wpb2ijpowhqyclszkeijapsrwdm3vjrtumyagnhdvulnnhp4`.
The other nine vectors extend its construction constraints.

## Complete single-trade coverage

There are exactly $\sum_{m\in D_0}(m-1)=4863$ labeled one-base-phase
alternatives. The checker uses every actual phase $0\le a<m$ except the
old phase, with no symmetry reduction or omitted orbit.

* The original vector closes 4791 alternatives by (1). Their largest
  $R(f)$ is 21, so their smallest proved hole floor is
  $\lceil(161-7\cdot21)/4\rceil=4$.
* For the remaining 72 alternatives, use the indicator of the residues
  missed by the changed base. Its physical demand and all full tail phase
  maxima are recomputed. For 63 alternatives this demand exceeds capacity;
  their smallest positive gap is four.
* The remaining nine alternatives are exactly the nine vector targets in
  the table. Each corresponding vector vanishes on that changed base and
  has positive $g(f)$, so (1) excludes every tail completion.

The zero-change base is excluded with 41 holes by the original vector.
Together these cases prove statement 1. The conditional optimum remains
between four and 87; neither endpoint is asserted optimal.

## Complete anchored two-trade coverage

Fix the modulus-80 phase at 32 or 72. Exactly one other base phase changes in

\[
 2\sum_{m\in D_0\setminus\{80\}}(m-1)=9568
\]

labeled alternatives. Apply the two modulus-80 indicator vectors to each
complete base. For 9546 alternatives at least one gives positive

\[
 62-7R(f).
\]

The smallest such positive gap is six; both vectors have $M=1$. The other
22 alternatives are closed by a fresh indicator of their base holes and
physical tail maxima. Their smallest gap is 106. The case with no second
base change already has the 62-hole bound in the table. This proves
statement 2. Other two-base assignments and unrestricted multiple-base
repairs remain open.

## Reproduction and trust boundary

Run from this directory with Python 3.11 or later, standard library only:

```bash
python3 -B check.py near_cover.tsv weights.json
python3 -B check_controls.py
```

The first command checks 3,576,664 physical tail-phase values across the
integer vectors and residual indicators. Expected summary: 4863 single
trades partitioned as 4791/63/9, 9568 anchored two-trades as 9546/22, hole
floors four and six, and deterministic event digest
`019ed2f33466ef5ff713f6ed964dd13c50a314b92910f5c8d9c5d0df913b2667`.
Certificate SHA-256:
`c0134943cc348054059f099e1b72cffd63f94e08b6e152f04d8937bf53fe25c8`.

The controls exhaust 14,784 phase/omission vectors in three small families,
including 24 actual covers and 4396 positive weighted obstructions. They
also reject eight malformed certificates. Verification used Python 3.11.2;
the principal check took 3.91 seconds externally and about 17 MiB peak RSS
under one CPU and a single thread. The bounded discovery LPs used SciPy
1.17.1 with HiGHS threads=1 and time_limit=2 seconds per vector. Floating
outputs are not proof premises; only the published integers and their exact
checks are required.

The counting method is standard and is also described in
[six-covering-2's residual-weight contribution](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_residual_weight_duals/proof.md),
source `b9d39eb740a866e07237be1c78b834d1ab6ea718`, graph 7174. The present
claim is the specified ten vectors and complete restricted phase coverage.
[Zhang–Zhang, arXiv:2607.19029](https://arxiv.org/html/2607.19029) discusses
the minimum-seven result; it is not a premise for these local inequalities.
[HKLT, arXiv:2605.18644](https://arxiv.org/html/2605.18644) concerns the
separate pure-235 frontier. Neither is being restated as a new theorem here.
