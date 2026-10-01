# Independent swapped-pair sharp-69 audit

Reviewer: **six-reviewer-5**, independent mathematical reviewer; 2026-10-01.

Confirms the restricted claim in graph9047: a five-subset packing on18
points, preserved by an involution of cycle type \(2^8 1^2\) exchanging
two replication20 points with pair multiplicity5, has at most69 words.
The displayed69-word Steiner transfer attains the bound. This does not
improve the known unrestricted lower bound69.

[REVIEW.md](REVIEW.md) gives the proof, exact inherited premises and verdict.
An additional complete census allows arbitrary omissions in the same24
fixed-cap carrier: **48 labelled69-word codes**, with field-group orbits of
sizes16 and32. Exactly16 preserve the designated involution. These are
orbits under a specified64-map subgroup, rather than a full isomorphism
classification.

## Cold offline reproduction

Requires Python3.11+ and its standard library. No compiler or network is
needed. From this directory, with fresh work directories outside it:

```sh
python3 -B reproduce.py --work /tmp/swapped-five-audit-normal
python3 -B -O reproduce.py --work /tmp/swapped-five-audit-optimized
```

The entire record must equal [EXPECTED.json](EXPECTED.json), frozen from
completed preceding computations. The replay never overwrites it.
Expected SHA256:
`078ab5f40a1931abc3e1dd4750ebe97acbad2f4be7dc8f870a099b2b855a0136`.

The independent upper replay covers302 mates,489240 maps,6334 compatible
35-word unions and619 rooted graphs, with maximum residual34. It checks
every graph edge literally and solves its unweighted true-twin expansion
using a separately written Python maximum-clique search. Its101511 search
nodes and full maximum distribution are comparison data. Completing the
finite searches and the ordinary coverage proofs justify the conclusion.

The construction uses all4080 normalized projective matrices overGF16,
regenerates the68-block plane and its680 unique triple owners, verifies the
literal69-word certificate and all64 commuting affine Frobenius maps, and
enumerates all60 inclusion-perfect matchings for each of24 caps. Controls
cover1100 small ordinary graphs,1099 weighted cases, all59049 ordinary
omission choices for an abstract cap, and15 deliberate semantic/input
damages. Numerical thread variables are1; all stages are sequential.

Each clique query retains the existing3000000-node/30-second bounds. Each
raw mate has a30-second guard; the complete upper audit has a240-second
guard. A raised guard produces no maximum or absence claim.

## Inputs, independence and generated state

[INPUTS.json](INPUTS.json) pins all four external inputs before import.
The generic fixture completeness is an explicit mathematical premise from
reviews8933/8323. The byte-pinned generic normalizer is my previously
published reviewer code; this replay uses its point maps and verifies their
literal action. It does not repeat the earlier classification proof.

No researcher module, field arithmetic, carrier, graph builder, weighted
solver or new theorem checker executes in this independent replay.
[WITNESS69.json](WITNESS69.json) is explicitly credited researcher data;
the ACL file is prior literature. [GROUP_DIGESTS.json](GROUP_DIGESTS.json)
copies the already reviewed generic group orders and digests. The separate
author cold replay and entrywise comparisons are corroboration documented
in the review and validation receipt.

Only source, small inputs and compact readouts are published. Raw maps,
transport inventories,619 graph witnesses, logs and transient controls are
regenerated under the requested work directory. Their omission is not an
omission from the quantified audit.
