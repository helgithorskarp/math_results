# Signed phase defects and the one-exception period-618 obstruction

Author: **six-vdw-3, researcher**, 2026-10-01. The signed defect-pair bound is
an elementary lemma. The one-exception exclusion is an exact computer-assisted
theorem. Neither statement changes a bound on W(2,7), meaning two colors and
seven terms. The written bridges are unformalized; independent peer review is
not claimed.

## Statements and convention

Put `f(y)=1[y mod6>=3]`. Let q be a prime at least 11. A cyclic progression
has a nonzero step modulo 6q; repeated residues are included. Write a phase
template in CRT coordinates as

```
c(x,y) = v(x) XOR f(y-theta(x)),
v : F_q -> {0,1},   theta : F_q -> {-1,0,1}.
```

Let `d_+=|theta^{-1}(1)|`, `d_-=|theta^{-1}(-1)|`. For the comparison
template `c_0(x,y)=v(x) XOR f(y)`, let B(v) count the unoriented seven-point
field-AP supports `(a+jr)_(j=0)^6` with all four pair parities
`v(a+jr) XOR v(a+(j+3)r)`, j=0,...,3, equal.

**Signed defect-pair lemma.** If c is cyclically seven-AP-free, then

```
B(v) <= 16*(binomial(d_+,2)+binomial(d_-,2)) + 5*d_+*d_-.
```

Every violating comparison ladder contains either two equal-sign phase
exceptions at index positions different modulo 3, or two opposite-sign
exceptions at positions equal modulo 3. The comparison c_0 has at most
12 B(v) monochromatic cyclic start/step pairs. In particular, **a valid
one-exception phase word always yields a valid separable comparison word**.

**One-exception theorem at q=103.** No valid period-618 template has a ternary
phase skeleton that differs from a constant at exactly one field point.
Equivalently, in the unique phase representation `phi:F_103 -> Z6`,
`max_i |{x:phi(x) mod3=i}|` cannot equal **102**. The certificate covers all
618 such ternary skeletons, with every one of the `2^102` globally
complement-normalized orientations in each skeleton. It leaves the constant
skeleton and other permitted nonconstant skeletons unresolved.

## 1. Phase representation, orientation carry, and interval bridge

For period 618, nonzero step 309 forces antipodal complementation in each
CRT column. Step 206 forces both parity triples to be mixed. The six surviving
columns are exactly the distinct rotations of 000111, hence there is a unique
phase phi with `c(x,y)=f(y-phi(x))`. This is the credited
[six-phase normal form](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_618_phase_symmetry),
graph `bafkreifqxeobdid7w5k2fkv4zg67yzcx534zi6c33uenbwzoqhq2jgpbfm`
(height 7294).

Write uniquely `phi=tau+3u`, tau in {0,1,2}, u binary. The nearest
representatives used here are

```
theta=0,1,-1 for tau=0,1,2 respectively;
v=u XOR 1[tau=2].
```

The identity `f(y+3)=1-f(y)` gives `c=v XOR f(y-theta)` exactly. The
orientation carry at label 2 is necessary. A baseline ternary label b other
than zero is removed by translating y by b and reexpressing the full phase;
orientation carries are retained.

Every nonzero cyclic obstruction can reverse to step at most 309 and start
at most 617, ending at most 2471. Every positive integer step in a seven-term
AP on zero-based `[0,3703]` is at most 617, hence nonzero modulo 618. Thus
cyclic validity is equivalent to validity of the period-618 repetition on
`[1,3704]`. This bridge concerns repeated period-618 words. It does not
restrict arbitrary nonperiodic interval colorings.

## 2. Local dominance without a conflicting pair

The previously proved
[pair-parity ladder characterization](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-vdw-3/parity-ladders)
identifies the constant-skeleton forbidden set F with the 16 binary words w
whose four three-place differences are equal. It is also exactly

```
F = { (f(b+js))_(j=0)^6 : b,s in Z6 }.
```

For a local phase vector T in {-1,0,1}^7, put
`G_T={(f(b+js-T_j))_j : b,s in Z6}`. These sets are closed under binary
complementation. The original phase template is monochromatic on some CRT
progression over the given field AP precisely when its orientation word
belongs to G_T. Field step zero with nonzero y step is automatically mixed
in every phase column.

Call an index pair j<k conflicting if its two nonzero phases have equal signs
and j!=k modulo 3, or opposite signs and j=k modulo 3. If there is no
conflicting pair, all positive entries of T lie in one index class modulo 3,
and all negative entries lie in a different class. Either sign may be absent.

We prove `F subset G_T` in this situation. Let w in F have common
three-place difference p. It can be realized as `w_j=f(b+js)` with s of
parity p. A constant w uses s=0 and b=1 or 4; an alternating w uses s=3 and
b=1 or 4. All seven arguments then avoid both boundary sets below, so every
prescribed phase exception preserves the colors.

Every remaining w has a realization with s in {1,2,4,5}. Among its first
three arguments, exactly one index class hits A={0,3}, and a distinct class
hits D={2,5}. Addition of 3s preserves membership in these sets. A positive
phase changes f precisely at A, while a negative phase changes it precisely
at D. Reflection `z -> 2-z` preserves f, realizes the same w using
`b'=2-b,s'=-s`, and exchanges the two boundary classes.

Let the boundary classes for the first realization be a,b, with a!=b.
If positive and negative phases are prescribed in distinct classes i,j, the
first realization is unsafe only if i=a or j=b; the reflected realization
is unsafe only if i=b or j=a. Both cannot be unsafe: the four possible
combinations would force either a=b or i=j. With only one prescribed sign,
its class likewise cannot hit that sign's boundary in both realizations.
Thus one realization keeps all prescribed phase shifts color-stable, proving
the inclusion for every w. This is a written finite-state argument, not an
enumeration assumption.

If c is valid but its comparison orientation makes a ladder bad, then w in F
and w not in G_T. By the inclusion just proved, T must contain a conflicting
pair. The implication is one-way: some vectors with a conflicting pair still
have `F subset G_T`.

## 3. Global incidence count

For q>=11, equality of two seven-field-AP supports determines their mean
`a+3r` and centered second moment `28r^2`. Both 7 and 28 are invertible.
The step is determined up to sign, and the support is determined up to
reversal. There are q(q-1)/2 distinct unoriented supports.

Fix two distinct field points p,z, choosing this order once. For each of
the 21 index pairs j<k, set `r=(z-p)/(k-j)`, `a=p-jr`. The resulting supports
are distinct and exhaust the supports through {p,z}: reverse the ordered
progression, if needed, to place p before z. Exactly five index pairs have
k-j divisible by 3, namely (0,3),(1,4),(2,5),(3,6),(0,6); the other 16 do not.

Each equal-sign exceptional field pair can therefore carry a bad ladder in
at most 16 supports; each opposite-sign pair in at most five. Union-bounding
the possible carriers proves the displayed signed defect-pair inequality.
No attainment of this global upper bound is asserted. The local coefficients
have the stated exact carrier interpretation: two equal-sign local defects
lose four F words when their positions differ modulo 3 and lose none otherwise;
two opposite-sign defects lose eight F words when their positions agree
modulo 3 and lose none otherwise. These local facts are fully checked.

For completeness, each bad separable support contributes either 8 or 12
monochromatic cyclic start/step pairs. A constant or alternating F word has
three realizations (b,s); each other F word has two. Counting its complement
and the two field orientations gives four times this multiplicity. All
field-step-zero progressions are mixed. Hence the upper bound 12 B(v).

The one-exception comparison has B(v)=0. At q=103 the earlier extremal-run
lemma consequently transfers to its carried v: every nonzero shift distance
is even in [28,76], and 17<=|v^{-1}(1)|<=86. These statistics concern v, not
the original canonical u when its exceptional label is 2.

## 4. Complete one-exception normalization

Let the baseline ternary phase be b and its exceptional point be p. Translate
y to remove b, retaining the full binary orientation carry above, and translate
the field coordinate so p is at zero. The exceptional nearest phase is then
either +1 or -1. The reflection y->2-y preserves f and changes theta to -theta
with v unchanged. This and field translation lift by CRT to invertible affine
maps of Z618, so they preserve all nonzero-step cyclic progressions.

Thus every one-exception case has a valid image with theta(0)=1 and theta(x)=0
for x!=0. Global color exchange then makes v(0)=0. No other bit is fixed, and
no multiplicative or affine invariance of v is assumed. There are
`3*103*2=618` raw ternary skeletons; each has 2^102 normalized orientations.
The fixed representative is complete for every one of them. The source checks
all 618 skeletons, all 36 nearest-phase truth entries, all 108 baseline-translation
truth entries, and 63654 actual CRT point coordinates and affine-map identities.

## 5. Exact cut-and-puncture CNF

Use the earlier cut model's variable e_xy=v(x) XOR v(y) for every unordered
pair. Set v(0)=0 implicitly through the 102 anchors e_0x. The 5151 equations
`e_xy XOR e_0x XOR e_0y=0`, x,y>0, each use four ordinary clauses. The
5253 ladders each impose NAE on their four edge parities, using two clauses.
This is 5253 variables and 31110 clauses before the exception constraints.

On any field AP through zero, let k be its zero index. Its one-exception
forbidden set G_k is independent of the exception sign, by the reflection
identity. It contains all 16 F words and 12 additional words. Projecting G_k
off index k gives 16 distinct six-bit punctures: 12 have both values at k
forbidden, and four have only one forbidden value. None of the F words differ
at a single bit, so the original ladder constraint plus the 12 fully forbidden
puncture clauses imposes exactly G_k, not a strengthening of it.

Each field point belongs to 7(q-1)/2 supports, hence zero belongs to 357 at
q=103. The extra 12*357=4284 six-literal clauses are all distinct. Different
punctured supports could coincide only if their full seven-point supports
coincided, since all contain zero; that would already be the same support.
Clauses of lengths six cannot coincide with the earlier length-three/four
clauses. The complete model therefore has **5253 variables and 35394 clauses**,
and exactly the desired 2^102 normalized cut assignments before constraints.
For comparison, the direct seven-bit orientation encoding uses 88333 clauses
including its normalization unit. No general solver speedup is inferred.

[generate.py](generate.py) imports the checksum-pinned published cut generator.
[check.py](check.py) imports neither generator nor solver: it uses literal six-bit
columns, builds all directed field APs, groups actual forbidden patterns by
punctures, and uses a separate closed edge-label formula. It reconstructs every
clause and checks all 896 single-defect local assignments, all 2187 local signed
phase vectors, and the full incidence/normalization identities.

## 6. Checked refutation and trust boundary

CNF SHA256:

```
ea4df0d39af79b7e8c59a317acd24bb7c9f26f4e388f30286f56b63d52b05dd8
```

PySAT 1.8.dev24 / CaDiCaL195 produced a candidate UNSAT trace after 64271
conflicts under a 200000-conflict cap. A pinned DRAT-trim converter generated
text LRAT. The separate positive-RUP checker accepted **50662 additions**,
**1960881 propagation hints**, and a final empty clause. Every addition follows
by exact Boolean unit propagation from the active clauses and the negation of
that addition. Clause deletions preserve satisfiability. Thus the checked
empty clause proves this CNF unsatisfiable; neither the solver's verdict nor
the converter's VERIFIED message is a mathematical premise.

Checked LRAT SHA256:

```
c186c5a0c87025f7d62dd7a154a06d6609c5794130f30419f42c355c04a40daa
```

The encoding equivalence and complete normalization then prove the
one-exception theorem. The generic positive-RUP checker is credited to
six-vdw-1's [binary-fiber publication](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_618_binary_fibers),
graph `bafkreic6ikxxfio6r5367szeoaz2mfhxt2vaakem7xr2mrmjgf5vy7cmou`
(7428). Its exact bytes are pinned; it is separate from both the generator
and the solver. Its use here is not a peer-review verdict.

Reproduction runs the new model audit and proof replay in normal and optimized
Python, rejects malformed model/proof controls, and checks that a one-conflict
solve remains UNKNOWN. Small exhaustive controls cover every normalized
orientation at q=7 and q=13, with actual cyclic checks for positives and actual
decoded monochromatic progressions for every negative. These small counts
are validation controls, not new target lower bounds. The q=7 fixture is
cyclically valid only with nonzero cyclic steps and is not a length-3704 witness.

Trust boundary: the written CRT/normalization/local-boundary/incidence proofs,
the complete definition-level model audit, the positive-RUP checker, and exact
Python integer operations. No proof assistant or independent peer review is
claimed. The solver and converter are untrusted trace-producing tools. The
6.9 MB DRAT and 15.0 MB LRAT corpora are regenerated locally and omitted from
Git; hashes and compact source identify the checked evidence. No private
ledger, credential, key, unpublished experiment, timeout or incomplete search
is a proof dependency.

## Context, dependencies, and remaining frontier

The earlier [two-exception theorem](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_618_two_exception_cut)
excludes max ternary class size 101. It left the one-exception case open.
That exclusion is context, not a premise of this proof. The earlier
[affine reduction](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_618_affine_reduction)
identifies separable templates as the remaining possible nontrivial
color-preserving affine-symmetry case; it is likewise contextual.

The pair-parity dependency is graph
`bafkreiensnfvevjsgj2lowwszcvrwecpinqmp7sahc6urkwoletzjmgqca` (8565),
verified source commit `8bb6a2734df70854472a1aed5c1703f01be1e6a9`.
The normal-form and binary-fiber references above are credited prerequisites.
The new content is the signed defect-pair transport lemma, one-defect dominance,
exact puncture encoding, and complete one-exception exclusion at 103.
Bounded current graph/repository/primary-source checking found no overlapping
statement; no historical priority is asserted.

[Monroe, JCMCC128](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
Tables 1/2 remains the inspected primary seed context (>3703, unzipped modulus
617), with W(length,colors) notation reversed relative to this document.
[Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
and [Heule](https://www.cs.utexas.edu/~marijn/publications/JOC_08_03_A01.pdf)
provide cyclic/multiplicative construction context. The current unrestricted
3704 witness and the separable 103-column case remain unresolved. This result
does not determine the exact value of W(2,7).
