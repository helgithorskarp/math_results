# A permissive three-AP obstruction in the period618 phase family

Actual author: six-vdw-1, researcher. This is an exact construction
restriction for symmetric two colors/seven terms W(2,7).

For zero-based t define

    c_phi(t+1) = f(t mod6 - phi(t mod103)),
    f(z) = 1[ (z mod6) >= 3 ],   phi : F103 -> Z6.

The word has period618 and satisfies c(n+309)=1-c(n).
Write h_i=c(i) for1<=i<=309.

## The primary obstruction

Let A={2,45,73,77,79,81,83,85} and
B={3,32,36,55,69,95,98,102}. Suppose

    phi(A) subset {2,3,4},   phi(B) subset {5,0,1}.

Every r in A has color1 at y=1 and color0 at y=4. Every r in B
has color0 at y=1 and color1 at y=4. Here x=(n-1) mod103,
y=(n-1) mod6. These colors are fixed uniformly over every allowed phase,
not only at the reference word used to discover the pattern.

Consider the following three nonconstant integer seven-term APs:

| start | difference | terms |
|---:|---:|---|
|305|276|305,581,857,1133,1409,1685,1961|
|209|93|209,302,395,488,581,674,767|
|86|204|86,290,494,698,902,1106,1310|

In the first row, all terms except581 have color1. Its nonmonochromatic
condition is h_272=1, because c(581)=1-h_272.
In the third row, all terms except1106 have color1. Its condition is
h_179=1, because c(1106)=1-h_179.
In the second row, all fixed terms have color0. Its only unfixed terms are
c(488)=1-h_179 and c(581)=1-h_272. Its condition is

    not h_179 or not h_272.

The two forced ones contradict this condition. Thus at least one displayed
AP is monochromatic. This proves the obstruction with all other87 phases
arbitrary. Each of16 restricted phases has three permitted values, so the
excluded domain contains exactly3^16*6^87 assignments. This is a domain
cardinality, without a claim about overlaps with transformed domains.

The reconstructed CNF is

    h_272,
    not h_179 or not h_272,
    h_179.

Its positive-RUP certificate is `4 0 1 2 3 0`. The direct checker derives
these premises from the seven integer terms and checks all8 assignments
to their free bits. The reference halfword is used only to reconstruct
the permissive color restrictions; the displayed proof needs no large
model, search completeness assumption, or solver verdict.

## Transport to63036 distinct forbidden domains

A length3704 AP-free prefix of a period618 word is cyclically AP-free.
Indeed any cyclic start a in{0,...,617} and nonzero step d mod618 can be
represented after optional reversal by a positive integer step
min(d,618-d)<=309. Choose the start representative in{0,...,617}; the
resulting seven integer positions are at most

    617+6*309+1=2472<3704.

Conversely every integer AP in the3704 prefix has step at most617, so a
cyclically AP-free period618 word gives an AP-free prefix. Nonconstant
integer progressions remain nonconstant even if their cyclic residues repeat.

For any alpha in F103*, beta in F103, epsilon in{1,-1}, and k in Z6,
the map

    phi'(x)=epsilon*phi(alpha*x+beta)+k

preserves cyclic AP-freeness. To see this explicitly, take a CRT unit m
with m mod103=alpha and m mod6=epsilon. Choose a CRT translation q with
q mod103=beta and q mod6=e, where e=-k for epsilon=1 and e=k+2 for
epsilon=-1. The elementary identities

    f(y+e-p)=f(y-(p-e)),
    f(-y+e-p)=f(y-(e-p-2))

show that c_phi'(t+1)=c_phi(m*t+q+1), with periodic interpretation.
The affine permutation t->m*t+q sends nonzero cyclic steps to nonzero
cyclic steps. Its inverse is of the same form. The interval bridge then
gives the claimed preservation at length3704.

Equivalently, a forbidden domain on support S=A union B transports to
support a*S+b with permitted phase sets epsilon*P_r+k. The inverse field
affine map gives the preceding action on full functions. Thus every such
transported domain is forbidden.

The support S has trivial affine stabilizer. This finite fact is checked
over all102*103=10506 field affine maps. A second complete check sends
the ordered anchors2,3 into all16*15=240 distinct ordered pairs in S,
which determine every possible stabilizer map. Both return only(1,0).
Consequently there are10506 distinct affine support images.

Each of the two permitted phase sets is invariant under p->-p. Their
simultaneous phase-domain stabilizer is exactly(1,0),(-1,0), giving six
distinct phase variants. The entire support can be read from the locations
whose allowed set has size3 rather than6, so two domains with different
supports cannot coincide. The number of distinct forbidden domains is
therefore10506*6=63036. Each has3^16*6^87 assignments. No union cardinality
or global exclusion follows. The checker also verifies all432 elementary
color-identity cases, all204 CRT unit multipliers, and a deterministic hash
of the complete63036-domain stream; the orbit corpus is not stored.

## The secondary certificate

`secondary.json` contains22 actual integer APs and a positive-RUP proof
with two additions and23 propagation hints. It constrains the33 residues

    {22,23,29,30,31,36,38,39,41,43,45,49,51,52,54,55,56,
     59,61,64,68,69,73,76,79,81,85,86,88,92,94,98,102}.

For each constrained residue, the checker collects only the term colors
appearing in these22 APs and enumerates the phases preserving those colors.
No other bits in that column are fixed. The resulting permissive sets are
reported in build/result.json. All70 other phases are arbitrary.

Substituting the fixed term colors makes each AP's NAE condition exactly
one Boolean disjunction. The checker reconstructs those22 clauses from
the actual integer APs, checks all122 free-term truth assignments, and
independently verifies the two RUP additions ending in the empty clause.
This excludes the stated product of permissive sets. It also excludes the
subfamily where the33 phases equal the supplied reference exactly.

The first exploration used66 free columns with37 phases fixed. Only33
fixed columns appeared in its independently checked proof; the remaining
four could be released without changing any proof premise. The final direct
certificate contains only the22 APs and the two proof lines. Its validity
does not depend on the original solver trace or the full projection.

Both negative results have explicit quantified domains. No minimality,
unrestricted nonexistence, new length3704 coloring, improved W(2,7) bound,
or exact value is established. Written mathematics and finite independent
Python checks are the trust boundary; no external peer review or formal
proof assistant is claimed.
