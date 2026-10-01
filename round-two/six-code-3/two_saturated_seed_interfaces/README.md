# Two literal saturated-star seeds cannot extend to size71

Actual author: **six-code-3, researcher**. Seed inputs supplied by
**six-code-1, researcher**, campaign message930, 2026-10-01.

**Lemma.** Let F be a family of five-subsets of {0,...,17}, with distinct
members intersecting in at most two points. Suppose F contains the36-word
seed17, respectively seed18, specified in [certificates.json](certificates.json),
and points17 and11 each have replication20 in F. Then |F|<=61,
respectively |F|<=64. Neither bound is asserted sharp.

The statement also applies after any point bijection, with the corresponding
two centers still at degree20. There is no assumed involution, restriction
on other degrees, or reliance on the unpublished two-unsaturated structural
candidate. The seed list is not asserted complete for any global profile.
Consequently this result excludes these two supplied interfaces from a
71-word completion, not every multiplicity-two interface or a whole profile.
Unrestricted campaign bounds remain69--71.

Both literal seeds have36 distinct five-sets and360 distinct triples.
Each includes exactly20 words through17 and20 through11, with four common
words; every seed word contains at least one of these centers. Since their
degrees in F remain20, any further word avoids both centers. Test every
binomial(16,5)=4368 five-subset of the other sixteen points against the
seed. The complete candidate domains have118 and121 words. Joining
two candidates when they meet in at most two points gives residual graphs
with5803 and6087 edges. A completion is a clique in the appropriate graph.

The small certificate gives a proper coloring of all vertices with25 and28
colors. A clique has at most one vertex in each color, proving36+25=61
and36+28=64. No coloring optimality or solver exclusion is claimed.

[verify.py](verify.py) imports only the Python standard library. It decodes
all actual words, verifies their complete literal triple ownership and
center degrees, reconstructs every candidate via unused triples, and checks
every actual compatible pair against the color list. It imports neither
the producer coloring routine nor an earlier star decoder. The colorings
were discovered with the [published generic DSATUR routine](../nineteen_twenty_twenty_interfaces/residual.py);
the heuristic's quality is irrelevant once its properness is checked.
No completeness statement about all seed classes is used by this lemma.

Reproduce from the repository root with Python3.11+:

```bash
python3 round-two/six-code-3/two_saturated_seed_interfaces/verify.py \
  round-two/six-code-3/two_saturated_seed_interfaces/certificates.json --controls
python3 -O round-two/six-code-3/two_saturated_seed_interfaces/verify.py \
  round-two/six-code-3/two_saturated_seed_interfaces/certificates.json --controls
```

Normal and optimized checks agree. Twelve meaningful damages per seed
are rejected. The proof uses exact finite positive coloring certificates
and ordinary residual/clique arguments. Independent peer review, formalization
and historical priority are not claimed. Compact validation, certificate
and readout hashes are in [VALIDATION.json](VALIDATION.json).

The neighboring [mixed19/19/20 proof](../nineteen_nineteen_twenty_interfaces/PROOF.md)
is a separate result and is not a premise here. Source provenance for the
input seeds is recorded in the certificate. Their broader exploration,
point maps and unpublished structural bridge remain outside this claim.
