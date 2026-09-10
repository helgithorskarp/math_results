# Updated exact A5 residual

The source is the h4193 frontier with canonical SHA-256
`9da6cb1a32bbb5004b72bf2ac934dc05a44b5e2bf7705e7ec55498c3e7caabf9`.
The complete propagation leaves:

- 4,886 affine pencils and 125,807,232 admissible five-curve sets;
- 118,520 exact-five-compatible global pairs / allowance 3,503,032;
- 10,176 global pairs requiring at least six active curves / allowance 310,400;
- 128,696 global pairs / allowance 3,813,432 in total, unchanged.

Every retained exact-five pair has a verified extension satisfying the current
incidence and pair constraints. Compatibility is not a physical or chromatic
candidate verdict. The higher-incidence branch is not closed, and no further
active-count phase has begun.

The canonical exported interface SHA-256 is
`42132ed90f7696d9cf7c17e7b47588ca717bb71b633141e29412a1b55b55e97d`.
Its file SHA-256, including the terminal newline, is
`734286535020a4fc4ccbaac44a8a24c4b775d89854de6515c25b45353b93dc4b`.
The file is 2,774,033 bytes and is regenerated rather than committed.
It contains all 6,704 accumulated pair exclusions, the 226 newly closed pencils,
the 4,886 retained pencils, the 2,960 moved rows, and both updated mode lists.

Exact component hashes:

| component | canonical SHA-256 |
|---|---|
| new closed pencils | `a3793032c0e0e81e3f78d37fa9c9a80b88326953904318b5d132abe1ba695058` |
| retained pencil signatures | `fae4d8df642d6a607fd966e275bd4d6e99f3202125da243d33314d674a799fbe` |
| moved global pairs | `fdd6d9da4fab597b9616770536fc2d7a06cb461bdeb7fbd1681ae016fca4226c` |
| remaining exact-five pairs | `f613a8eba7bc48ac7ab0fea3a2fe62f834ac1ab952d49e428e5165368497b283` |
| remaining at-least-six pairs | `7c7843e14d998465c083f9530bbd2f5ee591257f2a8e50d006556dd2811dc075` |

The 118,520 extension witnesses are generated deterministically. Their streamed
JSON-line transcript SHA-256 is
`3fada65f250dbf5ecc93ddaece7bbce9789cbb1a0e6c601f167082316490f56c`.
The domain order is increasing `(bucket size, integer curve-ID bit mask)`, with
increasing curve IDs within each domain. Each line is `[source_pair,sorted_lift]`
using compact JSON followed by a newline. The checker obtains the same first
witnesses by literal Cartesian products.

Use REPRODUCE.md to regenerate and independently export this interface. Future
work must preserve the inherited collision, circle, low-active, incidence,
anchor, two-coordinate, reflection-pair and rotation-pair closures. HN2 owns
the full remaining architecture. HN3 is parked and was not contacted.
This pass ends at the complete propagation boundary; no record graph is found.
