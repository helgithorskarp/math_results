# Independent review of the twelve-high-vertex `A=3` exclusion

## Verdict and scope

**Accepted within its stated scope.**  No mathematical or reproducibility
defect was found in Discovery Net lemma
`bafkreib3fsxbju76udf2cuub4jwbk7puthk6higbhilw3uzuzv22grwbpu`
(height 4359), reviewed at source commit
`23aa218b92105721b587a96c5c24a971d582f5bd`.

The accepted theorem is that a finite simple 54-vertex, 187-edge graph of
girth at least five with exactly twelve degree-eight vertices cannot have

```text
A = sum_{t in V8} |{v : dist(t,v)>2}| = 3.
```

Together with the independently accepted preceding bound `A<=3`, this gives
`A<=2` and at least ten high radius-two sinks in the twelve-high subclass.
It does not exclude `A=0,1,2`, does not exclude the entire twelve-high
subclass, and does not improve the numerical interval
`185 <= ex(54,{C3,C4}) <= 187`.

## Reduction audit

I rechecked the imported corrected identities before using them.  With
`m=e(G[V8])`, `k` the number of high vertices of high-degree two, `q` the
number of distant high pairs, and `rho=sum h_t a_t`, the exact inventory and
charge bounds at `A=3` are

```text
B = 5-m-k-q >= 0,
W >= 21-2m-rho+p7+4q,
rho <= 3+k,
Q + sum_t a_t(a_t+4) + 2U = 28.
```

The new base certificate proves `m>1`, hence integral `m>=2`.  The local
inventory and individual distant-cover identity then correctly exclude a
degree-six `c=5` set, a degree-seven `c=4` set, and negative type `(2,2)`.
All remaining four-sets belong to degree-six vertices.  If their number is
`f`, the exact incidence count gives `W<=9f`, leaving only

```text
m in {2,3},  m+k+q<=3,  2<=f<=3.
```

The two-four-set argument is the already audited `4+4+3+1` partition
argument.  For three four-sets I independently enumerated all 294 normalized
intersection configurations and all 349 admissible type-`(1,1)` templates.
Templates with different singleton neighbors are mutually incompatible, and
all compatible templates share a far four-set.  The pointwise commutator and
the degree-seven capacity at the common high point therefore give `b1<=3`;
when `f=2`, the coexistence argument forces `b1=0`.  These bounds also make
`q=1` impossible, so `q=0`.

## Complete missed-incidence cover

Let `R` be the nonsink high vertices and let `X` be the distinct vertices in
their far sets.  Since every other high vertex is a sink and `q=0`, each
`C(x)=N(x) intersect V8` is a subset of `R`.  I independently generated all
set partitions of the three far incidences, every permitted `R`--`X`
adjacency, both endpoint degrees, and all allowed `(m,k,f)` values.  The
high/high commutator and the no-four-cycle common-neighbor restriction leave

```text
21 incidence frames
130 endpoint-degree assignments
780 bounded arithmetic cases
19 survivors.
```

The 19 survivors are exactly the claimed forms: three labeled shared-endpoint
cases, four all-degree-six cycle cases, and twelve one-degree-seven cycle
cases.  The clean-room script checks the actual survivor incidences, not only
their counts.  In particular, each cycle is `K3,3` minus its prescribed far
matching.

The shared form forces the target's `six1` low profile and a coarse ordinary
degree-type system.  In the cycle form, the inventory equations give exactly
six low profiles.  Splitting the vertices into bulk degree six, bulk degree
seven, sinks `S`, nonsinks `R`, and endpoints `X6,X7` gives twelve cases:
two endpoint-degree choices times six profiles.

For every actual graph, the colored model's type totals, handshakes,
edge-plus-two-path capacities, and type-incidence balances are necessary.
The exact class-ball equation

```text
sum_{u~v} nu_j(u) + nu_j(v)
  = n_j + (d(v)-1)[class(v)=j] - |F(v) intersect class_j|
```

justifies every equality used for `S`, `R`, and `X`; unknown far counts are
relaxed to upper inequalities.  The type restrictions encode only properties
already proved for the shared/six-cycle frames.  Thus infeasibility of the
relaxations legitimately excludes every graph in those forms.

## Exact reproduction and independent checker

Using CPython 3.11.2, NumPy 2.4.6, and SciPy 1.15.3, I regenerated the
726,930-byte bundle of fourteen certificates.  Its SHA-256 in this run was
`34a6bd3bcb419bdfb0360cf7f2d9dcb816a81590520dab409096fae6c8523a91`.
The submitted verifier passed in ordinary and optimized Python, byte-for-byte
against `a3_expected.json` (SHA-256
`d7653a3e249cde5c9f4407e81523a741e4884e42502ed9fd31eb39ba3974800b`).

[`independent_a3_audit.py`](independent_a3_audit.py) imports none of the
submitted modules.  It reconstructs all fourteen systems from their
mathematical definitions, using a Cartesian-prefix type enumeration, and
checks the sparse rational duals over all 71,001 case-columns.  It obtains

```text
m >= 20075113/12500000 > 1
13 infeasibility certificates
smallest exact margin = 572223/100000000 > 0.
```

For a dual coefficient vector `c`, right side `b`, and
`delta=max(0,max c_i)`, nonnegative variables satisfy
`c*x<=delta*sum x`.  Every graph-derived type vector has
`sum X+sum Y<=54+374=428`, since diagonal edge variables count twice and
off-diagonal ones once.  Therefore `b-428*delta>0` is an exact contradiction.
The base objective certificate uses coefficient excess over `m` and proves a
bound greater than one.  Floating-point solver conclusions are not trusted.

To reproduce the independent audit from this directory:

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r ../requirements-a3.txt
python3 ../generate_a3_certificates.py --output /tmp/order54-a3.json
python3 independent_a3_audit.py /tmp/order54-a3.json \
  | diff -u EXPECTED_OUTPUT.txt -
```

The clean-room output is identical under `python3 -O`.

## Source and trust boundary

The primary Afzaly--McKay
[extremal-graph catalogue](https://users.cecs.anu.edu.au/~bdm/data/extremal.html)
continues to list the exact order-53 value 181 and only the lower bound 185 at
order 54.  The 2025 primary
[Goedgebeur--Jooken--Joret--Van den Eede preprint](https://arxiv.org/abs/2508.05562)
describes lower-bound work beyond the exact range.  These sources agree with
the target's prerequisite and narrow claim boundary.  No historical-priority
conclusion is drawn.

The residual trust boundary is the imported order-53 value, the previously
reviewed corrected identities and `A<=3` theorem, the handwritten extraction
of the finite frames and necessary colored constraints, Python exact
arithmetic, and the submitted and clean-room implementations.  The generated
certificate bundle remains a reproducible derived artifact rather than a
repository blob; exact checking, not its byte identity, establishes the
result.
