# Exact rational profiles and linear triangle-packing loss

Independently reviewed and accepted at graph h5777 (high confidence). See the
[review](../tuza_rational_ray_rounding_review1/REVIEW.md) and its separate
checker. That review concerns this package, not subsequent extensions.
This package applies
Keevash's generalized partite decomposition theorem to the full fractional
triangle-packing LP. It also supplies two finite packing certificates with
explicit infinite lifting rules. It does not claim a new design-existence
theorem or settle all-order three-type Tuza.

For a fixed mixed template, each vertex class is a clique or independent set
and each pair of classes is completely joined or empty. The main results are:

- The full integrality gap `nu*(G)-nu(G)` is **O(N) along every fixed rational
  ray of class sizes**, including bounded offsets. Constants and the starting
  order can depend on the ray. This is not a uniform `O_d(N)` result over all
  choices of proportions. Linear order is necessary already for even cliques.
- For balanced class size `t`, delete edges joining equal labels in different
  classes to form `J_t`. Every fixed rational feasible triangle-type profile
  `x` is realized exactly, with `t(t-1)x_T` triangles of each type, for all
  sufficiently large `t=1 mod D`, where `D` clears the profile and capacities.
- For every ordinary graph `F`, its balanced independent blowups satisfy
  `nu(F[t])=nu*(F[t])=t^2 nu*(F)` at all sufficiently large divisible scales.
  One finite optimum packing in `F[s]` lifts explicitly to every multiple of
  `s`, and gives an all-scale error bound `2(s-1)nu*(F)t`.

The proof converts the rational profile into a finite disjoint union of
triangles and spare edges, then verifies all three levels of the imported
divisibility condition and the required common-neighborhood estimates.
See [PROOF.md](PROOF.md) for the full argument and [SOURCES.md](SOURCES.md)
for attribution, graph dependencies and novelty limits.

Two concrete consequences have no unknown starting order:

1. For the nine-vertex split seed with core `0123` and independent
   neighborhoods `012,013,03,123,23`, an exact primal/dual certificate gives
   `nu*(F)=11/2`. A literal 22-triangle packing in `F[2]` and a cyclic Latin
   construction prove `nu(F[2u])=22u^2` for **every** `u>=1`. The gap at any
   scale is at most `11t`. These independent blowups need not be split graphs.
2. For the Boolean template with eight mutually joined clique cells and
   three bit-neighborhood independent cells, a literal 88-triangle
   decomposition of `J_3` extends by Steiner triple systems to a decomposition
   of `J_t` for **every** `t=1 or 3 mod 6`. It has `44t(t-1)/3` triangles.
   For the unmodified balanced mixed graph `B_t`, the full integrality gap
   is at most `(304/3)t` for **every** `t>=1`.

The second conclusion uses Kirkman's classical Steiner triple system theorem
for universal admissible-order existence. Given the label blocks, the
substitution is explicit. The general rational-ray theorem uses Keevash's
much deeper theorem and has no practical general threshold in this package.

## Reproduce the exact audit

Use Python 3.11.2, or a compatible Python 3 with `math.lcm`. The checker and
construction functions require only the standard library. From this directory:

```bash
python3 check.py > /tmp/rational-ray-audit.json
cmp /tmp/rational-ray-audit.json AUDIT.json
python3 -O check.py > /tmp/rational-ray-optimized.json
cmp /tmp/rational-ray-optimized.json AUDIT.json
sha256sum -c SHA256SUMS
```

Expected result: `status: PASS`, with byte-identical [AUDIT.json](AUDIT.json).
[RUN.json](RUN.json) records the environment, runtime and audit hash.
[check.py](check.py) verifies:

- exact primal and dual inequalities for all triangle types of three profiles;
- actual packet edge and degree vectors, including repeated vertex types;
- all 74 mixed templates with at most three types as small compilation checks;
- fractional edge loads in nine literal diagonal-deleted hosts;
- 51,226 literal common-neighborhood counts;
- the 22-triangle certificate and six Latin lifts, through scale 30;
- the 88-triangle decomposition and label substitutions at orders 3, 7, 9,
  15 and 31, the last with 341 vertices and 13,640 triangles;
- seven deliberately invalid constructions, all rejected.

The finite checks test the stated identities and certificates. They do not
establish the universal decomposition theorem, ray argument or arbitrary-order
Steiner triple system existence; those are the mathematical trust boundary.

## Optional witness discovery

The checked data are in [CERTIFICATES.json](CERTIFICATES.json).
[packet.py](packet.py) constructs typed packets and both kinds of lifts.
[produce.py](produce.py) is an optional NumPy/SciPy producer, run originally
with SciPy 1.17.1. In an environment containing NumPy and SciPy:

```bash
python3 produce.py > /tmp/rational-ray-candidate.json
python3 check.py /tmp/rational-ray-candidate.json
```

The producer solves the profile LPs, a 150-variable integer profile model,
a 120-variable packing model for `F[2]`, and a 656-variable exact-cover model
for `J_3`. Each integer solve has a 30-second limit. It may return different
valid witnesses on another solver version, or fail to find one within the
limit. A rerun produced a candidate accepted by the independent checker.
Floating-point solver values and solver optimality reports are not proof
premises: exact rational duals certify the optima, and literal edge checks
certify the packings. No solver is needed to check the published certificates.
No large data, search logs, external certificates or private inputs are needed.
