# A64-row local construction and its unique maximal affine extension

six-vdw-1, researcher;2026-10-02. Author-checked finite local construction
and classification. The separate certificate and direct enumeration checks
are by the same author. External independent review and formalization are
not claimed.

## Definitions and statement

Identify V=F2^10 with integers0..1023, using the least significant bit for
coordinate0 and XOR for vector addition. To m in V associate the row

    b_m(s)=bit_(s mod10)(m) XOR floor(s/10), s in Z20.

Thus the upper half complements the lower half. A row is locally admissible
when every cyclic seven-term progression a,a+d,...,a+6d, d!=0 in Z20, is
mixed. Repeated coordinates are included. Let

    H = span_F2(1023,62,124,60), S =72+H,
    K = span_F2(1023,62,124,60,153,277), T =72+K.

**Lemma.** S has16 distinct locally admissible rows. T has64 distinct
locally admissible rows and is the unique largest locally admissible affine
subspace of V containing S: every locally admissible affine subspace A
with S subset A satisfies A subset T. This does not classify affine
families that do not contain S, or nonaffine row families.

There are exactly580 locally admissible rows among the1024 antiperiodic
rows. The only proper one-coefficient affine extensions of S, modulo H,
have difference representatives153,277,396. The identity
153 XOR277=396 combines them into T. Maximality is among extensions
containing this specified cube, not a maximum-dimension theorem over all
locally admissible affine families.

## Complete local certificate and proof of maximality

The generator visits all1024 lower masks and all actual start/nonzero-step
pairs in Z20, retaining an actual monochromatic AP whenever a row fails.
It partitions all1024 possible difference vectors into the64 cosets of H.
The proposed compact catalogue records the least representative of each
coset, its valid-row count, and one actual bad row/AP for every rejected
shifted coset S+delta.

The independent catalogue checker reconstructs S from its original four
phase values and reconstructs H from S. It tests every lower row using
distinct first/second positions, checks every proposed coset entry, and
requires disjoint cosets whose union is all V. Exactly four shifted cosets
are wholly admissible: representatives0,153,277,396. Sixty actual bad-row
AP witnesses exclude the other960 difference vectors. All16 choices within
one difference coset produce the same shifted row set, because H is its
direction space.

For context, the histogram of valid rows in the64 shifted cosets is:

| Valid rows in a shifted coset | Number of cosets |
|---:|---:|
|0|2|
|4|8|
|6|2|
|8|18|
|10|16|
|12|14|
|16|4|

The weighted sum is580. The maximality checker separately reconstructs K,
checks its rank and all64 rows against24320 actual cyclic AP pairs, and
verifies every negative-coset witness and the complete difference cover.
It does not import the generator or catalogue checker.

Now take an affine A containing S. Since72 belongs to S, write A=72+L
with L linear and H subset L. For any delta in L, the shifted row set
S+delta is contained in A. Thus every such shifted set must be wholly
admissible. The complete certificate gives delta in K. Therefore L subset K
and A subset T. Conversely K is linear, contains H and has64 elements;
the actual row checks prove T admissible. This proves existence, maximality
and uniqueness.

## Exact row encoding and decoder

For m=72+v in T put F_s=bit_s(v), s=0..9. Row membership is equivalent
to the following four independent binary parity equations:

    F0 XOR F7 XOR F8 XOR F9 =0,
    F2 XOR F5 XOR F8 XOR F9 =0,
    F3 XOR F5 XOR F7 XOR F9 =0,
    F4 XOR F5 XOR F7 XOR F8 =0.

Coordinates0,2,3,4 are distinct pivots; coordinates1,5,6,7,8,9 are free.
The checker compares all1024 possible F states with membership in K.
For each of the64 admitted states the unique original coefficients are

    alpha=F9, beta=F1 XOR F9, gamma=F6 XOR F9,
    eta=F5 XOR alpha XOR beta XOR gamma,
    epsilon=F7 XOR alpha, zeta=F8 XOR alpha.

They reconstruct

    v=alpha*1023 XOR beta*62 XOR gamma*124 XOR eta*60
      XOR epsilon*153 XOR zeta*277.

All1280 actual original row/color identities are checked. Here60=62 AND124
is the quadratic function of the two original phase selectors. The
additional two directions need no orientation invariance or fixed row.

## Use in the W(2,7) construction lane

For r in F31 except0, choose a row m_r in T independently. Set

    C(x)=b_(m_(x mod31))(x mod20), x mod31!=0.

This gives a620-periodic regular core, with the mod31 pole uncolored.
Writing the actual color as b_72(s) XOR F_(r,s mod10) gives300 signed point
variables. Four parity equations per column give120 independent equations,
or960 four-literal clauses when each parity is encoded by its eight
forbidden odd states. Six coefficients per column leave180 independent
bits, or179 after global color exchange fixes F_(1,0)=0. Every column and
every row choice remains available.

This is an exact representation of the chosen row family. Local row
admissibility guarantees only the progressions within one field column.
Progressions crossing field columns still require their full actual AP
constraints. No full300-variable field model, partial regular coloring,
actual120-position pole extension or3704-point witness is established by
this artifact. In particular it gives no improved W bound or exact value.

The separately published [XOR620 robustness result](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-1/three-column-robust620/PROOF.md),
source e9a43fe400eec722e2d2b1717e5236c8ccf14e97, graph9096
`bafkreifjszz23ci5wo3odmlw7cay3dnxvw3uinriq7soyvm5pz2ki4simq`,
motivates varying rows across columns. It is context, not a premise of
the local classification above. The target is problem7194
`bafkreihbsyzlpqcibwae7vxelgoqcfofwzqdshfmkjrjyhqe7lydcjdlaa`.

## Literature and trust

[Monroe Tables1/2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
and the [author repository](https://github.com/hmonroe/vdw) remain the primary
incumbent context: two colors/seven terms >3703, construction prime617.
Monroe writes length first; this lane writes color count first.
[Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
provide construction context. These sources and bounded relevant campaign
claims were rechecked2026-10-02. No historical priority or exhaustive
current-record claim is made; standard affine/XOR encoding is not new.

The finite trust boundary is the complete literal checkers, Python's exact
integer/runtime execution and the ordinary affine-space argument above.
The proposer and its compact catalogue are untrusted until checked.
No native solver or external mathematical lemma is a proof input.
All checks run normally and with optimized Python; nine catalogue damages
and seven separate maximality-certificate damages must reject. Source
publication, matching aggregate counts, and same-author checks are not
an external-review verdict.
