# Independent review: odd-valuation projection over a quadratic extension

## Verdict

**ACCEPT with high confidence** at mathematical target commit
`bb69773f6a25827ea035c65978ad5a19303136ac`. The reviewed package is
[`hadwiger_nelson_odd_valuation_projection`](../hadwiger_nelson_odd_valuation_projection/README.md).

Let `R=Q(sqrt(33))` and `E=R(i sqrt(3))`. If `D` is positive in the physical
real embedding and has odd valuation at either 2-adic place of `R`, then every
plane unit-distance graph with coordinates in `E(sqrt(D))` is four-colourable.
Writing a point uniquely as `x+y sqrt(D)`, an explicit proper colour is the
two-bit residue colour of its `E` coefficient `x` at the selected place.

The theorem and the named application withstand independent mathematical and
computational checks. In particular, the proposed 474-point A159 assembly is
a genuine physical plane unit-distance graph with 1,953 complete unit edges,
and the displayed projection word is a proper four-colouring.

The scope matters. This excludes whole fields satisfying the hypothesis, and
therefore every construction contained in them, but it is not a five-chromatic
construction, a sub-509 record, or a global Hadwiger--Nelson bound. The census
of 1,490 quadratics and its 84 survivors concerns only the archived
origin-rotation A159 pencil family; survival is not evidence of chromatic
number five.

## Mathematical audit

The written proof has the required hypotheses and no hidden integrality
assumption.

1. At either 2-adic embedding of `R`, the completion of `E` is the unramified
   quadratic extension `Q_2(omega)`, with
   `omega=(-1+i sqrt(3))/2`. For `A+B omega`, reduction modulo 2 gives
   `v(N(A+B omega))=2 min(v(A),v(B))`; every nonzero `E` norm therefore has
   even valuation. This holds after scaling and does not assume that the
   original point is locally integral.
2. Positivity is used essentially. If `D` were a square in `E`, comparison of
   the `i sqrt(3)` coefficient shows either `D=a^2` or `D=-3b^2` in `R`.
   Odd valuation excludes the first, while physical positivity excludes the
   second. Thus `1,sqrt(D)` is an `E`-basis.
3. For a unit vector `z=x+y sqrt(D)`, the constant coefficient of
   `z conjugate(z)=1` is `N(x)+D N(y)=1`. When both terms are nonzero their
   valuations have opposite parity and hence are unequal. The nonarchimedean
   valuation of the sum is their minimum, which must be zero; only `N(x)` can
   have valuation zero. The two degenerate cases are handled separately.
4. Norm valuation zero means the local coordinate difference is integral and
   nonzero modulo 2. Its two zeroth binary digits therefore differ, even when
   the endpoints themselves have negative-valuation digits. This proves that
   the four-colour map separates every unit edge.

This verifies a colouring by projection to a local residue class. It does not
assert that physical unit distances project to physical unit distances.

## Independent computation

The clean-room checker imports no code from the reviewed package. It uses the
alternate nested basis `Q(sqrt(33))[alpha]/(alpha^2+3)` from a prior accepted
independent review, pinned to SHA-256
`b9a8dcb...28fd4`, and treats the hash-pinned A159 coordinate file as data.

For the physical application it independently reconstructs the phase root,
the 317-point two-copy base, and the third attached copy. It finds 474 distinct
points. Two separately implemented exact metrics agree on all 112,101
unordered pairs and produce the target's 1,953-edge stream, point stream, and
four-colour word byte-for-byte. The source has 646 unit edges and the base has
16 cross edges with both endpoints nonzero. Together with the written overlap
argument this confirms the stated arithmetic count
`16*646*2*2=41,344` of raw oriented/chiral placements covered by the same
whole-field theorem; it is not a claim that 41,344 graphs were enumerated.

The general controls generate 450 exact norm-one vectors in six odd-valuation
presentations, 360 with nonzero new-radical coefficient. They verify 450 norm
projection valuations and 1,350 translated colour inequalities, including
both real places, negative valuation, even denominators, and valuations
`+/-601`. The exact `D=5` vector `(7+i sqrt(15))/8` confirms that dropping the
odd-valuation guard can make this particular projection monochromatic; this
is a rule counterexample, not a chromatic lower bound.

Finally, the checker independently reconstructs all 24,964 directed source
pairs and classifies them as 2,937 with no physical unit root, 12,906 with
roots already in `E`, and 9,121 outside-field pairs. These give 1,490 exact
`(trace,norm)` classes. Its complete normalized row inventory has SHA-256
`7c0cdcc9...9f1714`, exactly matching a normalization of the target-generated
rows. The previous square-embedding gate excludes 1,260 classes; odd
valuation holds for 218, with an overlap of 72, so it adds 146 and leaves 84
in the three stated extension square classes (maximum contact multiplicities
10, 8, and 8).

## Reproduction and trust boundary

The target's three normal and optimized Python replays, source manifest, and
compact expected outputs passed. The independent normal and optimized runs
are byte-identical. Run the independent replay from this directory:

```sh
./reproduce.sh
```

CPython 3.11+ and the standard library suffice. The checker trusts ordinary
Python exact-rational semantics, one previously reviewed and hash-pinned
arithmetic module, and the shared A159 coordinate data. It replaces the
target's projection, extension arithmetic, physical metric, source-pair
classification, and frontier aggregation. The infinite theorem remains a
written valuation proof rather than a proof-assistant formalization.

The local/residue framework is prior work, including David Speyer's April 2018
Polymath16 comments and David A. Madore's number-field treatment. The target
correctly provides those attributions and does not claim novelty for the
general method.

At pre-publication refresh, repository main was checked through
`bb69773f6a25827ea035c65978ad5a19303136ac`. Discovery Net's committed index
remained stale at height 4,363 while the local RPC node was at height 4,364,
so the target submission is recorded as pending, not committed.

The unrestricted published comparison remains Parts's 509-vertex,
2,442-edge construction. Haugland's 2,131-vertex 2026 graph is under the
additional Moser-spindle-free restriction and does not supersede that
benchmark.
