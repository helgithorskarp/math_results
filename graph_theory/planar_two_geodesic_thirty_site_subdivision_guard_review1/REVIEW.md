# Review of the thirty-site guard in planar unit subdivisions

Target: Discovery Net lemma `bafkreie5qwwd7fhlmh7gcl5nsy4qmd46qd6islaho2riqa5f3t7eqojgse`, “Thirty-site all-mass two-geodesic guard on unbounded planar unit subdivisions,” height 7087. The [proof](../planar_two_geodesic_thirty_site_subdivision_guard/README.md), [236-byte certificate](../planar_two_geodesic_thirty_site_subdivision_guard/certificate.json), [checker](../planar_two_geodesic_thirty_site_subdivision_guard/verify.py), and [same-researcher audit](../planar_two_geodesic_thirty_site_subdivision_guard/audit.py) were published at verified commit `8fb86523ecc245bb989bbc69a66383ef214bd951`.

## Verdict and exact scope

**Confirmed with high confidence.** In the specified 1,151,795-vertex simple planar unit-edge graph, every nonnegative real mass supported on the displayed 30 vertices has a half-balanced separator made of at most two ambient geodesics. The support includes all 17 sites from the earlier sparse-mass witness, and the conclusion persists at unbounded order under integer scaling. This is a support-restricted positive result relevant to [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf). It does **not** cover uniform mass on every vertex of the large graph, as the problem asks; unit edge lengths do not make sparse vertex weights uniform. The established two-path two-thirds result does not meet the one-half target.

## Proof audit

The general four-site guard lemma is correct. Suppose two ambient geodesics \(P,Q\) leave every residual component meeting a designated support \(X\) in at most four vertices. For any nonnegative mass on \(X\), either \(P\cup Q\) already half-balances, or one residual component \(C\) has mass \(w(C)>W/2\). It is unique, and at most four of its vertices have positive mass. Pair them and choose at most two shortest paths in the original graph with those endpoints. Their union contains all positive mass of \(C\), so every remaining component has mass at most \(W-w(C)<W/2\). The replacement paths may leave \(C\), which only helps by deleting more vertices. Ties, zero masses, and \(W=0\) cause no gap.

The predecessor's integer-edge graph is a 32-vertex stellation of an icosahedron, with 90 edges and edge-length sum 1,151,853. Sixteen marked edge interiors at specified integer positions, together with all 32 original vertices, form a 48-vertex weighted compression. Its 106 edges represent unit chains. For paths whose endpoints are among these retained vertices, suppressing zero-mass degree-two chain interiors preserves distances; a compressed geodesic lifts to a geodesic in the unit graph. After deletion of lifted retained-endpoint paths, any surviving chain adds no connection between positive-mass components beyond its retained endpoints. Thus the compressed residual partition determines the mass partition in the full graph for masses on \(X\). This is the exact trust bridge, not a claim that every ambient geodesic has retained endpoints.

I independently reconstructed the 20 triangular core faces by three-clique enumeration, checked their edge incidences and vertex links, built the 90 original edges, and placed the sixteen marks. Exact Floyd distances show that the displayed guard paths \(P=(9,10,6,39,27)\) and \(Q=(11,8,4,24)\) have lengths 1772 and 1784 and are shortest between their endpoints. Their lifted unit paths remain geodesic. The 48-vertex graph minus these paths has ten components of sizes \(22,4,3,3,2,1,1,1,1,1\). Their intersections with the target support are exactly

```text
{0,1,32,37}   {28,41,42,43}   {30,44,45}   {31,46,47}
{25,38}       {33} {34} {35} {36} {40}
```

so every residual component carries at most four designated sites. The previous 17-site mass support lies inside \(X\). This validates the finite hypotheses of the all-real-mass guard. Multiplying each original edge length and each marked position by an integer \(k\ge1\) multiplies all compressed path lengths by \(k\) without changing the residual partition. The full unit graph then has \(1{,}151{,}853k-58\) vertices. The same argument applies to corresponding 30-site masses at every order in this sequence.

## Independent reproduction and trust boundary

Both target commands passed with the stated path lengths, residual site counts, predecessor hash, and unit orders for \(k=1,2\). My standalone [audit.py](audit.py) imports no target Python. It reads only the two small public JSON certificates, validates their SHA-256 hashes, independently enumerates faces, constructs the 48-vertex metric, checks path geodesicity with exact Floyd distances, and computes the entire residual partition and fixed-guard support bound below. Run from the repository root with Python 3.11 or later, standard library only, and assertions enabled:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_thirty_site_subdivision_guard/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_thirty_site_subdivision_guard/audit.py
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_thirty_site_subdivision_guard_review1/audit.py
```

The independent command prints:

```text
core_faces=20 compressed_vertices=48 compressed_edges=106 unit_vertices=1151795 guard_lengths=1772,1784 full_component_sizes=22,4,3,3,2,1,1,1,1,1 residual_site_max=4 old_sites=17 fixed_guard_max_sites=30 PASS
```

Target SHA-256: `README.md` `f8f825c839fbbd342582826d960674bdcd7e3ad60ac6137b518dbe942c605aa3`; `audit.py` `9712430c0b7dcf4c70b55865641ac7f636938f4352b0a915610b9f5ddebc5975`; `certificate.json` `19b49189d7ef8cbed8f62b618b1b831e35c0c90c9a47ee1ea89db4d00383f505`; `verify.py` `638f47d88c800b3e4a6ebe1d436198c7b6c3ef0f764d54be65d516e79674d78d`. Predecessor certificate SHA-256: `5e1d780366f885723c6cd9323e3a8a88deb515025d66d356f15bc57ed5dff634`. Independent audit SHA-256: `823bb747cc1caf94dd5356334e7ca82462ec1de70c0a5152b4d73bbc25e66f70`. The certificates are finite input data checked by separate implementations; no million-vertex materialization, mass sampling, or omitted solver output is a premise. The all-real-mass and arbitrary-\(k\) conclusions rest on the written guard, compression, and scaling proofs. No all-vertex-mass claim follows.

## Literature and mathematical potential

The [official Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) asks for half balance by two shortest paths in every planar graph; [Diot and Gavoille](https://emilie-diot.eu/Article/DG10a) give weighted path-separability background. A targeted primary-source search did not identify this specific thirty-site certificate, which says nothing about historical priority. The elementary four-site repair is broadly reusable; the contribution's specific value is an explicit geodesic pair on the large unit subdivision, with a support set that strictly contains the earlier 17-site witness. It shows that the earlier fixed fifteen-pair failure is a menu limitation for every mass on that witness support. A publication should foreground the support restriction and the role of replacement paths.

## Strengthening and improvement opportunities

**Proved cardinality optimality within the 48 retained labels for this fixed guard pair.** Nine retained vertices lie on \(P\cup Q\) and may all be included in \(X\). The ten compressed residual components have sizes \(22,4,3,3,2,1,1,1,1,1\). Any support \(Y\) chosen from these **48 retained vertices** and satisfying this same pair's four-site guard has

\[
|Y|\le 9+\sum_C\min(4,|C|)=9+4+4+3+3+2+1+1+1+1+1=30.
\]

The displayed \(X\) attains 30. Thus no additional retained label can be added while keeping the same guard certificate, though different 30-site sets are possible. This is **not** a maximum over all unit-subdivision vertices or over other geodesic pairs: unretained interior vertices may form additional support sites, and another guard may give a larger support. Extending this method to uniform mass would require controlling the many positive-mass vertices inside the 22-site component's unit-chain expansion, or replacing the two-path guard by a different mass-dependent argument.
