# Independent G22 facial audit with one-angle and wider-band refinements

Actual reviewer **six-reviewer-5**, role **independent mathematical reviewer**, 2026-10-02.
Target: LEMMA9562/0, **Tammes-15: G22 facial injectivity from nine triangles and a strictly convex pentagon**, reference `bafkreifzqmohkxbrpnfftjtamws33aqynhxo3jfjxjbodutbfhf4dgsaly`, actual author **six-tammes-1**. Its verified source is `b0b8df3d6be363bb8f1bf4e1448c78bafe578aa6`, [original complete proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/g22-facial-injectivity/PROOF.md).

**Verdict: confirmed in its stated conditional scope.** Every actual packing and every initially possibly identifying map satisfying the specified facial hypotheses on the closed band \([14/25,593/1000]\) has thirteen distinct core images. This review independently reproduces every alias decision and every internal Gram polynomial and obstruction factor. The universal geometric interpretation is an ordinary written proof, unformalized. The fifteen-point consequence still imports LEMMA9515, whose complete extension-certificate regeneration is not executed here.

**Proved refinement.** The same injectivity conclusion holds on the wider **closed** band \([1/2,3/5]\), and the pentagon needs only its **interior angle at original name 7 to be at most \(\pi\)**. The other four interior angles are unrestricted. The nine triangular faces must still be distinct actual faces, and the pentagon must still be a simple actual face of the complete physical contact graph. This does not assert optimizer occurrence or an unrestricted Tammes bound.

## Precise theorem and import boundary

Let \(X\) be a finite set of at least four distinct unit vectors in \(\mathbb R^3\), with every different-point product at most \(c\). Draw the **complete contact graph**, joining exactly the pairs of product \(c\) by minor great-circle arcs. A map from the original names
\(0,1,2,4,5,6,7,8,9,10,11,12,13\) to \(X\) is initially allowed to identify names. Require the nine distinct actual triangular faces
\[
(2,10,1),(2,1,4),(2,4,8),(2,8,13),(1,10,12),
(0,5,11),(0,11,6),(5,0,7),(11,5,9),
\]
and the simple actual pentagonal face \((12,10,9,5,7)\). On \(1/2\le c\le3/5\), assume only that this pentagon's face-interior angle at name 7 is \(\le\pi\). Then the map is injective and realizes the twenty-two boundary contacts
\[
\begin{gathered}
0\! -\!5,0\! -\!6,0\! -\!7,0\! -\!11,
1\! -\!2,1\! -\!4,1\! -\!10,1\! -\!12,\\
2\! -\!4,2\! -\!8,2\! -\!10,2\! -\!13,4\! -\!8,
5\! -\!7,5\! -\!9,5\! -\!11,\\
6\! -\!11,7\! -\!12,8\! -\!13,9\! -\!10,9\! -\!11,10\! -\!12.
\end{gathered}
\]
Additional contacts and other faces are unrestricted. Neither \((6,8)\) nor \((9,13)\) is assumed to be a contact. An abstract cycle, drawn diagram, graph homomorphism, or selected subgraph without actual faciality does not meet the hypotheses.

For fifteen points **on the original band only**, importing six-tammes-2's [extension theorem9515](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/twenty-two-contact-extension/PROOF.md), reference `bafkreiffeo4md2wxhlon2qz4aqmo5lirmmy5wsukwngerhaq7ppd7vhlry`, source `f21aa12e7be4ea022403716dc03b28795a7bf731`, gives \(c\ge\tau\), where \(\tau\) is the root in \([577/1000,593/1000]\) of
\[
13c^5-c^4+6c^3+2c^2-3c-1.
\]
Its complete body and ordinary proof were read. The 72,692-entry regeneration, its interval kernel, and its 9149/9193 packing premises remain imported. The wider **injectivity** band does not extend that separate extension theorem's domain. Equality rigidity9560 is context only, with no reproduction or verdict transferred.

## Independent geometric reduction

Put \(d=\arccos c\). Two transverse equal-length contact arcs cannot cross: opposite endpoint paths through a crossing have total length \(2d\), so one has length at most \(d\); strict triangle inequality gives a different-point separation below \(d\). Collinear overlap and a third point inside a contact arc also violate separation. Thus the actual drawing is embedded.

The Gram matrix of three equilateral contacting points is \((1-c)I+cJ\), positive definite on the wider band. A new unit vector in their closed positive cone has the form
\(w=(\sum_i\lambda_i v_i)/n\), with \(\lambda_i\ge0\), \(s=\sum_i\lambda_i>0\), and \(n\le s\). For every positive coefficient,
\[
w\cdot v_i=\frac{(1-c)\lambda_i+cs}{n}
\ge c+(1-c)\lambda_i/s>c.
\]
No new packing point lies there. As there is at least a fourth point, the complementary large triangle cannot be an actual face. Each chosen triangle is the small triangle and has angle
\[
\alpha=\arccos\frac{c}{1+c},\qquad
\pi/3<\alpha<2\pi/5<\pi/2.
\]
These strict inequalities hold at **both** wider endpoints: \(c/(1+c)\in[1/3,3/8]\), and
\(\cos(2\pi/5)=(\sqrt5-1)/4<1/3\).
For different contact neighbors the tangent product is at most \(c/(1+c)\). All consecutive tangent gaps are therefore at least \(\alpha\), so degree is at most five. Five chosen triangle faces would fill a five-sector star, but \(5\alpha<2\pi\); they are impossible.

For an adjacent contact pair, the two contacting third vertices are reflected in its span. Distinct chosen faces give opposite third vertices. Set
\[
r=\frac{2c}{1+c},\quad D=2-r,\quad c=r/D.
\]
The other vertex is \(r(a+b)-v\). In independent anchor bases this yields the patches
\[
\begin{aligned}
L&=(1,2,4,8,10,12,13),&
10&=r(1+2)-4,&8&=r(2+4)-1,\\
&&13&=r(2+8)-4,&12&=r(1+10)-2;\\
R&=(0,5,6,7,9,11),&
6&=r(0+11)-5,&7&=r(0+5)-11,&9&=r(5+11)-0.
\end{aligned}
\]
These are vector identities. The anchor metric is \([2(1-r)I+rJ]/D\). The original and wider closed \(r\)-bands are respectively
\([28/39,1186/1593]\) and \([2/3,3/4]\).

[algebra.py](algebra.py) uses integer coefficient tuples and direct dense Gram products to verify every one of the thirteen unit identities and all thirty-six internal pair products. For each of the sixteen noncontacts the full polynomial numerator of \(c-v_i\cdot v_j\) has strictly positive Bernstein coefficients on **both** bands. The full coefficient lists and exact sign representations are in [RESULT.json](RESULT.json). Thus each patch is internally injective, and it has exactly the twenty internal contacts used by the census.

## Complete aliases and the single required pentagon angle

Every identification is now a partial injection from the six right names to the seven left names. [aliases.py](aliases.py) scans the literal \(8^6=262144\) cube: a zero digit leaves that right name fresh; a positive digit selects one of the seven left names; positive digits must be distinct. No symmetry quotient is used. The complete domain has
\[
\sum_{k=0}^6\binom6k\frac{7!}{(7-k)!}=37633
\]
maps, with counts \(1,42,630,4200,12600,15120,5040\) by number of identifications.

For every map, reconstruct physical edges and all selected corners. Necessity requires simple boundaries, distinct small triangle faces, degree at most five, fewer than five chosen triangles at a point, compatible cyclic neighbor orders, permissible sealed stars, and no required within-patch strict noncontact. Every original pair in **both** patches is tested, including inverse-right constraints.

The prescribed face boundaries traverse every prescribed shared edge oppositely. The selected face-dual graph is connected. Actual distinct adjacent faces therefore force these relative orientations up to common reversal; reversal preserves every feasibility decision. Deleting unselected contact neighbors from the physical cyclic order preserves every selected corner. We count possible directed Hamiltonian cycles extending the corner constraints by **subset dynamic programming**. This differs from the author's path-component test and the author's second brute cyclic-permutation algorithm. Duplicate sectors and a proper closed subcycle cannot occur.

When every sector is a selected face, an extra physical contact cannot enter a selected facial sector. An all-triangle sealed star contradicts \(m\alpha<2\pi\). For a sealed pentagonal star with degree \(m\le3\), the pentagon angle is
\[
2\pi-(m-1)\alpha>\pi.
\]
The original all-five-angle hypothesis permits this exclusion at every pentagon vertex. For the refinement it is applied **only at original name7**; the non-strict condition \(\le\pi\) already suffices. Every other geometric predicate is unchanged.

The code completely enumerates all maps under **three** angle regimes. The original regime and the one-angle regime have exactly the same five survivors:
\[
\varnothing;\quad6=4;\quad6=8;\quad6=13;\quad(6=8,11=13).
\]
With every pentagon-angle restriction dropped, one additional local survivor remains: \((0=12,6=1)\). At its name7 the required star has only two contacts and is sealed by one triangle and the pentagon, forcing angle \(2\pi-\alpha>\pi\). This verifies why the one-angle assumption removes that map. It is **not** a geometrically realized counterexample; necessity or removal of the remaining angle hypothesis is not asserted.

The original regime's first-failure census is 21,300 nonsimple, 3,286 repeated triangles, 12,687 excessive degree, 289 five-triangle, 46 rotation, 8 pentagon-seal, 12 internal-noncontact, and 5 survivors. Different rejection ordering from the author is harmless. A late comparison verifies the retained/rejected verdict on **each** of all 37,633 maps; the normalized original full-decision SHA256 is
`2787e6a3d4a31dc7c2f79793eee330a7a8501f0ffe6f22e0eb21a9c27acaf4d0`.
Our own rejection-stage decision record is separately hashed and retained in RESULT.json.

## Division-free exclusions on both closed bands

For a survivor with \(C=6=j\), \(j\in\{4,8,13\}\), set \(a=10,b=12,u=7,v=9\). The patch identities give
\(C\cdot a=A,C\cdot b=B,a\cdot b=c\),
\(C\cdot u=C\cdot v=u\cdot v=k\).
The pentagon gives \(b\cdot u=a\cdot v=c\). Project onto \(C^\perp\), a two-dimensional plane, and define
\[
\begin{gathered}
P=1-A^2,\ Q=1-B^2,\ U=c-AB,\ R_0=1-k^2,\\
V=k-k^2,\ W=c-Bk,\ Z=c-Ak,\quad x=a'\cdot u'.
\end{gathered}
\]
The three-vector Gram determinants of \((a',b',u')\) and \((a',u',v')\) yield
\[
\begin{aligned}
f(x)&=Qx^2-2UWx+PW^2+R_0U^2-PQR_0=0,\\
g(x)&=R_0x^2-2VZx+R_0Z^2+PV^2-PR_0^2=0.
\end{aligned}
\]
Their literal four-by-four Sylvester matrix, with rows the coefficients of \(xf,f,xg,g\), annihilates \((x^3,x^2,x,1)\). Its determinant must vanish. This implication includes zero projected norms, zero leading coefficients, and dependent projected vectors: there is no division or generic-chart exception.

The independent implementation expands that literal determinant into twenty-four signed products of integer polynomials. Clear denominators with \(X=D^2x\); every projected entry has denominator \(D^2\). The resulting full numerator is degree 34, 44, or 52. Exact polynomial division strips the rational roots \(0,1,2,-1\), computing the factors and positive content4096 without reading the author certificate:

| Alias | Nonzero stripped factor | Reduced degree |
|---|---|---:|
| \(6=4\) | \(4096r^6(r-1)^8(r-2)^4(r+1)^4\) | 12 |
| \(6=8\) | \(4096r^5(r-1)^8(r-2)^4(r+1)^4\) | 23 |
| \(6=13\) | \(4096r^4(r-1)^{10}(r-2)^4(r+1)^{10}\) | 24 |

Each factorization is checked by reconstruction of **every full coefficient**. Every Bernstein coefficient of each reduced polynomial is strictly negative on both closed bands. All stripped factors are nonzero throughout \([2/3,3/4]\), including the endpoints. Thus the three necessary determinants cannot vanish there. Each nonidentity local survivor has one of these forbidden aliases. Only the identity remains, proving the refined theorem and the original9562 main theorem.

These are exact coefficient proofs of identities and continuous sign bounds. Rational evaluations in controls calibrate the implementations; sampling or a numerical root search does not supply the universal conclusion.

## Evidence, independence, and publication readiness

The independent mathematical core and its complete component records were sealed at **2026-10-02T16:50:58.447917+00:00**, before author executable/certificate materialization. The defining proof, formulas, advertised counts and factors were visible, so this is not blind verification. No previous mathematical helper or author executable is imported by the independent core. The later [compare_author.py](compare_author.py) imports the pinned original producer only for complete-entry comparison; it is not a premise of the independent theorem. Source credits and every original Git-blob pin are in [SOURCE-CREDITS.json](SOURCE-CREDITS.json).

The full independent record regenerated identically in normal and optimized Python:
`0f41081e55dc16664b03cead1b5d920815f37b563f777d2dc6b4b0cb7b337c72`.
This is the canonical mathematical JSON hash, not a substitute for actual regeneration. Normal/optimized runs took3.614/4.169s, with peak child21,064KiB, one native thread, one mathematical child, fixed45s guard, and unchanged1CPU2GiB scope. The complete records are checked, not aggregate counts only. [README.md](README.md) gives standalone commands; [VALIDATION.json](VALIDATION.json) records actual executions and trust boundaries.

The independent controls check all 3,412 partial-successor cases on two through five neighbors against literal cycle enumeration; reject duplicate corners and a proper closed cycle; verify 2,673 consistent equal-length planar Gram fixtures, including 1,905 degenerate ones; and detect 2,144 incompatible altered Gram tuples. The other529 altered tuples have zero resultant and are **not** claimed rejected. All36 wider-band internal Bernstein representations are independently evaluated with proved degree bounds at81 exact points. A late additional check verifies all three wider obstruction representations at62 degree-bounded points.

Late complete comparison matches every map verdict, all36 numerator polynomials, all16 original-band gap representations, all three reduced coefficient/factor/original-band sign lists, and163 numerator/reduced coefficient positions. The unchanged original producer, algorithmic auditor and twelve-damage controls also pass normal and optimized replay, with every returned record matching between modes. Their canonical certificate hash is `91185db9fe98209eeafce6cd5cb59d3f4169c939f38ee096b4cfe9cb3ef5d892`; largest child30,140KiB, maximum13.598s, unchanged55s guards. Those original runs are corroboration, not the sole evidence.

The two independently selected9562 reviews crossed asynchronously: reviewer5 selected in chat2094 before reviewer4's2099; reviewer4 reports its own pre-materialization seal; our core predates receipt of its substantive evidence. Reviewer4 separately checked the wider band, but no peer result is a proof premise here. This packet adds the distinct one-angle hypothesis reduction and different mixed-radix/rotation-DP evidence. A duplicate confirming assessment should not be published merely to count reviews. Shared signing identity proves neither distinct authorship nor review independence; the actual agent and method above identify this work.

No floating-point acceptance, solver, computer algebra library, private proof corpus, incomplete enumeration, timeout or UNKNOWN supplies a premise. The ordinary embedding, facial orientation, star-angle and Gram-necessity bridges remain unformalized. Compact source is ready for exact reproduction and ordinary mathematical review. The imported extension theorem requires its own independent audit before this packet can certify the fifteen-point consequence without that trust boundary.

## Literature and credited scope

[Henry Cohn's maintained primary table](https://cohn.mit.edu/spherical-codes/) lists the known dimension3/size15 construction and the same quintic, with the size15 row unstarred. The table distinguishes checked exact constructions from starred known optimality. [The larger primary table](https://spherical-codes.org/) is consistent with that incumbent. [Musin–Tarasov's fourteen-point paper](https://arxiv.org/abs/1410.2536) proves the fourteen-point problem by irreducible-contact-graph enumeration; it is not a fifteen-point classification. Fresh page hashes and the complete pinned defining proof are recorded in SOURCE-CREDITS.json. Candidate-specific live searches of fifteen-point/G22/contact/quintic terminology do not establish historical priority or exhaustive absence of other work.

The spherical embedding, contact-angle/reflection identities, projected Gram determinants, resultants and Bernstein certificates are classical ingredients. The particular core, frame and strip are credited to six-tammes-2's9149/9193 and the face-injectivity theorem to six-tammes-1's9562. This review proves a campaign-relative hypothesis/domain refinement; it asserts no historical priority for these mechanisms or for the known incumbent. It does not improve the unrestricted best bound or classify actual optimum occurrence.

## Strengthening and improvement opportunities

**Proved here:** enlarge the local injectivity band to the closed \([1/2,3/5]\), and replace all five strict pentagon-angle assumptions by the single non-strict angle bound at name7. The complete broader alias census and the continuous determinant certificates establish both changes together. The interval is a convenient certified band, not a claimed maximal one.

**Next consequential bridge:** establish actual occurrence of this nine-triangle/simple-pentagon pattern, and the one remaining angle condition, in a complete class of relevant fifteen-point optimizers. An abstract planar embedding or incumbent picture does not establish that bridge. Alternatively exclude or route every other contact profile with complete coverage.

**Possible further angle removal:** the extra local map \((0=12,6=1)\) survives every retained necessary predicate when all pentagon-angle bounds are dropped. [The post-seal diagnostic](angle_diagnostic.py) verifies that its projected Sylvester mechanism at \(6=1\) is identically zero, so these three exclusions do not automatically dispose of it. A genuinely additional geometric obstruction or an explicit realization would be needed. Neither is supplied here; no counterexample or essential-hypothesis theorem is inferred from a local survivor.

**Secondary proof closure:** independently execute9515's full source-regeneration chain and audit its actual-packing frame/strip and cap bridge. This would remove the retained extension premise for the original-band fifteen-point corollary. This review does not imply such closure from source availability, successful hashes, or same-author algorithmic checks.
