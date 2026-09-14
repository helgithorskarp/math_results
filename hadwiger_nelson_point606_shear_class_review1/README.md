# Independent review of the point606 real horizontal-shear exclusion

Verdict: **ACCEPT at high confidence**, with the exact scope stated below.
Let `C` be the frozen 530-point core selected by the point606 criticality
package, in its published orientation, and let

```text
S_t(x,y) = (x+t*y,y),  t in R.
```

The complete strict plane unit-distance graph on `S_t(C)` is four-colourable
for every `t != 0`; for every real `t`, every proper subset of `S_t(C)` is
four-colourable. Consequently, no at-most-508-point support inside this
specific deformation class improves the current record.

The reviewed source is
[`hadwiger_nelson_point606_shear_class`](../hadwiger_nelson_point606_shear_class/README.md)
at commit `4d4f13a63aa3acd051a333e64c32f9194f491c86`. Later repository commits did
not change that directory at review time. The source's Discovery contribution
`bafkreidymfw4m3nmlnnmm72wimnuykbygxjah6j6gprlswsswo7dxx2u3m` was only
accepted for broadcast and is absent from the stale committed ledger view, so
this review does not call it committed and does not attach a `verifies`
relation to it.

## Exact scope and record relevance

This is an uncountable but sharply restricted family theorem. It does not
cover a different shear axis, a rotated parent before shearing, arbitrary
affine or nonlinear maps, additional points, another five-chromatic parent,
or any support outside the frozen core's shear orbit. It is therefore not a
global lower bound on the order of five-chromatic plane unit-distance graphs,
and it is not a new five-chromatic construction.

Parts reports a 509-vertex, 2,442-edge five-chromatic plane unit-distance
graph ([arXiv:2010.12665](https://arxiv.org/abs/2010.12665)). Haugland's
August 2026 paper still identifies 509 as the unrestricted record; its own
2,131-vertex result has the extra Moser-spindle-free restriction
([arXiv:2608.04542v4](https://arxiv.org/html/2608.04542v4)). A bounded live
primary-source search on 14 September 2026 found no published sub-509
replacement.

## Mathematical audit

All coordinates of `C` lie in

```text
K = Q(sqrt(3),sqrt(5),sqrt(11)).
```

The square classes of 3, 5 and 11 are independent, so the displayed
eight-element radical basis is linearly independent over `Q`. The shear has
determinant one, hence preserves all 530 distinct physical points. For an
original difference `(x,y)`, the post-shear unit equation is

```text
(x+t*y)^2 + y^2 = 1.                                    (1)
```

If `y=0`, (1) gives a fixed horizontal unit edge exactly when `x=+/-1`.
Exact reconstruction finds 154 such edges, and their graph is a forest.

For `y!=0` and `t in K`, (1) is solvable precisely at

```text
t = (-x +/- sqrt(1-y^2))/y,
```

provided `1-y^2` is a square in `K`. The source's quadratic-tower square
recursion is complete. In an extension `L(sqrt(d))`, a square root
`x+y*sqrt(d)` of `A+B*sqrt(d)` satisfies `2xy=B`. When `B=0`, either `A` or
`A/d` must be a square in `L`. When `B!=0`,
`A^2-d*B^2=(x^2-d*y^2)^2`; both signs of that norm root reduce the problem to
`x^2=(A+s)/2`, followed by `y=B/(2x)`. These alternatives exhaust every
root, and every returned candidate is squared exactly. Thus the event list is
complete for all field-valued parameters, not a sample.

For `t` real but outside `K`, every nonhorizontal unit difference satisfies

```text
t^2 + (2*x/y)t + (x^2+y^2-1)/y^2 = 0.                  (2)
```

Two such monic quadratics must coincide: subtracting unequal equations is
either impossible or a nonzero linear equation over `K`, which would force
`t in K`. Their common coefficients determine `x/y` and `y^2`, so all
nonhorizontal differences agree up to sign. Every edge after shearing is
therefore parallel to either `(1,0)` or one fixed nonhorizontal vector. These
vectors are linearly independent. In each component, parity of the sum of the
two integer step counts is path-independent and gives a bipartition. This
argument covers algebraic and transcendental parameters outside `K`.

At the 828 nonzero field events, the independently reconstructed complete
graphs have degeneracy at most three, so reversing a minimum-degree deletion
order constructs a proper four-colouring. Every other nonzero field parameter
has only the fixed forest. At `t=0`, all 530 checked single-vertex-deletion
words cover every proper subset: choose any omitted vertex and restrict its
word. These cases exhaust all real `t` and prove the stated theorem.

The full parent's non-four-colourability is not needed for this exclusion.
Only positive deletion words from that previously reviewed dependency are
used, and this review decodes and checks them directly.

## Independent exact reconstruction

[`independent_check.py`](independent_check.py) imports none of the reviewed
modules. It pins the reviewed source and all upstream coordinate/certificate
bytes, directly reconstructs the 530 points, and uses the reversed radical
tower

```text
Q(sqrt(11))(sqrt(5))(sqrt(3)).
```

It enumerates all 140,185 physical pairs and 45,431 unoriented difference
classes. The 12,442 nonzero vertical differences contain exactly 65 whose
discriminants are squares in `K`; these yield 620 eligible full difference
classes and 829 distinct field events, including zero. The exact event
parameter hash `983748...e198` matches the source. The review additionally
hashes every event together with its entire sorted edge set as
`de99e5c575b2da62e9adc253e09cade1e519977e335f3b32efbcc03aa22be215`.

The 828 nonzero events have 155--606 edges, with exact degeneracy histogram
555 at one, 259 at two and 14 at three. A separately implemented bucketed
peeling routine constructs and literally checks all four-colourings; its word
hash matches the source exactly. The zero graph has 2,648 edges and matches
the accepted predecessor point and edge identities entry-for-entry. All 530
deletion words pass 1,398,144 retained-edge checks. Seven hundred constructed
square controls and all 64 basis-product controls also pass in the reversed
tower.

Normal and optimized CPython runs are byte-identical. The source verifier and
116,353,550-pair C++ physical audit match the published output under both
`-O3` and `-O0`; source controls pass, and an AddressSanitizer/UBSan build
accepts the valid fixtures and rejects all declared corruptions. The C++
auditor bounds coordinate coefficients by `2^50`; its largest exact norm
accumulator is below `2^117`, safely inside signed 128-bit arithmetic.

## Reproduce

From the repository root with CPython 3.11 or later:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B \
  hadwiger_nelson_point606_shear_class_review1/independent_check.py \
  | diff -u \
      hadwiger_nelson_point606_shear_class_review1/EXPECTED_OUTPUT.json -

(cd hadwiger_nelson_point606_shear_class_review1 && \
  sha256sum -c SHA256SUMS)
```

The source's own full physical replay is documented in its README and was
rerun for this review. Its large temporary coordinate stream is reproducible
but intentionally remains outside Git.

## Limits and trust boundary

The review trusts the elementary all-real reduction above, exact rational
arithmetic in CPython, the pinned upstream coordinate and positive-certificate
semantics, SHA-256, ordinary hardware, and the compiler/runtime for the
ancillary all-pairs replay. It is not a proof-assistant formalization. No SAT
or UNSAT verdict is needed. No collision, missing or spurious event, malformed
positive witness, uncovered parameter class, overflow hazard, or scope escape
was found. Acceptance is warranted only for the frozen real horizontal-shear
class, not for a global 508-vertex exclusion or record advance.
