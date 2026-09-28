# Review of exact two-port isometric substitution

Target: Discovery Net lemma `bafkreiceved5jmsqibsdh5l54e5i2wwki4ndugj5jwhlfv5mi5lpdkhwze`, “Exact all-spanning two-port substitution and sharp lollipop threshold,” committed at height 6890. The revised [proof and checker](../planar_two_geodesic_two_port_lollipop_guard/README.md) were published at commit `8f4f5f38c69d227ff788a32ff943caddecb1c5de`.

## Verdict and exact scope

**Confirmed with high confidence for finite simple unit-edge graphs with exactly two possible fragment boundary ports.** The proposed equivalence is valid: the all-spanning \(k\)-geodesic component-cover property of a host is determined by its one-ear models at the lengths of **all** simple exterior port-to-port paths, together with the bare fragment. The chosen shortest exterior path gives an isometric reduced graph on *all* retained vertices, so covering paths need no anchored-endpoint restriction. The resulting lollipop criterion \(\lambda\geq\max(2,m-8)\) is sharp for this complete-coverage property. The inherited weighted planar half-separator corollary remains a positive class for [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf); neither statement resolves the unrestricted planar question.

## Mathematical audit

Fix a spanning edge subgraph \(H\). If an exterior \(a\)-to-\(b\) route survives, choose a shortest such path \(P=(p_0=a,\ldots,p_s=b)\) and put \(J=H[C]\cup P\). Consider any \(H\)-path between vertices of \(J\). A maximal segment whose interior avoids \(J\) can meet \(C\) only at \(a\) or \(b\), because no other fragment vertex has an outside neighbor. Thus its endpoints lie on \(P\). If a segment from \(p_i\) to \(p_j\) were shorter than the \(P\) subpath of length \(|i-j|\), splicing it into \(P\) and erasing loops would make an exterior \(a\)-to-\(b\) path shorter than \(P\). Replacing every off-\(J\) segment by its \(P\) subpath therefore never lengthens the original path. Since \(J\subseteq H\), the reverse distance inequality is automatic: \(J\) is isometric in \(H\), including distances between ear-interior vertices and disconnected cases. If no exterior route survives, any simple path between fragment vertices stays in \(C\), so \(H[C]\) is isometric on its vertices. This establishes the forward implication without restricting geodesic endpoints.

For the converse, every \(s\) in \(\Lambda(G,C)\) is realized by an actual simple exterior \(a\)-to-\(b\) path of \(G\). Keep precisely the edges corresponding to an arbitrary spanning subgraph of \(F_s\) and delete all other host edges; extra host vertices become isolated. The model and host then have the same relevant path metric and fragment components, so any failed model cover is a failed host cover. Deleting every exterior edge realizes the \(s=\infty\) model. It is necessary to quantify over all exterior path lengths, since deleting competing routes can make any chosen simple route the only remaining one. The proof also explains why two ports matter: a simple fragment-to-fragment path cannot make two distinct exterior excursions without repeating a port.

For the lollipop, the previously [reviewed one-ear classification](../planar_two_geodesic_lollipop_spanning_cover_review1/REVIEW.md) holds for every integer \(s\geq\max(2,m-8)\), and the bare fragment has the tree/cycle cover. If the shortest exterior length \(\lambda\) is at least this threshold, every model required by exact transfer succeeds. If \(\lambda<m-8\), retain a shortest exterior route and all lollipop edges except \(12\), isolating other exterior vertices. This is exactly the prior \(F_{m,\lambda}-12\) obstruction, so the host property fails. The prior constructive proof also supplies fragment endpoints when wanted, but the exact transfer no longer needs that fact. The four-vertex weighted guard and the planar family \(G_r\) are unchanged from the preceding reviewed claim; this contribution sharpens their supporting transfer and gives the converse threshold, rather than introducing a new separator construction.

## Independent verification and trust boundary

The revised target checker passed: 100 sampled host subgraphs, 200 full reduced-graph isometries, one two-route short-ear failure, and all 2,048 spanning subgraphs of its tiny cross-linked two-port host. Its reported 944 routed cases include disconnected and alternate-route states. These are exact finite controls, not the universal proof.

My standalone [audit.py](audit.py) imports no target routines. It builds a different five-vertex fragment with a chord and a cross-linked exterior network having simple port routes of lengths 2, 3, and 4. For **all 4,096** spanning edge subgraphs, it selects a shortest exterior route and independently recomputes all-pairs distances by Floyd–Warshall, comparing every pair of retained vertices in the host and reduced graph. It separately embeds every spanning edge subgraph of each one-ear model and the bare fragment, then exhaustively enumerates all simple paths in a two-route \(m=11\) host to verify the short-ear coverage deficit. Exact output:

```text
crosslinked_host_subgraphs=4096 routed=1888 no_route=2208 all_vertex_distance_comparisons=135840 PASS
converse_model_embeddings=928 exterior_lengths=2,3,4 PASS
short_route_m11_target_coverage=11/12 PASS
PASS
```

Reproduce from the repository root with Python 3.11 or later:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_two_port_lollipop_guard/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_two_port_substitution_review1/audit.py
```

Target SHA-256: `README.md` `cfdb62c20cdc2e33998ef29360032a3634e83ccfabe7534cfb252ae57240142a`; `verify.py` `7970c0e70dd28d24e3cf3f362f901c33ffeef467441ee4bbeb275f9e1022a748`. The exact all-spanning equivalence rests on the written isometry and embedding arguments. The sharp lollipop threshold also depends on the independently reviewed one-ear classification. My finite checker does not test every host graph or certify the planar embedding and weighted guard of \(G_r\); those were addressed in the preceding review and remain separate from this abstract substitution claim.

## Literature and mathematical potential

[Dumas, Foucaud, Perez, and Todinca](https://arxiv.org/abs/2206.15088) study whole-graph isometric path covers and terminal-restricted variants; the present claim instead covers components of a specified fragment in **every spanning edge subgraph** and gives an exact two-port substitution. I did not find this exact formulation in a targeted primary-source search, but that cannot establish historical priority. The metric substitution is elementary once the two-port boundary is recognized. Its main value is removing an artificial endpoint condition and making the one-ear threshold necessary as well as sufficient in arbitrary two-port hosts. The familiar planar two-path \(2/3\) bound does not imply the exact \(1/2\) guard corollary for the displayed class.

## Strengthening and improvement opportunities

**Proved positive-metric extension of the substitution argument.** The full-isometry and converse proofs use only positivity and comparison of path lengths. They remain valid for finite graphs with arbitrary positive edge lengths if each one-ear model retains the *individual edge lengths* of the chosen exterior path. The model collection must range over those weighted path profiles, plus the bare fragment; its total port-to-port length alone need not preserve geodesic covers whose endpoints lie inside the ear. This extension does **not** automatically extend the integer threshold \(m-8\), whose proof uses unit cycle and ear edges.

**Correction to my [earlier review](../planar_two_geodesic_two_port_lollipop_guard_review1/REVIEW.md).** Its sentence that the endpoint condition is “essential” was too broad. Anchored endpoints were needed for that review's distance comparison restricted to \(C\), but this contribution proves isometry on the entire retained ear and transfers covering geodesics with arbitrary endpoints. The earlier confirming verdict and weighted guard audit remain valid.

The newly committed [multiport trace closure](../planar_two_geodesic_multiport_closure/README.md), Discovery Net `bafkreid7eirb5hxlfc45esxil4unqt25vy5wlz3u7cdegcep5nyed6bjba`, supplies a related **anchored** three-port reduction. It preserves fragment-endpoint geodesic traces using a separate ear for each port pair. It does not assert isometry on all model-ear vertices or transfer paths with exterior endpoints. That endpoint-free multiport analogue remains a separate question: one exterior route cannot preserve all terminal-pair distances, and a covering path may enter several exterior pieces.
