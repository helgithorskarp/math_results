# Signed rectangle graph and a failed strict-ascent repair

Theo, literature-researcher-4, 2026-10-05. New uniform partial author
reduction and finite mechanism failure, awaiting a separate different-
researcher check. Exact target410 remains unsolved. Neither claim is covered
by the earlier inflation/root/public/graph packets.

For p in S_n let G(p) have positions1..n as vertices, with edge i<j exactly
when no i<k<j satisfies min(p_i,p_j)<p_k<max(p_i,p_j). Mark that edge negative
when p_i>p_j and positive otherwise. Positions may equally be replaced by
their value labels; do not discard the signs.

These are prior algebraic/geometric objects. Adin–Roichman,
*On Degrees in the Hasse Diagram of the Strong Bruhat Order*, SLC53(2006),
B53g, primary https://www.mat.univie.ac.at/~slc/s/s53adinroi.pdf,
Observation1.2 and the Section3 graph definition, give the empty-rectangle
criterion for transpositions changing Coxeter length by1. Their Proposition1.9
states that the value-labelled strong descent set determines p. Keevash–Loh–
Sudakov, *Bounding the number of edges in permutation graphs*, EJC13(2006),
R44, primary https://people.maths.ox.ac.uk/keevash/papers/permutation-graphs-journal.pdf,
Definition1.1/Introduction, explicitly connects this graph with the
rectangle graph. These papers were freshly inspected; their prior objects
and bounds are credited. No novelty claim is made for the reduction below.

**Exact reduction.** A selected quadruple is boxed2143 if and only if its
vertices form a K4 in G(p) with exactly two negative edges. This gives a
bijection of selected quadruples, not only equality of total counts.

Proof. For the forward direction let values be a,b,c,d at ordered positions
i1<i2<i3<i4, with b<a<d<c. Every pair's open rectangle lies in the global
box. None of the other selected points lies in it: all selected triples
have order132 or213, never123 or321. The global empty-box condition excludes
every unselected point as well. Hence all six edges exist. Exactly the
pairs(a,b),(c,d) are negative.

Conversely, a K4 has no increasing or decreasing triple: the middle point
of such a triple would obstruct the edge between its outer points. The
four possible standardized patterns without either triple are2143,2413,
3142,3412 (direct finite enumeration of the24 orders). Their negative-edge
numbers are respectively2,3,3,4. Thus exactly two negative edges force2143.
For its values b<a<d<c, the six pair rectangles cover its whole open box.
In the left strip(i1,i2), pair(i1,i2) covers values(b,a) and pair(i1,i3)
covers(a,c). In the middle strip(i2,i3), pair(i2,i3) covers(b,c). In the
right strip(i3,i4), pair(i2,i4) covers(b,d) and pair(i3,i4) covers(d,c).
No unselected point can have a selected value or selected position, so the
strip boundaries introduce no exceptional point. Any unselected interior
point would obstruct one of these edges, contradicting K4. The box is empty.

The unsigned value-labelled graph alone loses avoidance: p=2143 and p=2413
both give the complete graph on values1..4, but only the first contains
boxed2143. Known extremal edge bounds also do not by themselves imply a
counting bound: high increasing band followed by low increasing band
classically avoids2143 while having quadratically many negative edges.
The missing full-target obligation is a multiplicity/encoding or repair
argument retaining the signed structure, not a claim that graph sparseness
or a generic K4-free condition settles growth.

**Tested full-target mechanism.** Let d_-(q) be the negative-edge count,
equivalently the strong Bruhat down degree. I tested the hypothesis that
every nonavoiding strict interleaving J_rho(pi) admits a swap of two even
entries that strictly increases d_-. If true, starting with any rho and
repeatedly choosing such a swap would terminate because d_- is an integer
bounded by binomial(2m-1,2). A terminal word would avoid by the hypothesis.
Taking a deterministic successful swap gives a recoverable length2m-1
completion for every pi and hence a_(2m-1)>=m!, solving the entire negative
target. This is a conditional argument; the ascent hypothesis is false.

The first failure occurs at pi=231,rho=12:

    J_12(231)=32541, d_-=4,
    J_21(231)=34521, d_-=4.

The first four points of32541 form boxed2143 (3,2,5,4). Its negative edges
at zero-based positions are(0,1),(1,4),(2,3),(3,4). The other word avoids
and has negative edges(0,3),(1,3),(2,3),(3,4). There are only two scaffolds
in S2, so the bad word is a global degree maximizer in its fixed-input
fiber and has no strictly improving even transposition. In particular,
every degree maximizer need not avoid. A weaker existence-of-an-avoiding-
maximizer hypothesis is not refuted by this tied example and is not proved.
Any further repair route needs control of degree plateaus or a different
invariant, rather than assuming strict descent/ascent.

`bruhat_completion_probe_v1.py` imports no author executable. On all5914
permutations through7 it compares complete boxed2143 sets with all signed
K4 selections,187824 quadruples in total. On all12164 transpositions of
permutations through6 it independently recomputes inversion lengths to
confirm the empty-rectangle signed cover criterion. All four K4 types occur
2555 times each in this finite domain, consistent with the existing boxed-
pattern mean identity; this is not promoted to a new distribution theorem.
The deterministic graph stream is
1428ff8ce38bc1c45fd5374cff4b140dca3b396096398e0e93d0cb3e2ece9249.
The ascent search stops after its first bad word, at9 input/scaffold pairs;
it does not extend a census after falsification.

Replay with CPython3.11+, standard library, one process/thread:

    python3 -B bruhat_completion_probe_v1.py --output /tmp/bruhat-probe.json

Evidence `bruhat-completion-probe-v1.json`:1.479seconds,17956KiB peak RSS.
These controls establish finite alignment, while the separate written
geometric argument gives the stated uniform reduction. A different reviewer
must check both before any publication. Source Conjecture7.4 permits any
rho and is not contradicted; the full growth problem is unchanged.
