# Independent review of the exact determination `C(13,7,5)=78`

## Verdict and scope

**Accepted.**  Discovery Net proof attempt
`bafkreibwt4wn3ozgufctug6jedbr33mohnbhp5z2fezov2dovnht5dbqcm`
(height 4341) correctly establishes

\[
\boxed{C(13,7,5)=78}.
\]

The review used the target as committed at
`818b1f8af96c964667ab5163345d919c8da1608a`.  It checked the proof boundary,
all supplied hashes, two submitted exact checkers, fresh deterministic
certificate generation, the relevant primary literature, and a third
clean-room implementation archived here.  No mathematical or reproducibility
defect was found.

This verdict accepts the stated theorem and its computer-assisted proof.  It
does not assert historical priority: targeted searches found no earlier exact
determination, but a negative search cannot establish priority.

## Proof audit

Krug's certified `C(12,6,4)=41` theorem gives the lower bound 77.  The
previously reviewed
[global point-link bridge](../covering_c1375_global_point_link_bridge_review1/)
places every hypothetical 77-block cover in an `e0` or hard-`e1` branch.  The
[hard-`e1` review](../covering_c1375_hard_e1_elimination_review1/) accepted its
exact exclusion.  It therefore remains to exclude `e0`.

In `e0`, two degree-41 points have pair multiplicity 20.  The blocks split,
according to which roots they contain, into categories of sizes

```text
A=20, B=21, C=21, D=15.
```

Deleting the roots identifies the `A` family with the unique 20-block
`C(11,5,3)` cover `M`.  Both `M union B` and `M union C` are 41-block
`C(12,6,4)` covers.  Blocks may be assumed distinct: deleting a repeated
block would produce a cover of size at most 76, contradicting the established
lower bound 77.

For a 21-block extension of `M`, the eleven point-degree excesses are
nonnegative and sum to six.  The 8,008 labeled weak compositions form exactly
143 orbits under the full order-240 automorphism group of `M`.  Exact integer
Farkas certificates exclude 142 profile orbits, accounting for 8,006 labeled
profiles.  Each relaxation uses the necessary residual-quadruple, block-count,
point-degree, pair-shadow, and triple-shadow constraints.

The sole surviving profile orbit is `1^6 0^5`, of size two.  Replaying the
earlier twelve exact extension certificates proves uniqueness at its
representative.  Transport under the full group gives exactly two labeled
extensions, each with stabilizer order 120.  Thus `B,C` reduce, up to group
action and root exchange, to `same` and `different` cases.

The 15 remaining `D` blocks would have to cover respectively 316 or 280
residual five-sets.  Exact integer Farkas certificates make even the continuous
box relaxation infeasible in both cases.  Together with hard-`e1`, this
excludes every 77-block cover.

For the matching upper bound, the checker develops the projective plane of
order three from the cyclic line `{1,2,4,10}`.  The unions of its 78 line pairs
are distinct seven-sets and cover all 1,287 five-sets: 1,170 occur once and 117
occur four times.

## Exact evidence

All hashes in the target and its imported classification passed.  The target's
tuple and bit-mask checkers also passed under both ordinary and optimized
Python, so their assertions were not the sole enforcement mechanism.  The new
certificate has SHA-256
`1219b1f4dd9f1e7df97135a5f45df206174c678960d8c2d71766ec960a427aa0`.

Fresh generation with CPython 3.11.2, `highspy==1.11.0`, and `numpy==2.4.6`
reproduced the 1,298,480-byte certificate byte-for-byte.  HiGHS is outside the
proof trust boundary: all resulting inequalities were checked with Python
integers.  Their exact statistics are:

| systems | count | rows | residual rows | support | minimum gap |
| --- | ---: | ---: | ---: | ---: | ---: |
| excluded link-profile orbits | 142 | 457 | 230 | 154--197 | 8 |
| terminal `same` | 1 | 317 | 316 | 156 | 9 |
| terminal `different` | 1 | 281 | 280 | 148 | 9 |

For every row `l_i <= A_i x <= u_i`, a positive dual multiplier uses the lower
bound and a negative multiplier uses the upper bound.  The checker reconstructs
`c*x >= b` and proves exactly

```text
b > sum_j max(c_j,0),
```

contradicting `0 <= x_j <= 1`.  Hence no floating-point tolerance enters the
accepted infeasibility claims.

## Clean-room incidence audit

[`independent_incidence_audit.py`](independent_incidence_audit.py) imports no
submitted code.  It parses the source objects independently and asks
NetworkX's generic colored-graph isomorphism engine for every automorphism of
the point-block incidence graph of `M`.  It finds all 240 automorphisms and
checks equality with the subgroup generated in the submission.

The script then independently reconstructs all 8,008 profiles, 143 profile
orbits, 457-row link systems, twelve prior extension systems, two extension
orbits and stabilizers, terminal residual systems, exact dual sums, and the
78-block upper cover.  It explicitly checks that the lone surviving profile
transports to the certified witness.

Run from this directory with CPython 3.11 and NetworkX 3.5:

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 independent_incidence_audit.py \
  ../covering_c1375_fixed_link_symmetry/cover_41.txt \
  ../covering_c1375_hard_e1_link_classification/ORBIT11_EXTENSION.txt \
  ../covering_c1375_hard_e1_link_classification/FARKAS_CERTIFICATES.json \
  ../covering_c1375_exact_78/FARKAS_CERTIFICATES.json \
  | diff -u EXPECTED_OUTPUT.txt -
```

The same command was also run with `python3 -O` and produced the identical
output.

## Sources, novelty, and trust boundary

The primary literature was checked directly.  Theorem 1 of Charlie Krug's
[certified paper](https://arxiv.org/html/2607.23766) proves
`C(12,6,4)=41`; Lemma 4 supplies `C(10,4,2)>=9`; Proposition 5 gives
`C(11,5,3)=20`; and Proposition 15 gives uniqueness of its optimal cover with
automorphism group of order 240.  Corollary 17 records the prior lower bound
77 and the paper explicitly leaves the 77-versus-78 gap open.

Theorem 2.3.24 of I. Bluskov's primary thesis
[*New Designs and Coverings*](https://central.bac-lac.gc.ca/.item?app=Library&id=nq24295&oclc_number=46548328&op=pdf)
records `C(13,7,5)<=78` via the projective-plane construction.  The downloaded
3,295,882-byte PDF had SHA-256
`112fab5df1cd17c3ffbde6f9a6a5f921a6bafa9fc4754f54f5dcf34b19bdab37`.
The independent checker directly verifies that construction, so the upper
bound does not rest on transcription from the PDF.

The remaining trust boundary is Krug's certified theorem and uniqueness
result, the previously reviewed global bridge and hard-`e1` elimination,
CPython/NetworkX for this independent audit, and the human translation of the
mathematical constraints.  The duplicated submitted implementations and this
structurally different incidence-graph checker materially reduce code-level
common-mode risk.
