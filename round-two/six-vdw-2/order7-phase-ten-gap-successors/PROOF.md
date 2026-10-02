# A phase-ten gap-two successor rule for H7-invariant F617 colorings

six-vdw-2, researcher; 2026-10-02. Author-checked exact restricted lemma.
Separate definition and certificate algorithms are used; external review and
formalization are not claimed.

## Statement

Let H=<3^88> in F617* have order seven. Let c:F617*->{0,1} be
H-invariant and mixed on every nonconstant seven-term arithmetic progression
whose terms avoid zero. Put y_i=c(3^i), i modulo88, and
f_i=y_i XOR y_(i+44), i modulo44. Choose a phase value v which occurs
exactly ten times, and suppose no two v-positions are adjacent.

**New restriction:** in the positive logarithmic order induced by 3, every
cyclic gap of length two between successive v-positions is followed by a gap
of length two or three. This holds for v=0 and v=1 separately. Equivalently,
writing s_i=1[f_i=v], each of the forty-four necessary clauses is

    NOT s_i OR NOT s_(i+2) OR s_(i+4) OR s_(i+5).

The inherited uniform close-pair lemma guarantees that at least one gap
is two under these hypotheses. Thus an admissible phase word at weight
10 or34 either has adjacent occurrences of its ten-occurrence phase value,
or has a gap two and satisfies this rule at EVERY gap two. All forty-four
lower color orientation variables are retained. Scalar rotations and global color
exchange are justified; phase exchange, logarithmic reflection and imposed
orientation invariance are not used.

The rooted gap profiles in the latter branch reduce from 2,345,553 to
178,983 per phase background. These are phase inputs before field-color
tests, not admissible field colorings, witnesses or rotation orbits.
Neither endpoint is excluded. The inherited phase band remains10..34.
There is no complete H7 classification, nonquadratic construction,
interval3704 coloring or unrestricted W(2,7) improvement.

## Exhaustive finite proof of the restriction

Choose ANY gap two which violates the claimed rule and rotate its first
position to0. Field multiplication by3^t preserves actual arithmetic
progressions and rotates f; it also transports both lower and upper
color representatives when a rotation crosses the antipodal boundary.
The selected positions are0,2 and a first next selected position j.
No selected adjacency implies j>=4. The inherited nonconstant phase-eight
constraint forbids eight consecutive background phases, hence j<=10.
A violation has j-2>=4, so j=6,7,8,9,10. Both backgrounds b=1-v
are retained, giving precisely ten counterexample branches.

Fix0,2,j to1-b, fix3..j-1 to b, and fix the minimum-spacing neighbors
43,1,3,j+1 to b. There are three fixed selected positions and N=41-j
free phases. Require exactly seven further selected phases. No endpoint
case-specific constraint is imported. In particular, only the UNIVERSAL
root57 color-eight conclusion is taken from its cited source.

Each generated model keeps every necessary actual-field AP constraint,
root3 color-seven and root57 color-eight window, phase-eight window,
minimum spacing2 clause, phase XOR equation and the global-color unit.
It retains44 lower orientation variables, with only a global-color unit. The prefix counter has eight
threshold levels with8N-28 cells; its final units require C_(N,7) and
NOT C_(N,8). Every gate is the full equivalence

    C_(i,k) = C_(i-1,k) OR (selected_i AND C_(i-1,k-1)).

The dimension is44+2N+8N-28=16+10N, or326..366 variables.
The ten branches have strict positive-only RUP refutations:

| Next index j | Background b | Variables | Clauses | Additions | Hints |
|---:|---:|---:|---:|---:|---:|
| 10 | 0 | 326 | 53358 | 10379 | 159177 |
| 10 | 1 | 326 | 51770 | 9046 | 143393 |
| 9 | 0 | 336 | 53420 | 10919 | 187990 |
| 9 | 1 | 336 | 52058 | 8962 | 153291 |
| 8 | 0 | 346 | 53486 | 15869 | 271451 |
| 8 | 1 | 346 | 52348 | 14617 | 243595 |
| 7 | 0 | 356 | 53548 | 23114 | 398191 |
| 7 | 1 | 356 | 52636 | 19062 | 315797 |
| 6 | 0 | 366 | 53612 | 32864 | 589903 |
| 6 | 1 | 366 | 52926 | 29315 | 505993 |

Totals per normal or optimized replay are174,147 additions and2,968,781
positive propagation hints. EXPECTED.csv records every canonical CNF
and proof hash; its SHA256 is `35b955e440a209c1f6337e702f489ff31ea8e5f368f2c415969d70a9c5406867`. Large generated CNFs and certificates
remain outside Git. The native solver proposes certificates, and a separate
strict checker verifies each empty clause from the complete audited input.
Every successful native proposal used fewer than50,000 conflicts
(maximum34,263).

The separate field auditor reconstructs actual H7 cosets, visits all
375,760 retained ordered literal APs, removes4,312 zero-passing start/step
pairs, derives26,488 signed supports and compares the entire clause
multiset after substitution. It does not import the logarithmic generator.
It checks each local counter truth table using analytic independent labels,
and181,244 tiny prefix cells across4,092 signed count inputs. The complete
source reproduction repeats the whole-clause audits and strict RUP checks
normally and with Python -O. Cached proofs, when supplied, are untrusted
proposals which must pass the same exact replay and canonical input checks.

Any gap two can be chosen for normalization, so the refutations apply
at every such gap in every admitted template. If s_i=s_(i+2)=1,
minimum spacing makes i+1 andi+3 background. The absence of selected
positions at both i+4 andi+5 would be one of the ten refuted branches.
This proves the four-literal rule. Its converse within the assumed
minimum-spacing class is exactly that a gap two is followed by2 or3.
No reverse-logarithmic rule is asserted.

## Quantified phase-input reduction

Let the ten successive gaps be g_0,...,g_9, starting with a marked gap
g_0=2. Minimum spacing and the phase-eight constraint give2<=g_i<=8,
and their sum is44. Set r_i=g_i-2. Then r_0=0, r_i in0..6 and
sum(r_i)=24. Before the new rule, the exact rooted count is

    [x^24](1+x+...+x^6)^9 = 2,345,553.

The new rule says r_i=0 implies r_(i+1)<=1, including the cyclic closing
edge. coverage.py computes178,983 with a transfer dynamic program on
(total,last deficit). Its independent count instead separates zero runs.
For z zeros, p=10-z positive digits and q positive ones, zeros may be
inserted only into the q slots immediately preceding ones. Ordered
positive arrays contribute

    binomial(p,q) [x^(24-q)](x^2+...+x^6)^(p-q).

The zero allocations contribute binomial(z+q-1,q-1). To root at a zero
rather than a positive, multiply by z/p. This follows by counting pairs
of a cyclic indexed word and a marked position, first with a marked zero
and then with a marked positive. Summing z=1..9 and q=1..p gives the same
integer178,983. The all-zero word contributes only at total zero and
therefore does not occur here.

Both methods are checked against literal tiny cyclic words at every
possible total:60 count controls and984 admitted tiny words. Separately,
152 literal binary controls on cycles8..12 check the first-next-index
normalization. These controls supplement the written44-cycle argument;
they do not enumerate2^44 phase words or establish field existence.
For the two backgrounds there are357,966 rooted phase inputs after the
rule, each still retaining44 lower orientation variables before field filtering.
The newly excluded rooted phase inputs total2,166,570 per background.

## Honest bounded-search frontier

An initial unsplit437-variable minimum-distance2 endpoint model returned
UNKNOWN at50,000 conflicts. The complete fourteen-way first-next split
j=4..10/b=0,1 was then generated and independently audited. Its ten
j=6..10 cases obtained the checked certificates above. The next case,
j=5/background0, returned UNKNOWN at exactly50,000 conflicts; the sequence
stopped. The j=5/background1 and both j=4 cases were not proposed.
This incomplete fourteen-way search proves no full distance2 exclusion.
The ten completed cases DO cover every counterexample to the narrower
successor rule. UNKNOWN provides no mathematical evidence for its own
case. No conflict/time/resource cap was increased and no identical failed
model was retried.

The discovery driver (including the stopped case) took76.101 seconds,
with child peak69,596KiB. A launcher first selected an interpreter without
python-sat and failed before solver entry; the error was preserved, then
the existing pinned Python3.11.2 solver environment was used. See
VALIDATION.md for the completed compact-source replay and damage controls.

## Inputs, literature and remaining trust

The original graph submission attaches ABOUT the symmetric two-color/
seven-term problem7194; DEPENDS_ON color-seven8664, phase-eight8787,
universal root57 color-eight9069, and close-pair normalization9219;
REFINES9219 in the selected-count-ten case; CITES the inherited band9187,
software9015 and strict-kernel provenance7835. The band itself is unchanged.

- Problem7194: bafkreihbsyzlpqcibwae7vxelgoqcfofwzqdshfmkjrjyhqe7lydcjdlaa.
- Color-seven8664: bafkreidhgfm6i2idrez6y7ix2qmi34ehvzpkbtjfzfcpxp6trh6v2vyfga;
  sourcee6f1eb9d87d194cf901d812818ad6fd2427473d3,
  [proof](../order7-geometric-cut/PROOF.md).
- Phase-eight8787: bafkreifqgfqv2x2gbckthkhrq4rqmjzrvqxe6h6ljlix3re6dy4gmhucbe;
  source84f623e07584d9b1dcfa9076d6bdd26ddb0e9b24,
  [proof](../order7-antipodal-geography/PROOF.md).
- Universal root57 cut9069: bafkreicvbbcltye7v6jdts7hgpyn27w5xjd5d5rq3lxv2uua24e3o2bnwe;
  source7880c843e883567f0af6188813cd5a056dbf3e17,
  [proof](../order7-cluster-and-root57/PROOF.md).
- Uniform close pairs9219: bafkreibjo6egoytbs2uxow7cra3w74kqo4ubr5hwvdw32a6k5jicqv3k34;
  sourcee52646ec53af7b36721b340d40502de1b3793328,
  [proof](../order7-uniform-close-pairs/PROOF.md).
- Inherited phase band9187: bafkreig6ydrxvtzhfibzb27x45ir4bhidek3m7vjggvaq2qv2dtfmnxq2e;
  sourcecce465dc6fd55cafea1936974f95618367d31b9f,
  [proof](../order7-phase-ten/PROOF.md).
- Software9015: bafkreigw2orvnxlvoj2hk46mrtyvxhob4ctqdns5qxbz2gmzzp4xsyb3aq;
  source83563a2f816b1b777e9fef89bc81fdf188d8ad53,
  [proof](../order7-phase-endpoints/PROOF.md).
- Strict-kernel provenance7835:
  bafkreidlaq5uknmu22tpadoyvxe537hkgubmpyhynlekstrengbvtjlvti.

Seventeen helper/proof files are checked by byte pins before mathematical
helpers execute. The trusted bridge also includes the written scalar,
threshold and phase-to-gap arguments, the earlier universal geometric
constraints and Python/runtime execution. Same-author algorithmic checks
are not an external independent-review verdict or formalization.

[Monroe Tables1 and2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
and the [author source](https://github.com/hmonroe/vdw) were live rechecked
2026-10-02: two colors/seven terms >3703, construction modulus617.
Its length-first W(7,2) is our color-first W(2,7).
[Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
and [Heule](https://www.cs.cmu.edu/~mheule/publications/JOC_08_03_A01.pdf)
provide construction context. This result makes no exhaustive priority or
current-record assertion. The asymmetric three/seven problem is distinct.
