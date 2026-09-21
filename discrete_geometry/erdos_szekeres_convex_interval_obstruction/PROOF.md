# Nonuniform blow-ups: a convex-interval obstruction and all convex-seed maximizers

## Setting

Let $S=(p_1,\ldots,p_N)$, $N\ge2$, be a planar general-position set,
ordered by increasing first coordinate. For $h<j$, let $s_{hj}$ be the
maximum size of a convex subset of $S$ with endpoints $p_h,p_j$.
Pairs count as convex. Put $n=k-2\ge1$.

Baek--Balko's general blow-up construction uses nonnegative integer
parameters satisfying

$$
x_i+y_i\le n+1,\qquad
x_h+y_j\le n+1-s_{hj}\quad(h<j).                 \tag{1}
$$

Its cardinality, with no convex $k$-gon, is

$$
B=\sum_{r=0}^{x_1}\binom nr
 +\sum_{i=2}^{N-1}\binom{x_i+y_i}{x_i}
 +\sum_{r=0}^{y_N}\binom nr.                    \tag{2}
$$

Both (1), the construction, and (2) are **prior work**, Lemma 14 of
Baek--Balko (SoCG 2025). We prove an obstruction for these profiles;
we do not claim the construction as new. The irrelevant coordinates
$y_1,x_N$ may be set to zero. Constraints (1) imply $x_i\le n-1$
for $i<N$, and $y_j\le n-1$ for $j>1$.

## Theorem 1: a local certificate, independent of conjectural ES bounds

For $1\le i<N$, define the integer envelope

$$
t_i=\max_{1\le h\le i}(x_h+i-h),
\quad\text{equivalently}\quad
 t_1=x_1,\quad t_i=\max(x_i,t_{i-1}+1).          \tag{3}
$$

For each $2\le j\le N$, choose any index $h_j<j$ attaining

$$
t_{j-1}=x_{h_j}+j-1-h_j.                        \tag{4}
$$

Assume that, for every $j$, the consecutive seed interval
$\{p_{h_j},p_{h_j+1},\ldots,p_j\}$ is in convex position.
Then every feasible profile (1) satisfies

$$
B\le2^n=2^{k-2}.                               \tag{5}
$$

Only these at most $N-1$ intervals must be convex. The whole seed may
be nonconvex. The condition is sufficient, not necessary.

In particular, (5) holds for every convex seed, for every admissible
factor, and for all nonuniform choices of $X,Y$. It also holds for
arbitrary seeds when $x_1<\cdots<x_{N-1}$: choose $h_j=j-1$.
More generally, any choice in (4) whose intervals have at most three
points automatically satisfies the geometric condition.

### Proof: raise parameters, then allocate disjoint binomial levels

By the interval assumption, $s_{h_jj}=j-h_j+1$. Therefore (1) gives

$$
t_{j-1}+y_j
 =x_{h_j}+j-1-h_j+y_j\le n-1\quad(2\le j\le N). \tag{6}
$$

For each interior index, $t_i=x_i$ or $t_i=t_{i-1}+1$ (possibly both).
In the first case (1) implies $t_i+y_i\le n+1$; in the second case
(6) gives the stronger bound $t_i+y_i\le n$. Hence

$$
t_i+y_i\le n+1\quad(2\le i<N).                 \tag{7}
$$

Also $t_{N-1}\le n-1$ by (6) with $j=N$. The envelope is strictly
increasing, so all its coordinates are between zero and $n-1$.
Increasing $x_i$ to $t_i$ increases or preserves the interior summand:

$$
\binom{x_i+y_i}{x_i}\le\binom{t_i+y_i}{t_i}.     \tag{8}
$$

Let $d_i=t_i-t_{i-1}\ge1$. If $d_i=1$, (6) gives
$t_i+y_i\le n$, and thus

$$
\binom{t_i+y_i}{t_i}\le\binom n{t_i}.
$$

If $d_i\ge2$, (7) and Pascal's identity give

$$
\binom{t_i+y_i}{t_i}
 \le\binom{n+1}{t_i}
 =\binom n{t_i-1}+\binom n{t_i}
 \le\sum_{r=t_{i-1}+1}^{t_i}\binom nr.           \tag{9}
$$

Thus each interior summand fits into the consecutive binomial levels
$t_{i-1}+1,\ldots,t_i$. These intervals are mutually disjoint and
follow the levels $0,\ldots,t_1=x_1$ used by the first term of (2).
By symmetry, the last term uses levels $n-y_N,\ldots,n$; (6) ensures
that $n-y_N\ge t_{N-1}+1$. All these levels are disjoint subsets of
$\{0,\ldots,n\}$. Their total is at most $2^n$, proving (5).

No assertion that the raised parameters satisfy **all** cross-constraints
is needed in this proof. The displayed local bounds (6)--(7) suffice.

### A purely numerical certificate and exact deficit

The same proof applies whenever (6)--(7) hold, whether or not the
convex-interval hypothesis is checked. Define, for interior $i$,

$$
A_i=\binom{t_i+y_i}{t_i}-\binom{x_i+y_i}{x_i},
\qquad
D_i=\sum_{r=t_{i-1}+1}^{t_i}\binom nr
       -\binom{t_i+y_i}{t_i}.
$$

Then all $A_i,D_i$ are nonnegative and the exact certificate is

$$
2^n-B
 =\sum_{r=t_{N-1}+1}^{n-y_N-1}\binom nr
  +\sum_{i=2}^{N-1}(A_i+D_i).                   \tag{10}
$$

Empty sums are zero. Computing (3), (6)--(7), and (10) requires no
convex-subset enumeration. Failure of this sufficient test gives no
counterexample and no conclusion about the actual sign of $2^n-B$.

## Theorem 2: all equality profiles for convex seeds

Let $S$ be convex with $N\ge2$ and let (1) hold. Then $B=2^n$ if and
only if the **active** parameters satisfy

$$
\begin{aligned}
&x_1\ge0,\qquad d_i=x_i-x_{i-1}\in\{1,2\}
                           &&(2\le i<N),\\
&x_{N-1}\le n-1,\qquad
 y_i=n+d_i-1-x_i             &&(2\le i<N),\\
&y_N=n-1-x_{N-1}.&&
\end{aligned}                                                   \tag{11}
$$

The inactive $y_1,x_N$ are unrestricted except for their original
nonnegativity and local bounds in (1). For $N=2$, (11) just means
$x_1+y_2=n-1$.

In particular, convex seeds admit feasible parameters exactly when
$k\ge N+1$, their maximum blow-up size is $2^{k-2}$, and all parameter
profiles attaining that maximum are specified by (11). At the smallest
factor $k=N+1$, the unique active equality profile is
$x_i=i-1$ for $i<N$, and $y_j=N-j$ for $j>1$.
The existence of this latter profile, even for arbitrary seeds, is
already in Baek--Balko's known-construction discussion.

### Proof of necessity

A convex seed supplies every interval required in Theorem 1. Equality
in (10) means every nonnegative term is zero. The gap term vanishes
exactly when $t_{N-1}+y_N=n-1$, since every binomial level is positive.

For an interior index, $1\le t_i\le n-1$. If $d_i=1$, equality in
its binomial bound holds exactly when $t_i+y_i=n$. If $d_i\ge2$, it
requires $t_i+y_i=n+1$ and $d_i=2$: for $d_i>2$ there is an additional
positive binomial level in (9). In particular, equality always requires
$y_i>0$. For such $y_i$, the function
$u\mapsto\binom{u+y_i}{u}=\binom{u+y_i}{y_i}$ is strictly increasing
on nonnegative integers. Therefore $A_i=0$ forces $t_i=x_i$. This gives
all the conditions in (11). The case $N=2$ follows directly from the
two disjoint binomial tails.

### Proof of sufficiency and feasibility

Any profile (11) has $t_i=x_i$. Each gap of size one uses exactly one
binomial level, each gap of size two uses exactly two by Pascal's
identity, and the final tail begins immediately after the last allocated
level. Thus (10) vanishes.

For completeness these active profiles are feasible for convex seeds,
with $y_1=x_N=0$. For an interior $j$ and $h<j$,

$$
x_j-x_h=\sum_{r=h+1}^j d_r\ge d_j+(j-h-1),
$$

so $x_h+y_j\le n-(j-h)=n+1-s_{hj}$. For $j=N$ use
$x_{N-1}-x_h\ge N-1-h$ to obtain the same bound. Interior local sums
are $n+d_i-1\le n+1$; the endpoint local bounds hold as well.
Nonnegative parameters exist if and only if $N\le n+1$, since (1)
with $h=1,j=N$ requires $0\le n+1-N$, while choosing every $d_i=1$
and $x_1=0$ satisfies (11) for every $N\le n+1$.

## Scope and value

This excludes an entire nonuniform construction family unconditionally,
and gives a small checkable sufficient obstruction beyond convex seeds.
It complements the earlier **conditional hereditary** obstruction for
uniform blow-ups; neither theorem implies the other in general.
The present proof does not assume Erdős--Szekeres at smaller sizes.

The result does not prove the Erdős--Szekeres conjecture. Nonconvex seeds
with longer obstructing intervals remain outside the certificate, and
failure of the certificate is not evidence that a blow-up beats $2^{k-2}$.
Equality here classifies the integer parameters, not the order types or
geometric realizations of the clusters. Independent review and proof
assistant formalization are pending. See SOURCES.md for attribution and
the unavailable full-text limitation in the 2026 journal novelty audit.
