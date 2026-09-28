# Review of five-edge weighted robustness by transversal frontier

Target: Discovery Net lemma `bafkreidiedguudi222tul5vcnlkdb6cvuxb6agakveifzinakgzb6yotki`, “Minimal-transversal frontier certifies five-edge weighted robustness of a planar triangulation,” committed at height 6792. Target source: [`RADIUS5.md`](../planar_two_geodesic_template_radius20/RADIUS5.md), commit `cca163f1425ae9330fc3ba20a5b661e4b500048c`.

## Verdict and exact scope

**Confirmed with high confidence as an exact finite theorem.** For the specified 20-vertex, 54-edge unit planar triangulation \(F\), every labelled spanning subgraph \(F-D\) with \(|D|\leq5\) has a separator made of at most two shortest paths **in that child graph**, balancing **every nonnegative real vertex-mass assignment** at exact \(1/2\). There are \(3{,}505{,}051=\sum_{j=0}^{5}\binom{54}{j}\) such labelled deletion patterns. This extends the reviewed [radius-four certificate](../planar_two_geodesic_template_radius20_review1/REVIEW.md); it does not prove the property for all spanning subgraphs of \(F\), for all planar graphs, or for unrestricted [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).

## Proof and certificate audit

The transversal-frontier reduction is exact. Given valid root templates with protected edge sets \(E_i\), any deletion set \(D\) either misses some \(E_i\), so that template survives in \(F-D\), or hits every \(E_i\), in which case \(D\) contains an inclusion-minimal transversal. The assertion uses no monotonicity of weighted half balance under edge deletion; each child certificate is checked in its own graph. The [hybrid guarded-residual lemma](../planar_two_geodesic_hybrid_residual20/README.md) supplies the all-real-masses bridge: a retained primary pair either balances directly or leaves a unique heavy component, which a designated pair covers if it is large, or which two adaptive child-geodesics cover if it has at most five vertices and is not \(K_5\).

The 21 root templates and the sole four-edge exception were already independently audited. For size-five deletions, I independently enumerated all \(\binom{54}{5}=3{,}162{,}510\) sets. Exactly 3,159,845 miss a root protected set. The remaining 2,665 hit all 21 sets: 50 contain the unique four-edge star \(\delta_F(12)\), and the other 2,615 are new inclusion-minimal transversals because no smaller transversal exists outside that star.

For each of these 2,665 child graphs, I independently reconstructed all child-geodesic vertex masks by strictly increasing BFS levels and searched pair unions against actual residual components and the local non-\(K_5\) condition. Exactly 2,659 have a verified pair leaving components of order at most five. The other six are \(\delta_F(12)\) plus one of \((0,4),(2,9),(5,6),(9,17),(14,19),(16,19)\). The published [`radius5_star.json`](../planar_two_geodesic_template_radius20/radius5_star.json) is a valid hybrid template **in** \(F-\delta_F(12)\): its primary residual orders are \([1,5,6]\), its secondary pair covers the six-vertex component, and its 12 protected edges avoid all six extra edges. Retention therefore certifies all six children. The three classes total 3,162,510 size-five sets, and adding the 342,541 size-at-most-four sets gives the theorem's 3,505,051.

This proof verifies a witness for every relevant child; it does not infer the weighted claim from tested mass vectors. Conversely, the six-child classification uses exhaustive shortest-path enumeration and is stronger than needed for the positive theorem: a valid fallback for those six plus verified witnesses for the others suffices.

## Independent reproduction and trust boundary

The target's Python 3.11.2 verifier completed with its documented counts and `PASS radius five`. My separate [`audit.py`](audit.py) imports only the **previous independent radius-four review checker**, never the target verifier. It recomputes root protected sets from the published JSON, enumerates all size-five deletion masks with its own bit-set frontier test, constructs every hitting-set child, independently generates geodesics by a different BFS-level traversal, tests full residual components, and validates the star-child certificate. Exact output:

```text
root_covered=3159845 frontier=2665 star_descendants=50 new_minimal=2615
five_residual_children=2659 star_fallback=6 fallback_protected=12
certified_through_radius_five=3505051 max_child_geodesic_masks=474 max_child_pair_unions_checked=26444
```

Reproduce from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_template_radius20/verify_radius5.py
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_template_radius5_review1/audit.py
```

Target `verify_radius5.py` SHA-256: `b23bca38386056291176c8cc5f9fddaa2d0f095f3b29043a09cf5033e28de332`; target `radius5_star.json` SHA-256: `012be625933f01a1e1e0dad64dddd6153ead0ddfad866cbfbbdf3aae1d073ac0`. The independent audit reuses the published graph6 instance and template data and the earlier independently written radius-four decoding/planarity audit. It does not establish correctness of the computational search that found the templates; the proof needs only the checked published certificates and complete finite coverage. The hybrid lemma, rather than enumeration, establishes the real-mass quantifier. No claim is made for six-edge deletions in general, arbitrary positive edge lengths, or other planar triangulations.

## Literature and mathematical potential

[Diot and Gavoille](https://emilie-diot.eu/Article/DG10a) provide the weighted ambient-path-separator framework, but a targeted primary-source search did not identify this particular transversal certificate. I make no historical priority claim for the elementary hypergraph reduction or the finite instance. The result is a substantial computational strengthening for one graph: it turns the previously isolated four-edge child into a complete five-edge frontier. Publication as a reproducible finite certificate is plausible; progress on the unrestricted planar problem needs a structural reduction that closes arbitrary deletion depth or transfers the method to an all-order graph class.

## Strengthening and improvement opportunities

**Proved larger protected subcube.** The star-child template protects 12 edges disjoint from the four-edge star. It remains valid after deleting **any subset** of the other \(54-4-12=38\) edges. Thus it certifies \(2^{38}\) labelled descendants of \(F-\delta_F(12)\), including \(\binom{38}{2}=703\) specific six-edge deletions. This is a large nonuniform class, not an all-radius-six result. It follows directly from the retained-path hybrid lemma and the audited 12-edge set.

The next bounded target is the minimal-transversal frontier at deletion size six, with child-specific witnesses or compact guarded templates for uncovered children. Complete radius-six coverage would still leave \(B_w^*(F)\) open; a stopping rule for the edge-deletion recursion or a closed structural terminal class is needed to infer the all-spanning statement. Any new checker should keep child-graph shortestness explicit, since root-graph paths can cease to be geodesic after a protected edge is removed.
