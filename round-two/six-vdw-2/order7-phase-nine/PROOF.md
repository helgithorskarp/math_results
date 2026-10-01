# Phase weights 8 and 36 are excluded for order-seven F617 templates

**six-vdw-2, researcher; 2026-10-01.** An exact computer-assisted lemma.
Generation and definition checking use separate author implementations.
Independent peer review and proof-assistant formalization are unclaimed.

## Statement and imported results

Let H=<3^88> in F617*, of order seven. An admissible template is a binary
coloring c of F617*, invariant under H, with no monochromatic seven-term
field arithmetic progression a+j d, 0<=j<=6, with d nonzero and every term
nonzero. Write y_i=c(3^i), indexed modulo 88, and
f_i=y_i XOR y_(i+44), indexed modulo 44. Set K=sum f_i.

**Lemma.** No admissible template has K=8 or K=36. Consequently every
admissible template with nonconstant phase has **9<=K<=35**. The same
band holds for every nonquadratic admissible template, using the previously
published constant-phase classification. For these nonconstant-phase
templates, the sets of nonzero x satisfying c(x)=c(-x) and c(x)!=c(-x)
both have cardinality in **126..490**.

The ordinary quadratic-residue coloring and its complement have K=0 and
remain admissible. This result leaves existence of a nonquadratic H7
template, complete H7 classification, the interval-3704 construction,
and unrestricted W(2,7) unresolved.

The proof explicitly imports four published results:

| Input | Used conclusion | Source commit | Graph |
|---|---|---|---|
| [Color windows](../order7-geometric-cut/PROOF.md) | Every seven consecutive y positions are mixed | e6f1eb9d87d194cf901d812818ad6fd2427473d3 | 8664, bafkreidhgfm6i2idrez6y7ix2qmi34ehvzpkbtjfzfcpxp6trh6v2vyfga |
| [Phase windows](../order7-antipodal-geography/PROOF.md) | Every eight consecutive positions of a nonconstant phase are mixed | 84f623e07584d9b1dcfa9076d6bdd26ddb0e9b24 | 8787, bafkreifqgfqv2x2gbckthkhrq4rqmjzrvqxe6h6ljlix3re6dy4gmhucbe |
| [Endpoint spacing and root57](../order7-cluster-and-root57/PROOF.md) | At K=8/36 a majority gap is at most one; every root57 color-eight window is mixed | 7880c843e883567f0af6188813cd5a056dbf3e17 | 9069, bafkreicvbbcltye7v6jdts7hgpyn27w5xjd5d5rq3lxv2uua24e3o2bnwe |
| [Previous endpoint exclusion](../order7-phase-endpoints/PROOF.md) | Nonconstant phase satisfies 8<=K<=36; nonquadratic templates have nonconstant phase | 83563a2f816b1b777e9fef89bc81fdf188d8ad53 | 9015, bafkreigw2orvnxlvoj2hk46mrtyvxhob4ctqdns5qxbz2gmzzp4xsyb3aq |

Their proof bytes and required software are pinned in
[SOURCE_PINS.json](SOURCE_PINS.json). The nonquadratic corollary inherits
the old rigidity and identically-one-phase exclusions through these cited
inputs; the eighteen new refutations do not independently reprove them.

## A large majority gap must exist

At K=8 or K=36, put b=0 or b=1 respectively. There are eight minority
positions with phase 1-b. Their successive positive forward distances
sum to 44. Let g_0,...,g_7 be the intervening majority gaps: each distance
is g_j+1, sum g_j=36, and the phase-window input gives g_j<=7.
The endpoint-spacing input gives min g_j<=1.

If max g_j<=5, a zero gap is impossible, since the remaining seven gaps
would sum to at most 35. A gap of one forces every other gap to equal
five. Thus the only possible rooted profile, up to cyclic rotation, is

    (1,5,5,5,5,5,5,5).

Anchor a minority at zero. Its positions are 0,2,8,14,20,26,32,38.
For each b the corresponding model keeps all 44 lower color orientations
and substitutes the upper colors by y_(i+44)=y_i XOR f_i. Both 44-variable
models strictly refute. Hence max g_j is six or seven.

## Majority gaps of seven are impossible

Suppose a maximal majority run has length seven. Rotate its first
position to zero, giving f_0=...=f_6=b and f_43=f_7=1-b.
There are N=35 free phase positions, with exactly six further minority
values. Keep all 44 lower orientations, N upper orientations, and N
phase variables with the exact XOR relation. No remaining color
orientation is identified with another.

Seven-level prefix thresholds count the six remaining minorities:

    C_(i,k) <=> C_(i-1,k) OR (m_i AND C_(i-1,k-1)),
    C_(i,0)=true, C_(i,k)=false for k>i,
    C_(N,6)=true, C_(N,7)=false.

Here m_i is the signed minority predicate, f_i when b=0 and 1-f_i when
b=1. Four simplified clauses encode each equivalence. Induction on i
proves that C_(i,k) is the threshold for the first i inputs. There are
7N-21 counter cells and 23+9N=338 total variables. Both b models
strictly refute. Therefore max g_j=6.

## Every gap of six must be followed by a gap of zero

Choose **any** majority run of six and rotate it to positions 0,...,5.
Then f_43=f_6=1-b. Let j be the next minority position after six.
Since every majority run has length at most six, j lies in 7,...,13.
For j>=8 fix f_7,...,f_(j-1)=b and f_j=1-b. There are N=42-j free
phase positions and exactly five further minority values.

The twelve models, j=13,...,8 and both b, use six-level prefix thresholds
with final units C_(N,5) and NOT C_(N,6). Their dimensions are
29+8N=261,...,301. Each includes the global prohibition of an all-majority
seven-position phase window. This restriction is imposed **only for the
majority value**; a seven-position minority run is not erroneously cut.
Both signs of every eight-position phase window remain necessary inputs.
All twelve models strictly refute, so j=7.

Because the chosen run of six was arbitrary and scalar multiplication
permits its normalization, this proves the directed cyclic rule

    g_i=6 implies g_(i+1)=0.

Reflection and exchange of the two phase values are not symmetry
quotients. Both phase backgrounds are checked separately.

## The directed rule leaves one phase orbit

Let z count zero gaps and k count gaps of six. Since max g=6 and sum g=36,
there is at least one gap of six. Every such gap has a distinct following
zero, so 1<=k<=z. Also 36<=6(8-z), giving z<=2.
If z=2, all six positive gaps must be six, contradicting k<=z.
Thus z=k=1. The other six gaps are at most five and sum to 30, so each
equals five. Up to cyclic rotation, the unique directed profile is

    (6,0,5,5,5,5,5,5).

The anchored minority positions are 0,7,8,14,20,26,32,38. Both phase
backgrounds again yield 44-variable models retaining all orientations;
both strictly refute. This completes the exclusion of K=8 and K=36.

The independent profile audit supplies a finite control of this written
counting argument. It places twelve indistinguishable deficit units into
eight slots, enforcing 0<=u_i<=6 for u_i=6-g_i. It obtains 44052 possible
rooted gap tuples, exactly C(19,7)-8*C(12,7). Applying the maximum-gap
and directed-following conditions leaves precisely the eight rotations
of the stated profile. Each fixed phase profile has 44 distinct scalar
rotations. All 44 color orientations remain free even if a phase were
periodic; no orientation invariance is inferred from phase periodicity.

## Exact model and certificate boundary

Every model contains both signs of every actual admissible field AP
color clause, imported color-seven windows and root57 color-eight
windows. The latter use exponent step 19 because log_3(57)=19 modulo 88.
Counter models also include the exact XORs, phase-eight windows and
the specified majority run bound. All cases use global color exchange
only to set y_0=0, which preserves f.

The producer uses the pinned log/scale AP generator. Separate auditors
construct literal H-cosets and visit all 617*616 ordered field pairs
(a,d) with d nonzero. Exactly 4312 APs pass through zero; the other
375760 are retained, with 26488 distinct signed supports. Audits compare
the **entire** clause multiset, header, units, free domain, phase semantics
and fixture hash. No test of hashes or solver statuses replaces this
literal comparison. The imported literal checker also checks both QR
orientations as positive controls.

The counter auditors derive labels analytically, account for every gate
clause by its newest output, and check the complete local truth relation.
Small exhaustive controls verify prefix thresholds and exact counts.
All definition audits and strict proof checks run in normal and optimized
Python; explicit exceptions remain active under `-O`.

| Group | Cases | Variables | Checked RUP additions | Propagation hints |
|---|---:|---|---:|---:|
| Fixed gap profile (1,5,...,5) | 2 | 44 | 2786 | 21018 |
| Maximum majority run seven | 2 | 338 | 64341 | 1096528 |
| Nonadjacent following minority | 12 | 261..301 | 117223 | 1926682 |
| Forced directed gap profile | 2 | 44 | 2660 | 18630 |
| Total | **18** | | **187010** | **3062858** |

[EXPECTED.csv](EXPECTED.csv) records exact per-case CNF/proof hashes and
counts. The strict positive-only RUP-LRAT kernel checks actual unit
propagation with live clause IDs and an empty conclusion. It rejects
unsupported RAT, missing/deleted hints, malformed domains and incomplete
traces. Its provenance is graph 7835,
bafkreidlaq5uknmu22tpadoyvxe537hkgubmpyhynlekstrengbvtjlvti;
the exact imported source bytes are pinned. Native CaDiCaL195 and
drat-trim are untrusted proof proposers. Omitted models and proof corpora
regenerate outside Git.

An earlier unsplit maximum-six endpoint model returned UNKNOWN at the
existing 50000-conflict cap. That result establishes no exclusion. The
new complete following-minority split and directed-profile reduction
use different models; no identical UNKNOWN model was retried and no
resource limit was raised. Remaining trust includes the cited results,
written normalization and gate induction, exact checker/source and
Python/compiler runtimes. This is not a formalization or an external audit.

## Consequences, context and remaining frontier

Combining the new endpoint exclusion with the imported 8..36 band gives
9..35. Each phase position represents a J=H union(-H) coset of 14
nonzero points, proving the two cardinality ranges 126..490.
The next unresolved endpoint weights are K=9 and K=35.

[Monroe Tables 1 and 2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
give the inspected symmetric two-color/seven-term seed >3703 and prime
617. Monroe places length before color count, reversing this packet's
W(colors,length) notation. The [author's repository](https://github.com/hmonroe/vdw),
[Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf),
and [Heule et al., Section 4.3](https://www.cs.cmu.edu/~mheule/publications/JOC_08_03_A01.pdf)
provide construction and search context. Primary sources were rechecked
2026-10-01. No verified later interval record is used; a bounded check
does not prove its absence. The asymmetric three/seven problem is different.
Novelty is asserted relative to the inspected campaign phase frontier,
not as an exhaustive historical-priority claim.
