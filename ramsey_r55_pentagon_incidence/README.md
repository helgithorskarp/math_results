# At least 906 joined-edge pentagons in every Ramsey43 graph

Every hypothetical 43-vertex graph with no clique or independent set of order
five must contain at least **906 distinct induced seven-vertex copies of
K2 + C5 or its complement**, and at least **18 induced pentagons**.
Here + is the graph join. Each occurrence is counted by its vertex set,
without an automorphism or orientation factor.

This excludes the complete global 43-vertex families with at most 905 such
seven-sets or at most 17 pentagons. No symmetry, fixed neighborhood, degree
profile, catalog or partial graph is assumed. It is a necessary structural
condition, not a 43-vertex construction or an improved Ramsey-number bound.
The numerical global bounds are not claimed optimal.

[PROOF.md](PROOF.md) gives the full reduction and precise trust boundaries.
With d(v) the red degree and q_e the number of common neighbors in the color
of a physical pair e, it proves the stronger usable constraint

    W >= 903 + 3 sum_v (d(v)-21)^2
             + 2 sum_{e:q_e<=8} (9-q_e) + N_12 + 4 N_13,
    W <= 2 sum_P (|U_R(P)|+|U_B(P)|) <= 52 P.

N_i counts all pairs with q_e=i. U_c(P) consists of vertices joined to every
member of pentagon P in color c. The degree-square sum is an odd positive
integer, giving 906. These constraints cover all 903 physical pairs and
every pentagon in the entire graph, and remain invariant under relabeling
and color reversal. They do not force a particular previously excluded core.

## Proof mechanism

The new finite lemma states that a triangle-free ten-vertex graph with no
independent five-set has at least two pentagons. Two disjoint pentagons attain
two. A previously proved elementary lemma excludes zero pentagons. If there
were only one, every outside vertex would contact at most one of its vertices.
The remaining complete finite case is small and independently certified.

| Evidence | Coverage |
|---|---:|
| One-vertex stars on a fixed pentagon | All 32 |
| Arbitrarily labeled singleton-contact words | All 7,776 |
| Sorted words, with ten outside pairs arbitrary | 252 * 1,024 = 258,048 graphs |
| Admissible graphs in that normalized domain | 1,794, each with a second pentagon |
| Independent global incidence control | All 2,048 rooted seven-vertex graphs |
| Negative controls | Nine certificate corruptions and six malformed graphs rejected |

The producer uses adjacency bitsets and recursive independent-set search.
The separate checker uses 1,024-bit truth vectors, all physical triangle and
five-set conditions, exact graph-key coverage, and literal witness checks.
It imports no producer or graph catalog. The zero-pentagon proof dependency
is explicit and pinned in dependency.json. It is replayed in full reproduction.

Hereditary deletion counting gives valid pentagon bounds 2,4,7,12 on
triangle-free graphs with alpha<=4 at orders 10,11,12,13. The elementary
order bound thirteen is proved inside PROOF.md. Summing over every pair's
common neighborhood and applying Goodman's identity yields the global lower
bound. Summing the same occurrences by pentagon bounds the multiplicity by
52. Thus the small enumeration is connected to a complete global exclusion;
it is not published as a standalone local witness.

## Reproduction

Use a full checkout of this repository so the sibling
`ramsey_r55_induced_pentagon_forcing` is present. Python 3.11+ and its standard
library suffice. Tested with CPython 3.11.2. From this directory:

```sh
python3 -B reproduce.py
python3 -B -O reproduce.py
sha256sum -c SHA256SUMS
```

Expected status: `REPRODUCED_GLOBAL_PENTAGON_INCIDENCE`.
The certificate regenerates byte for byte, the pinned preceding package
replays, and the new checker and controls run in normal and optimized modes.
Measured full runs took 19.22 and 19.21 seconds, with peak child RSS 19,864 KiB.
No solver, external library, downloaded data, omitted large artifact or
private input is required. A hash alone is not treated as a certificate.

Certificate SHA-256:

    684c0d2ad458ac759bfc496cb03b12ad68b33c65a5fb0e497b03a8ce7ffd6de8

For just the independently checked finite certificate:

```sh
python3 -B check.py certificate.json
```

This last command establishes the normalized extension statement; the
zero-pentagon lemma and the written global double counting remain explicit
premises of the full theorem.

To inspect a physical graph:

```sh
python3 -B audit.py control40.edges
```

An input has a first line `n m`, followed by m distinct red pairs `u v`,
with `0 <= u < v < n`; omitted pairs are blue. The audit accepts orders 1--63.
It counts the two global incidences independently, checks the triangle
identities, and checks the conditional bounds only after verifying that
the input has no monochromatic five-set.

The included control is copied byte for byte from team-r55-1's
[maximum40.edges](../ramsey_r55_cyclic_minimum_puncture/maximum40.edges),
verified source commit 55487717629070142ea39226e3d449f698bd9c1a. It has 397 red
edges, 12,477 pentagons and 7,670 counted seven-sets. Its complement and a
scrambled labeling give the same invariant quantities. It is a pre-existing
smaller graph used as a control, not a new construction or proof premise.
Its counts also illustrate that the proved universal bounds can be loose.

## Sources and relation to shared work

The sole imported mathematical campaign lemma is the ten-vertex
triangle/C5-free result in
[the preceding pentagon-forcing proof](../ramsey_r55_induced_pentagon_forcing/PROOF.md),
Discovery Net h3593, artifact
`bafkreiffqyzfkpxkeaujbuacmzhduxnxs2pj2phancs3vm4q3yo5gdzu5e`,
source commit 514d32b01e495ee9df818e19bf2e0ae58ba52084.

The classical triangle identity is due to A. W. Goodman,
[On Sets of Acquaintances and Strangers at any Party](https://doi.org/10.1080/00029890.1959.11989408),
American Mathematical Monthly 66 (1959), 778--783. We prove the identity
directly here. The graph-growth and counting methods are standard; no
historical priority for them or for the finite cycle minimum is claimed.

During discovery, counts from
[McKay's Ramsey graph data](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
suggested the two-pentagon lemma. None of those files, their completeness,
or their higher-order cycle minima enters this proof. The certificate is
generated from the complete physical singleton-contact domain.

Current problem context was checked against Angeltveit--McKay,
[R(5,5) at most 46](https://doi.org/10.1002/jgt.70029).
Limited targeted live searches and new shared contributions supplied no
matching global incidence bound; this does not establish novelty or priority.

The h3595 Cyclic(43) puncture spectrum supplies the control graph only.
The h3599 M214 moment separator and h3597 local interface review have distinct
domains and are not proof inputs. This work does not rerun the old order-22
SAT instance, reopen H92/H93 gluing, or absorb the teammate's construction
lane. Those artifacts and intervening repository commits are preserved.

The new result is computer-assisted and unformalized, with author checks.
External peer review is pending. It does not decide global degree slices,
produce a target, improve the team's defect minimum, or improve an
unrestricted Ramsey-number bound.
