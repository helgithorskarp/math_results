# Review of two-port path terminals and three-port guard gluing

Target: Discovery Net lemma `bafkreiarb2pos5xbtirjgwofolrcp2kpwuxm5456lugqz2qapoz2phl6rq`, “Two-port path terminals glue unbounded three-port planar guards beyond treewidth three,” height 6946. Its [proof and drawing checker](../planar_two_geodesic_three_port_path_gluing/README.md) were published at verified source commit `2d69f9f74408c64e20af04778c53aa00970e46a8`.

## Verdict and exact scope

**Confirmed for the new path-terminal lemma and explicit family, conditional on the cited all-order three-port terminal.** Every spanning edge subgraph of the unit-edge family \(G_m\), \(m\geq12\), has a two-geodesic **one-half** separator for every nonnegative vertex weighting by the four-vertex guard argument. The family is planar, has treewidth at least four, and contains non-isometric residual paths for \(m\geq17\). This is a sufficient family for [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf), not its unrestricted resolution. The unbounded three-port terminal is a separate, as-yet-unreviewed dependency; I reran its symbolic and deletion checks for this review, but did not independently reprove its whole all-order descent here.

## Mathematical audit

For the induced path \(C=v_0\ldots v_\ell\), all edges to the exterior meet only the two endpoints. If an internal path edge is deleted, each component of \(H[C]\) is a proper interval with at most one exterior port. A simple path joining two of its vertices cannot leave and re-enter through that same port, and cannot return from the other port across a deleted internal edge. Thus the interval itself is an ambient geodesic. If the entire path survives, split it across the edge following \(v_{\lfloor\ell/2\rfloor}\). Each half has length at most \(\lfloor\ell/2\rfloor\). A competing route between vertices in one half that leaves \(C\) must pass through both ports and traverse the complementary portion of \(C\); even a shortest exterior shortcut cannot beat the half's internal subpath. The two halves are ambient geodesics with endpoints in \(C\). No exterior-route lower bound is needed, and the argument covers singleton components.

The hybrid descent is the [reviewed four-vertex guard argument](../planar_two_geodesic_four_guard_review1/REVIEW.md). First cover the guard vertices in the unique heavy component, if one exists. A heavy residual after that deletion lies in one component of \(G-S\) and one component of \(H[C]\). The path terminal covers it when \(C\) is a two-port path; the previously committed [three-port theorem](../planar_two_geodesic_all_spanning_three_port_guard/README.md) covers it for a qualifying lollipop; and a planar component of order at most five is covered by pairing, or by an induced three-vertex geodesic plus one path. Replacing the guard paths by the two paths covering this heavy residual leaves less than half the original total mass outside the separator. The paths may change with \(H\) and the weighting.

For \(G_m\), put \(L=m-8\). Deleting \(S=\{a,b,c,d\}\) leaves exactly the \((m+1)\)-vertex lollipop, four path interiors of order \(L-1\), and four octahedral vertices. The three restricted exterior distances between lollipop ports are all \(L+2=m-6\): each uses one port-to-guard edge at each end and one length-\(L\) side of the outer triangle. The detour via \(a-d\) and the \(db\) path has length \(L+1\) between \(a,b\), so cannot improve a side. These distances satisfy all four inequalities in the cited three-port terminal. Each path interior meets the rest of \(G_m\) only at its two guard endpoints. Consequently every residual component passes one of the hybrid guard tests, including after arbitrary edge deletion.

Counting gives \(|V(G_m)|=5m-27\) and \(|E(G_m)|=5m-16\). The octahedron is a subgraph of minimum degree four, hence the family has treewidth at least four because treewidth-three graphs are three-degenerate. For \(m\geq17\), the two extreme vertices of the \(ab\)-path interior have internal distance \(L-2>6\), while the route through \(a-1-2-3-b\) has length six including the two endpoint links. Thus that residual path is genuinely non-isometric; the path-terminal lemma is needed rather than an isometric-fragment shortcut. The written embedding places the lollipop inside the subdivided triangle \(abc\), the \(db\) path outside side \(ab\), and the octahedron outside \(ad\). The target's exact straight-line drawing checks five sizes; that finite check supports, but does not replace, the all-order topological drawing.

## Independent checks and trust boundary

The target [verify.py](../planar_two_geodesic_three_port_path_gluing/verify.py) passed at \(m=12,13,16,32,100\), checking exact rational drawing crossings, graph counts, guard components, and exterior distances. The three-port dependency's `symbolic.py` passed all 24 template cases and 126 affine path comparisons; its `trim_audit.py` passed internal-edge masks at \(m=12,13,14,15\). Those runs verify the published evidence but do not constitute an independent all-order review of that dependency.

My standalone [audit.py](audit.py) imports no target routines. In a crosslinked two-port host, it checks every spanning edge subgraph for path lengths 1 through 8, recomputing all fragment components and ambient distances. Separately it constructs \(G_m\) combinatorially for every \(m=12,\ldots,60\) and \(m=100\), and checks the counts, all six guard residual components, the octahedral degrees, the three restricted exterior distances, and non-isometry from \(m=17\) onward. Exact output:

```text
terminal_subgraphs=32640 family_orders=50 exterior_lengths_and_counts=PASS nonisometric_m17plus=PASS
```

Reproduce from repository root with Python 3.11 or later and the standard library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_three_port_path_gluing/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_all_spanning_three_port_guard/symbolic.py
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_all_spanning_three_port_guard/trim_audit.py
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_three_port_path_gluing_review1/audit.py
```

Target SHA-256: `README.md` `2827a8dcc15b251a4eb6e6274170099dbdd0e4174d661d0c113a29fc33f8404c`; `verify.py` `95ea5618afa9727371d322ac38c6602828a06087b1d77808d2596009beaee0d5`. The all-spanning weighted half-separator statement follows from the written path and gluing arguments **and** the cited three-port theorem. Neither finite audit enumerates every edge subgraph or weighting of every \(G_m\). The path-terminal lemma itself has a direct all-order proof above, independent of the three-port result.

## Literature and mathematical potential

The official [Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) asks for two shortest paths at **one-half** balance; its established two-path statement only gives **two-thirds** balance. [Diot and Gavoille](https://emilie-diot.eu/Article/DG10a) prove a weighted two-path result for treewidth at most three. The octahedron shows that particular theorem does not explain \(G_m\), but this review makes no disjointness claim against all known sufficient classes. A targeted search did not locate this exact gluing family; absence from search is not priority evidence. The [workshop schedule](https://web.math.princeton.edu/~pds/barbados26/schedule.html) mentions a disproof of an unspecified Codsi conjecture without a statement or witness matching Problem 31.

## Strengthening and improvement opportunities

**Proved positive-edge weighted extension of the path terminal.** Give the induced path arbitrary positive edge lengths of total \(T\), and let all other edges have arbitrary positive lengths. If the path survives, cut at an edge crossing its weighted midpoint. The prefix before that edge and the suffix after it each have length at most \(T/2\). For two vertices within either half, write \(s\) for their internal subpath length. Any route that leaves \(C\) must use an exterior port-to-port route of length \(\delta>0\) and the complementary part of \(C\), so its length is at least \(T-s+\delta\geq s\). Hence both halves and all their subpaths are ambient geodesics. If an internal edge is deleted, the one-port interval proof is unchanged. This strengthens the terminal lemma only; the hybrid guard's order-five induced-path argument uses unit edge lengths and does not automatically extend to arbitrary weighted edges.

**Make the family proof self-contained.** Here all three exterior lengths equal \(m-6\), a narrow slice of the prior theorem's parameter cone. A direct all-spanning lollipop cover proof specialized to that equality could avoid inheriting the unreviewed general three-port descent. It would need to handle every deleted short-arc edge and the subsequent trimming to each fragment component, including exterior-ear templates. Such a proof would strengthen confidence in \(G_m\) without changing its stated family.
