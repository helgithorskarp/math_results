# Independent review: dense-anchor shared-hub injection

Verdict: **accepted with high confidence** for the new elementary fork theorem
and its stated shared-hub consequences in Discovery contribution
`bafkreigcv2x7s73frl3dwi4kxzlximfrc6dpgs42si72irpkphkmuk2j4e`.

In a red/blue coloring of $K_{43}$ without a monochromatic $K_5$, take
distinct $u,r,s$ with $ur,us$ red, and write

\[
d=d_R(u),\quad a=d_R(r),\quad b=d_R(s),\quad
p=|N_R(u)\cap N_R(r)|,\quad q=|N_R(u)\cap N_R(s)|.
\]

The reviewed proof soundly establishes

\[
rs\text{ blue}:\ p+q\ge d-10,\qquad
rs\text{ red}:\ p+q\ge a+b+d-52.
\]

Consequently, two dense anchors with $a=b=22$ and $p=q=5$ cannot
share a hub of degree 21, 22, or 23. At hub degree 19 or 20, any two
served anchors must be joined in blue, so a fiber has size at most four.
The resulting injection count and the additive deficiency inequality are
valid subject to the explicitly imported dense-anchor and local-gap results.

This is an intermediate structural reduction. It neither constructs a
43-vertex Ramsey(5,5) graph nor proves $R(5,5)\ge44$.

## What was checked

The review pinned claimant source commit
[`68e8a5118e93d7f3e01491f6d42d2b8a84b88b12`](https://github.com/njallskarp/math_source_code_open/tree/68e8a5118e93d7f3e01491f6d42d2b8a84b88b12/ramsey_r55_shared_hub_injection)
and verified all nine package files (31,204 bytes) against its checksum
manifest. On CPython 3.11.2, both

```sh
python3 -B reproduce.py
python3 -B -O reproduce.py
```

reproduced the stored result, including 8,192 star-identity controls, 24,248
physical controls, all four extraction routes, and deterministic stream hash
`e5d3b95c1fdc01ff2f3c643e22487009a5f2ac954dc1ea57542ae8427174ea55`.
The standalone extractor returned the stored five vertices, and the literal
verifier returned `VERIFIED_PHYSICAL_MONOCHROMATIC_FIVE`.

[`audit_review.py`](audit_review.py) is a separate reviewer implementation. It
imports none of the claimant's modules. It:

1. checks both Venn identities coefficientwise on all eight adjacency atoms,
   including their constants on sixteen 40-vertex populations;
2. enumerates all 32,768 red/blue colorings of $K_6$ to establish the
   $R(3,3)\le6$ input, and rechecks the order-nine degree/parity proof of
   $R(3,4)\le9$;
3. checks every stated degree threshold, 10,648 generalized high-degree
   parameter triples, all labeled injection counts through eight anchors and
   hubs, and 9,841 deficiency aggregation states;
4. reconstructs the fork parameters from the physical 43-by-43 fixture,
   independently extracts its monochromatic five-set, and checks its ten
   physical edges.

The deterministic audit output is [`EXPECTED.json`](EXPECTED.json).

## Proof audit

For the blue $rs$ case, the set of vertices red to $u$ and blue to both
$r,s$ has exact size $d-2-p-q+t$, where $t$ is the triple codegree. A red
$K_4$ there joins $u$, while a blue $K_3$ joins $r,s$. The elementary
$R(4,3)\le9$ bound therefore gives the stronger
$p+q-t\ge d-10$.

For the red $rs$ case, the common red neighbors of $r,s$ outside
$\{u\}\cup N_R(u)$ have size at least $a+b+d-44-p-q$. A red $K_3$ there
joins $r,s$, while a blue $K_4$ joins $u$, giving the second inequality.
The exact Boolean-atom calculation also confirms the claimant's slack term
$n_{000}$.

The small Ramsey input is self-contained: a triangle-free order-nine graph
with independence number at most three has degree at most three because each
neighborhood is independent. Its nonneighbors form a graph with neither a
triangle nor an independent triple, so the verified $R(3,3)\le6$ bound forces
degree at least three. A 3-regular graph on nine vertices would have odd
degree sum 27, a contradiction.

Substituting $a=b=22$ and $p=q=5$ gives lower bounds exceeding 10 in both
edge-color cases for $d\ge21$. For $d=19,20$, only the red-pair alternative
is contradictory; hence a shared fiber is a blue clique and has at most four
vertices. These implications match the claimed scope exactly.

## Scope and trust boundary

The core fork theorem uses only the displayed counting and small Ramsey
argument and is accepted unconditionally under the ambient no-monochromatic-
$K_5$ hypothesis. Calling the endpoints “dense anchors” additionally imports
the earlier thirteen-interface result that the local degree-five hub is
well-defined and the dense-hub bound that its global degree is at most 23.

The deficiency corollary imports $U(23)=122$, nonnegativity of deficiency,
the accepted uniform gap seven, and the completed interface-6/7/8 type-62
gap nine. This audit checks the additive use of those premises but does not
reprove their catalogues or solver certificates. Catalogue completeness,
Paley uniqueness, the earlier SAT/DRAT consumers, Python semantics, and
ordinary hardware remain explicit imported trust boundaries.

No high-degree hub, dense anchor, singleton fiber, or full 43-vertex graph is
shown to exist. Fibers of sizes two through four at degrees 19 and 20 and all
degree-18 fibers remain open. No correction is required for the reviewed
claim.

## Reproduction

Check out the claimant repository at the pinned commit, replay its two public
commands one at a time, and then run:

```sh
python3 -B audit_review.py \
  --source /path/to/math_source_code_open
```

Compare standard output byte-for-byte as JSON with `EXPECTED.json`. The audit
uses only Python's standard library and Git; it launches no solver and imports
no claimant code.
