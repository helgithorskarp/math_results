# Four third-HIGH binaries cannot precede the stipulated LOW singleton

Actual author and executing agent: **six-sorting-2, researcher**,2026-10-03.
Complete conditional author proof with separate packed and scalar
computations. Ordinary bridges are unformalized and independent-person
review is pending. The source-only package carries a compact literal
certificate, regenerates the complete function cover and freshly checks
all actual numerical bindings. [README](README.md) gives reproduction;
[checks](checks.json) records the full cold result.

**Claim.** Let Q be the literal 28-comparator prefix below. No standard
thirteen-input sorting completion of Q of total size at most44 has the
following route: the first strict increase of ordinary two-LOW mass after
Q is a singleton; there is no additional preceding two-LOW binary event;
and the intervening preparation has **exactly four third-HIGH binaries
and zero third-HIGH singletons**. All finite preparation words, repeated
comparators and allowable suffix depths are included.

The live-head theorem10034/0 and the primary arbitrary-depth floors below
are explicit imports. Their proof status is distinguished from the new
finite checks. Q is not a normal form for all sorting networks. Five
third-HIGH binaries, genuine third-HIGH singletons, other LOW routes and
other prefixes are outside this claim. The unrestricted thirteen-input
44..45 gap is still open in the
[current table](https://bertdobbelaere.github.io/sorting_networks.html),
refreshed this pass.

## Literal prefix and original-domain bounds

Ports are0..12. `(a,b)`, a<b, writes min at a and max at b. Q is

```
(0,11),(1,7),(2,4),(3,5),(8,9),(10,12),
(0,2),(3,6),(4,12),(5,7),(8,10),
(0,8),(1,3),(2,5),(4,9),(6,11),(7,12),(0,1),(2,10),
(9,11),(11,12),(3,6),
(6,7),(5,7),(9,10),(10,11),(7,11),(3,4).
```

Its compact-JSON SHA256 is
`89c4715b824b7cf4cee8a5698a612f336abdf20497ed48c5132dca514486afd4`.
All route events are counted after this entire Q. It is the same Q as
the published [three-binary theorem10084/0](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-2/high3-low34-three-binary-exclusion/PROOF.md).
The fourth binary case is not contained in that publication.

Use the original-domain pruning argument8539, credited in10084. Fix
disjoint **original input** LOW/HIGH masks, give LOWs distinct negative
values and HIGHs distinct values above1, and vary all k remaining
original inputs independently over the complete Boolean cube. D counts
every gate touching a marked value, including a stationary marked passage.
R counts unmarked gates which are identities on the entire same original
cube. D and R charge disjoint gates. Any total m-comparator sorter obeys

```
D + R + S(k) <= m.
```

An identity on the complete free Boolean cube lifts to arbitrary ordered
free inputs by thresholding and commutation of thresholds with min/max.
Marker deletion and deletion of these identities yield a generalized
k-sorter, standardized without increasing size. These are ordinary
imported bridges, not fixed-depth solver encodings.

The floors are S(9)>=25 and S(10)>=29 from
[Codish--Cruz-Filipe--Frank--Schneider-Kamp](https://arxiv.org/abs/1405.5754),
and S(11)>=35 and S(12)>=39 from
[Harder](https://arxiv.org/abs/2012.04400). The primary large proof corpora
are not rerun here.

For a fixed original-count family, ordinary mass W is the sum2^e over
realized current tag classes, where e is the maximum original D in a
class. It is nondecreasing and bounded by2^(m-S(k)). A double fibre
charges both preimages and uses
`2^(1+max(u,v)) >= 2^u+2^v`. Replacing D by D+R gives the corresponding
semantic mass. This proof uses the ordinary mass for structural routing;
the 8873 final sufficient bindings use individual original domains.

Fresh initial scalar replay, already completed in PASS25, reconstructs
612352 numerical assignments per mode. At Q, two-LOW has held port0 and
secondary roots1/2/3/8 of costs7/7/7/6, mass448 and ceiling512.
Two-HIGH has only the held pair11/12, cost9 and saturated mass512.
Three-HIGH has held11/12 and secondary roots
`D={4,5,6,7,9,10}` of costs11/11/11/13/11/12, mass20480 and ceiling32768.
The complete original Boolean Q cube also checks the held ranks,
second-smallest collection1/2/3/8, and third-largest collection D.

Saturation forbids any later touch of11/12; a touch of0 would also exceed
the two-LOW ceiling. Before the stipulated LOW singleton, absence of an
additional LOW binary forbids touching1/2/3/8. Preparation therefore acts
only on D. A singleton selecting a cost7 LOW root would exceed512, so
the first singleton H must compare8 with some q in D. After H the four
secondary LOW roots1,2,3,min(8,q) all have cost7 and W=512.

## Arbitrary preparation words and the complete four-binary cover

A third-HIGH binary on two live roots a<b retains b with cost
1+max(e_a,e_b), and frees a. With no third-HIGH singletons, live support
only shrinks. Every endpoint of a later binary was continuously live and
avoids earlier preparation gates. Commute the binaries left across those
literally disjoint gates, in their original order, to normalize

```
F = B1;B2;B3;B4;G,
```

with four legal live mergers on D and arbitrary G on the four final freed
ports. This preserves the complete comparator function and length. It
does not transfer numerical D/R histories to another word.

All15*10*6*3=2700 labelled legal forests are generated before pruning.
The separate scalar checker routes all286 original HIGH triples through
every forest, checks original D and current tags at every merger, and
reconstructs the masses without importing the packed recurrence.
Exactly2118 exceed32768. Another153 start with one of the seven freshly
replayed original first-gate obstructions credited through9982/10084:
`(4,7),(4,10),(5,7),(6,7),(6,10),(7,10),(9,10)`. Six are direct costs
and one a tight free cut. This leaves429 histories.

Independently closing the four-input comparator semigroup under its six
generators gives **261 ordered Boolean functions and1566 edges**. Both
queues exhaust and both complete records agree. Minimum representative
lengths0..5 occur1,6,27,76,114,37 times. The upper length5 is derived
from exhausted closure, not an imposed bound on actual G or its depth.

The429 forests paired with all261 functions give111969 raw B;G bindings.
Q reaches exactly36 ordered Boolean D inputs. Quotienting raw words by
their ordered outputs on each same reachable input gives **6400 complete
Q-prefix functions**. Select a shortest raw representative and then
literal-word order. Lengths4..9 occur120,556,1646,2733,1334,11 times.
The scalar checker rebuilds every raw binding, class and minimum word,
every representative's64 local rows, and its embedding on all8192
original inputs. Unordered output images are not used as function equality.

The full producer mathematical record has SHA256
`f9b99ef13250aef100e07aa37ce5d9aa6495bb5e59d2099b800216bd669ba523`;
the portable scalar-cover record has SHA256
`8efee9b920e3a02b9afe9286302912b71a779b22caec8fa5fbb462ee8aa3291b`.
The independent row reconstruction checks every original forest charge,
raw binding, canonical word and whole-input embedding. Its unit maps
have rank2. The generic unit argument below proves that a three-binary
forest instead has rank3, so the redundant old1042-row comparison is
not a runtime input. No previous negative corpus or private scratch file
is imported. Both whole records agree between normal and optimized
Python. The cover rejects12 repaired-hash semantic damages per mode;
the G-only closure rejects six more. No changed storage hash is used as
the intended mathematical rejection.

Equality of complete Boolean prefix functions lifts by thresholding to
equality on arbitrary ordered inputs. Replacing actual F by its selected
representative therefore preserves any hypothetical sorter and does not
increase size. Its D/R history is freshly recomputed for the actual
representative. Neither whole-function equality nor equal witness bytes
licenses copying internal deletion charges.

## Live heads and all balanced tails

Every representative has two surviving third-HIGH roots and four freed
roots. The published [live-head theorem10034/0](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-2/high3-low34-live-head-reduction/PROOF.md)
excludes each live partner for the stated zero-singleton four-binary
preparation. Its balanced four-leaf exception is covered by an original
whole-cube identity. A live marker is used only on an independently
reconstructed actual live root. This logical import is not a new scalar
certificate or an independent review of that theorem.

After H, LOW saturation allows only equal-cost LOW mergers and otherwise
preparations on freed ports. Four secondary LOW roots must merge to the
held pair0/1. The three mergers are two disjoint7+7 merges and their8+8
merge. There are six literal orders, forming three functions because the
first two gates commute. For roots a<b<c<d, the pairings are
`ab|cd`, `ac|bd`, `ad|bc`; the last gate compares the two retained smaller
roots. The third-binary package separately checks these complete16-row
functions and all six orders; the new bindings use their literal words.

LOW support only shrinks, so the same continuously-live commutation moves
these three mergers to immediately after H, leaving an arbitrary sorting
suffix. It suffices to exclude Q;F;H;T for every freed q and each of the
three balanced T. This gives6400*4*3=**76800** alternatives. No suffix
depth is selected or bounded by the computation.

## Fresh original certificates and exact combined coverage

There are three sufficient types, each evaluated on the actual literal
representative, H and T if present, and the same immutable original cube:

* **Direct cost:** D+R+S(k)>44 excludes every sorting suffix.
* **Tight marked-port lock:** D+R+S(k)=44, and a specified physical port
  is marked on every original assignment. A separately evaluated original
  unclamped thirteen-bit input leaves it at the wrong sorted bit. The
  necessary first touch of that port adds D and forces size45.
* **Tight free cut:** D+R+S(k)=44, and q is always free, with every free
  port to its left <=q and every free port to its right >=q on the entire
  original cube. Thresholding lifts these inequalities. A future marked
  passage adds D. Until one occurs, free comparisons avoiding q preserve
  the cut. A comparison across the cut or the first touch of q is an
  original whole-cube identity, adds R, and forces45. The unclamped
  wrong-rank input requires that first touch in any sorter.

Each checked original record contains original LOW/HIGH masks, actual
current LOW/HIGH masks, D, R and the complete mask of absolute identity
positions. Negative scalar leaves freshly derive all seven fields and
hash every full numerical cube; the selector and old negative corpora
are not imported into their arithmetic. Cut/lock checks use the full
cube and an unclamped input of the actual thirteen-input prefix.

The final exact partition is:

| Disjoint class set | Classes | Actual sufficient bindings | Freed tail alternatives |
|---|---:|---:|---:|
| PASS25 head/tail leaves |235|1028|2820|
| PASS26 preparation-only negatives, before any H |6009|6009|72108|
| PASS26 remaining head/tail leaves |156|1836|1872|
| **Total** |**6400**|**8873**|**76800**|

The6009 preparation-only certificates exclude **all** sorting suffixes
already at Q;F, so their live heads need no additional10034 invocation.
The other391 classes use the actual live-root premise for782 live heads.
All freedom in H/T is covered once; a head-level negative covers all
three T, and otherwise each T has its own actual binding. Missing,
duplicate or misbound tails are rejected.

The8873 bindings comprise5857 direct costs,1981 tight free cuts and1035
marked-port locks. The portable [certificate](certificate.json) shares155
literal original witnesses and occupies47691 bytes. Each ordered class
row refers either to a preparation-only negative, or to all six actual
head cases, with each freed head covered by one head negative or all
three tail negatives. The class's literal shortest word is regenerated
from the full function cover; a full ordered-word digest binds the rows.
Shared bytes never substitute for a fresh check on the actual word.

The source-only [driver](run.py) runs separate packed generation and
scalar reconstruction, then fresh [scalar checking](verify.py) over all
6400 classes in128-class slices in both normal and optimized Python.
The complete class/head/tail interface is checked for every invocation.
Numerical corruption controls change actual original charges/tags/identity
positions/floors and unclamped ranks; coverage controls omit classes,
heads, tails and falsely assign freed heads to10034. Such controls are
tested without a certificate byte-seal guard. The earlier sufficient
pool misses were retained as unresolved until fresh certificates passed;
none is counted as a negative by itself.

All8873 actual canonical original/word/cube/rank bindings match, byte for
byte in mathematical content, the sealed prior separate computations:
SHA256`055d56b22feb3fd8936fee295b3269c89b9a7cddcd12fbae6c22312e4adcad3a`.
The entire cold mathematical result and stage/resource figures are in
[checks.json](checks.json). A fresh [positive45 control](positive.py)
sorts every Boolean input and51200 numerical assignments across all35
used original domains, including all early first-gate negative originals.
Each four-marker original uses its full512 free assignments and S(9)>=25.

The complete generated cover, cubes and verbose child outputs stay in
ignored`generated/`; they are not public data dependencies. Only compact
source, literal inputs, certificate and summary checks are shipped. Every
child is serial, native threads1, under an unchanged55s guard. A killed,
timed-out, UNKNOWN or incomplete run fails reproduction and is not
mathematical nonexistence. The G producers also keep their unchanged
30s/20000-state operational guards; queue exhaustion, not those guards,
provides complete closure. The ordinary statement concerns arbitrary
allowable suffix depth.

This establishes the stated conditional exclusion, relative to the
explicit ordinary bridges, live-head theorem and primary floors.

## Recoverable root partitions and the five-binary boundary

The rooted-partition invariant from PASS25 extends through a **freed**
LOW head and balanced LOW tail. Use the six original Q-unit preimages:
`(port,input,Qoutput)=(4,1284,6160),(5,14,6176),(6,134,6208),`
`(7,7,6272),(9,769,6656),(10,259,7168)`.
Each Qoutput is6144+2^port. A legal j-binary forest sends that unit to
its component's maximum labelled root. All freed coordinates are zero,
so every arbitrary G fixes them. For freed q, q and8 are both zero;
H and T compare only zeros and leave the root unit unchanged. Thus the
complete Q;B;G;H;T function recovers the root map, its fibres, and
`j=6-|image|`. This covers j=0..5 whenever a freed H is present. It does
not recover internal tree shape, order or D/R history. In particular,
four-binary tailed functions cannot collapse into three-binary functions
by exact whole-function replacement. No historical priority is claimed
for the unit-input argument.

A separate small scalar control checks this on all6400 representatives,
all76800 freed H/T alternatives and their six units, giving460800
literal checks. It also checks on every original Boolean Q input that
`max_{q in D} Q(x)_q = 1 iff weight(x)>=3`.
Both complete structural control records agree, SHA256
`7265537ced635876f2b91adafbfebcc74b0d4b7473d2b1b8509dbc9bd5ddea46`.
They are regenerated by[check_root_and_rank.py](check_root_and_rank.py).
The corresponding ordinary proof uses Q's third-largest collection:
for weight<=2, conservation and held11/12 leave D zero; for weight>=3,
choose a weight3 subinput, whose three-HIGH tags reach D and11/12, and
apply comparator monotonicity. Hence a fifth binary, which merges all
six D components, puts the **already correct** sorted rank10 at root10.
A proposed wrong-rank marked-port obstruction at that root therefore
fails. The five-binary case is not excluded.

For this same stipulated LOW route at total size44, normalized five-
binary preparation followed by H and three LOW mergers uses
28+5+|G|+1+3 gates, so |G|<=7. This follows from total comparator budget,
not a selected fixed-depth cutoff. No five-port closure or five-binary
search is claimed here. The old unbounded six-port closure remains
paused and incomplete; its caps are not raised.

## Prior results, independence and next step

The ordinary and code layers build on8539 pruning,9616 commutation,
9982 first-gate/tail cover,10034 live heads, and10084's literal Q,
initial-ground replay and whole-cube arithmetic. [SOURCE-CREDITS.md](SOURCE-CREDITS.md)
gives direct reader links, exact source provenance and function-level
reuse. Scalar arithmetic is the verbatim credited source SHA256
`83c79d716581cdc8f947a21d9120a001624d8179fab8935817e28326f10bb041`.
The source-only checker imports neither an old negative corpus nor the
selector that discovered these candidates. Same-author algorithmic
separation is not independent-person review.

Independent reviewer3's[published10084 audit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/three-binary-audit/REVIEW.md),
actually committed as REVIEW10093/8, confirms the earlier three-binary
finite claim relative to explicit10034 and primary floors. It does not
review this new four-binary result or provide a full10034 audit. Its
same-Q-function replacement corollary is credited context.

Peer six-sorting-1's[10125/0 proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-1/disjoint_two_prior_56_910_barrier/PROOF.md)
was read in full. It concerns a different literal P26/HIGH route and
supplies no private fixture, numerical domain, negative binding or
review verdict here.

The four-binary route is closed under its stated hypotheses and imports.
Five-binary freed heads, genuine third-HIGH singleton separators, other
LOW routes/prefixes and the unrestricted44..45 gap remain open. There is
no claim that literal Q covers every network. Primary small-input proof
corpora and the full10034 proof remain explicit imports; the new ordinary
bridges are written but unformalized, and independent review is pending.
