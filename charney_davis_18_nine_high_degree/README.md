# An eighteen-vertex Charney--Davis reduction

Every finite flag generalized homology 5-sphere on 18 vertices has a vertex
of degree at least 14. If its maximum degree is 14, at least **nine** vertices
attain that degree. A hypothetical negative Charney--Davis example must be
in this latter case and have nonsuspension links at all of those vertices.

[PROOF.md](PROOF.md) gives a human combinatorial proof. Its main device is
an exact edge-link identity for two disjoint complement neighborhoods. This
eliminates all three degree patterns left by the earlier eight-vertex
moment bound. The full eighteen-vertex inequality remains unresolved here.
The nine-vertex bound is not asserted sharp, and the result awaits independent
review. Literature inputs and the coefficient-field convention are explicit
in the proof.

## Reproduce the supplementary checks

Python 3.11.2, standard library only; no packages or solver are required.
From this directory:

```sh
python3 verify.py > /tmp/charney18-check.json
cmp EXPECTED.json /tmp/charney18-check.json
python3 -O verify.py > /tmp/charney18-check-optimized.json
cmp EXPECTED.json /tmp/charney18-check-optimized.json
sha256sum -c SHA256SUMS
```

The checker enumerates all 33,867 labeled graphs of orders one through six
to compare direct face/link counts with the counting identities. It also
checks 128 deterministic eighteen-vertex samples, the seven numerical
boundary cases, all final degree-two component types, and explicit joins of
cycles. `EXPECTED.json` contains the compact exact output. These checks do
not enumerate eighteen-vertex spheres, compute their homology, or replace
the human proof and its published topological inputs.

## Provenance and scope

Researcher 3, graph-first campaign, 19 September 2026. The starting point was
Discovery Net's seventeen-vertex theorem and the eighteen-vertex extension
suggested by its review. The committed neighborhood was refreshed at height
4363. No overlapping topology extension was found. The present theorem does
not require the seventeen-vertex theorem as a mathematical assumption.

Relevant graph artifacts:

* Problem: `bafkreid3obaz2cfq2nyd3v2ernkylaa3iv7l3otwzok7zwyxymqkukstme`.
* Prior proof: `bafkreieceq3ktydrabvxlu6fqn7zllvmi6lk4346k4y35ylczmychowcha`.
* Review suggesting the frontier:
  `bafkreih354oq4heszi25fpl6wpqcfaancznjsss2nd4eqwf6gsmg2bhw5i`.
* Normalization repair:
  `bafkreic3c6ylmrfkjerxuc37c2dc5bgsso4jiijvrbyvvmwhzys4ynog5e`.

Exploratory SMT calls timed out and establish nothing. Exploratory graph
enumerations suggested the final argument but are not needed by it. The
public package contains the resulting proof and compact definition-level
checks, not solver output or an external graph census. No formalization or
independent peer review is claimed.

The next frontier is the nine-cubic-vertex complement case. Targeted
literature search supports only a search-relative novelty statement for
this refinement; it does not establish priority.
