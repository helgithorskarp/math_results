# A quadratic greedy completion for boxed2143

Every permutation of size m>=1 has a completion produced by the prescribed
greedy algorithm that avoids boxed2143, retains the source as a tagged
subsequence, and has length at most m^2. This is an internally checked partial
tool. The growth of the full boxed2143 avoiding class remains unresolved.

A boxed2143 is a quadruple i1<i2<i3<i4 with
p[i2]<p[i1]<p[i4]<p[i3] and no unselected point strictly inside the rectangle
between the outer horizontal positions and extreme selected values.
The algorithm processes source ranks increasingly, inserts new global maxima,
and repairs an illegal target by inserting an auxiliary maximum at the
rightmost legal earlier gap until the target becomes legal.

The [full uniform proof](author_packet/workday7_fixed_interval_v1/FIXED_INTERVAL_TRANSPORT_AND_REPEAT_CHARGES_V3.md)
retains persistent point identities and exact original-gap weights. Each
source episode labels its new auxiliaries as one birth group. Auxiliary
intervals within a group stay disjoint because later same-group birth values
provide permanent greater points to the right. The exact pre-episode minimum
labels then imply that a next episode charges at most n original points and
one auxiliary per prior group: cost<=n+G<=2n. Summing proves length<=m^2.

The proof also establishes exact mass/eligibility/birth transport, a conditional
K(K-1) mass decrease for each fixed old point, newborn mass partitions, and an
all-size family in which the same old auxiliary with K=1 is charged indefinitely.
These do not supply a useful unconditional cost estimate.

The new proof and both prescribed finite controls received an
[entire internal check by a different researcher](internal_review/QUINN_FIXED_INTERVAL_BIRTH_GROUPS_ENTIRE_REVIEW_V1.md).
The original author proof retains its earlier pending-status header; that is
historical, and this README plus publication provenance records the subsequent
whole check. This is team checking, not external peer review or a novelty claim.
The unchanged [independent checker](internal_review/check_quinn_fixed_interval_birth_groups_v1.py)
uses monotone-stack endpoints and a pointer-stack Cartesian walk; its only
executable dependency is the explicitly pinned, already checked648 helper
beside it. Both sources are published without changes.

The finite domain is ALL154 source parents of sizes0..5, ALL873 next original
choices, and ONLY seven directed parents s_n for n6..12 with ALL70 next choices
and the distinguished continuation to n13. Repeated history stages are
counted as executed traces. Each encoding has1887 insertions,1725 episodes,
8062 old-point comparisons,161 conditional controls and7 family records.
V2 adds1725 birth-group records and1887 group-state controls. The720 extensions
from size5 to size6 are included; size6 parents with all their next gaps are
not an additional census. The all-size result comes from the proof.

Run with Python3.11.2 and standard library only:

```sh
python3 -B reproduce_public.py --output-directory /tmp/boxed2143-quadratic-reproduction
```

The output directory must be new. The wrapper pins inputs, runs the TWO
unchanged author controls to regenerate the omitted full certificates, copies
only those certificates into a temporary author-input mirror, and runs the
ONE unchanged different-researcher checker. Native solver threads stay1;
each child has a60s internal/70s external guard and80point guard. Its full
outputs and logs remain in the chosen local directory. Running this wrapper
again is a new same-operator reproduction, not another independent review.

Expected complete V1 certificate:3390084B SHA256
`4cc47257eac44337e083929f5f59997cf003336d9b65c2b46184dedea5f4f684`.
Expected complete V2 certificate:3885809B SHA256
`005adc267bb228f204d2c250210e594904fd454007e57c3a7697c0d4fd35ea33`.
V1 sorts typed integer map keys; V2 normalizes JSON string map keys before
sorting. Both complete files,3780/5505 records respectively, were originally
independently regenerated and compared byte for byte. Compact original reports
and all scientific sources are included; the bulky full certificates are
omitted and locally regenerable. The original author manifest records both
omitted paths as well as the69 provided files.

Declared prerequisites are maximum-insertion blockers444, Cartesian split467,
leaf-language legality534, greedy repair592, actual original-gap law632 and
exact charge cost648/682. Their supplied scientific source and proof boundary
is in author_packet; the accepted648 helper and whole written review are also
included. PUBLICATION_PROVENANCE.json records the exact original packet and
whole review fingerprints, included subsets, omissions and subsequent actual
whole author acknowledgment. Large operational closures stay in durable
research storage and are not repository payloads.

Primary context is Kitaev, Qiu and Xu,
[Coincidences and Growth of Boxed Mesh Patterns, arXiv2609.13764v1](https://arxiv.org/html/2609.13764v1#S7).
The result here is quadratic, whereas their Proposition7.3 requires an
affine-length injection; their Conjecture7.4 specifies a fixed-odd-value
length2m-1 interleaving with a decoder. Tagged source retention does not by
itself give a decoder from the unmarked completed output. A lengthN output
can retain up to binomial(N,m) different m-point source patterns.

The outstanding sufficient route in this work is an actual-source mean cost
sum of little-o(m logm), or a suitable positive-density version, retaining all
history probabilities. Quadratic size is too large to establish it. This
release excludes the later, separately pending retirement/birth-surplus scope,
primary affine/fixed-odd-value conjectures, full growth solution, novelty,
external peer review and graph commitment.
