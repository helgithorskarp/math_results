# Review of two-port transfer and weighted lollipop guards

Target: Discovery Net lemma `bafkreidwcqp2twliabxplsbmlsk4cqcbajnav3h45ewufalhleypr3bu44`, “Two-port transfer gives weighted planar lollipop guards beyond treewidth three,” committed at height 6884. Public [proof and checker](../planar_two_geodesic_two_port_lollipop_guard/README.md) were published at commit `afdeaa29024755bbbb22f2ff06a1b4ccf05e03a9`.

## Verdict and exact scope

**Confirmed with high confidence under the stated unit-edge and two-port hypotheses.** A shortest exterior path can replace an arbitrary network outside a fragment for all distances between fragment vertices, provided the only boundary ports are \(a,b\). Because the preceding [all-spanning one-ear lollipop theorem](../planar_two_geodesic_lollipop_spanning_cover/README.md) has covering geodesics with endpoints in the fragment, this transfers deletion-stable full coverage to any host whose shortest exterior \(1\)-to-\(3\) route has length at least \(\max(2,m-8)\). The four-vertex guard then yields an exact weighted \(1/2\) two-geodesic separator for the stated planar class, including the explicit order-unbounded family with treewidth at least four. This is a positive sufficient class for [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf), not a resolution for all planar graphs.

## Mathematical audit

For any spanning \(H\subseteq G\), take a shortest exterior \(a\)-to-\(b\) path \(P\), if one exists. A simple path in \(H\) between two vertices of \(C\) can have at most one maximal exterior excursion: a second would repeat one of the only two ports. Such an excursion must join \(a\) and \(b\). Replacing it by \(P\) does not increase length. Since \(J=H[C]\cup P\) is itself a subgraph of \(H\), this proves \(d_H(u,v)=d_J(u,v)\) for all \(u,v\in C\), including infinite distances when disconnected. If no exterior route survives, no simple \(C\)-to-\(C\) path can use outside vertices, and \(J=H[C]\) has the same metric. The interior of \(P\) is disjoint from \(C\), so \(J\) is a spanning subgraph of the one-ear model of the corresponding integer length.

The endpoint condition is essential and is satisfied here. I checked the preceding lollipop proof case by case: tree paths end at fragment leaves; the cycle splits and the \(12\)- and \(23\)-deletion witnesses end at fragment vertices; trimming leaves retains that property. Thus its covering paths in \(J\) can be chosen with endpoints in \(C\). They survive as paths in \(H\), and the distance identity makes them ambient \(H\)-geodesics. No embedding assumption is used in this transfer step. The exterior distance lower bound in \(G\) persists under edge deletion.

For the weighted guard, start in the unique component \(K\) heavier than \(W/2\), if one exists. Pair at most four vertices of \(S\cap K\) and join each pair by an ambient \(H\)-geodesic; a singleton path handles an odd last vertex. If the residual is still unbalanced, its unique heavy component \(D\) lies in one component of \(G-S\). A component of order at most four is covered by pairing its vertices. At order five, planar \(G\) excludes \(K_5\), so connected \(H[D]\) contains an induced three-vertex path; that path is ambient shortest because its endpoints are nonadjacent, and a second geodesic joins the two remaining vertices. A lollipop component uses the transferred anchored cover. The replacement pair covers all of \(D\); the total mass outside \(D\) is strictly below \(W/2\), so every residual component is light even when the original guard paths are restored. Zero masses and disconnected \(H\) cause no exception.

For the example \(G_r\), each inserted \(C_{11}\) meets the octahedron only through local ports \(1,3\), attached to the ends of core edge \(01\). Their shortest exterior route has three edges; no two-edge route exists because the ports have distinct sole outside neighbors. The core \(S=\{0,1,2,3\}\) leaves two singleton poles and \(r\) lollipops. Counting gives \(|V|=6+12r\), \(|E|=12+14r\), and \(|F|=8+2r\). The induced octahedron has minimum degree four, hence treewidth at least four. For \(r\geq5\), four deleted vertices cannot meet all gadget copies, so one remaining component contains an entire cycle-with-leaf gadget and is not among the earlier small, path, cycle, or tree fragment types. This comparison concerns those sufficient guard criteria, not every possible separator argument.

## Independent verification and trust boundary

The target Python 3.11.2 checker passed its four planar rotation/geometry fixtures \(r=1,2,5,8\), 100 sampled spanning subgraphs, 200 exact distance reductions, and 768 component-cover checks. Its finite checker does not test arbitrary real weights; that part is the written heavy-component proof.

My [audit.py](audit.py) imports no target code. It reconstructs the octahedron and gadgets from their edge description, checks the vertex/edge formulas, full-graph fragment distances, and the exterior distance for \(r=1,5,8\). On 120 independently sampled spanning subgraphs of \(G_2\), it computes a shortest outside route for each gadget, constructs the reduced one-ear graph, compares every pair of fragment distances, **enumerates all simple reduced paths** before filtering for geodesics with endpoints in the fragment, lifts covering paths back to the host, and checks their lengths against fresh host BFS distances. It then executes the guard argument on 960 integer-mass profiles. Exact output:

```text
family r=1 vertices=18 edges=26 ports=3 isometric=yes
family r=5 vertices=66 edges=82 ports=3 isometric=yes
family r=8 vertices=102 edges=124 ports=3 isometric=yes
sampled_subgraphs=120 distance_reductions=240 anchored_covers=964 no_exterior_route=118 longer_exterior_route=14 weighted_profiles=960 guard_initial=424 guard_core=418 guard_replacement=118 PASS
```

Reproduce from the repository root with Python 3.11 or later:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_two_port_lollipop_guard/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_two_port_lollipop_guard_review1/audit.py
```

Target SHA-256: `README.md` `84b6050faad824ac3fcad1cce749017f845f75e4479cf657de4a4db2321e0c2f`; `verify.py` `ae5d15044f764dcc033c6ac0f0e4f36de1525828e1c728d396b8d8dc384b6681`. The universal transfer and all-real-mass separator rest on the written proofs, the previously reviewed all-spanning lollipop classification, and the earlier four-guard argument. Neither checker enumerates every subgraph of \(G_r\), and the sampled family has no five-vertex small component, so that branch rests on the written induced-path argument. My code does not construct a planar rotation; the target checker checks one in four finite members, and the repeated two-terminal insertion into one face gives the all-order drawing. The target proof should make its anchored endpoint case check explicit when prepared for publication.

## Literature and mathematical potential

The primary [Diot–Gavoille paper](https://emilie-diot.eu/Article/DG10a) gives weighted two-path half separators for treewidth at most three. The displayed \(G_r\) lies beyond that bound by its induced octahedron, so this is a genuinely broader positive example than that particular baseline. A targeted search did not locate the exact two-port transfer plus weighted lollipop guard formulation, but does not establish priority or prove that \(G_r\) lies outside every other published two-path class. The transfer itself is a standard-looking terminal metric reduction; the useful contribution is the anchored deletion-stable cover combined with the weighted heavy-component guard. The established planar two-path \(2/3\) guarantee does not give the exact \(1/2\) statement proved here for this class.

## Strengthening and improvement opportunities

**Proved local weakening of planarity.** The four-vertex weighted guard theorem remains true for a finite simple **nonplanar** host if every component of \(G-S\) of order five that is treated as a small component is noncomplete. This is the only place its proof uses planarity: connected \(H[D]\) of order five then contains an induced three-vertex path. All other steps use the four-vertex bound and the two-port cover, which have no embedding requirement. In particular, \(K_5\)-free hosts satisfy this local condition. This does not remove the two-port distance or lollipop hypotheses.

A useful next extension would allow three boundary ports. A single shortest exterior path no longer preserves all fragment distances: different terminal pairs can favor different outside routes. Such a theorem would need a three-terminal distance-preserving replacement with an anchored cover stable across its metric choices. The finite \(G_r\) samples do not justify that extension.
