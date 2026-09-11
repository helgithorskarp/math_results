# A global four-case reduction for 72-point line-free sets in AG(3,5)

**Theorem.** Suppose (S\subseteq\mathbb F_5^3\) has 72 points and contains
no complete affine line. Write (a_m\) for its number of affine plane
sections of size (m\). Then

\[
a_8+a_9\ge5,\qquad a_8+a_9+a_{10}\ge7,\qquad
a_8+a_9+a_{10}+a_{11}\ge9.
\]

No five planes of size at most nine have collinear normal directions in
the dual projective plane. Consequently (S\) has three such planes with
independent normals. After an affine change of coordinates, the three
coordinate parallel classes have one of these four profiles:

| Case | (x\)-profile | (y\)-profile | (z\)-profile |
|---|---|---|---|
| AAA | A | A | A |
| AAB | A | A | B |
| ABB | A | B | B |
| BBB | B | B | B |

Here the entries are indexed by coordinate values (0,1,2,3,4\), and

\[
A=(8,16,16,16,16),\qquad B=(9,15,16,16,16).
\]

These cases cover **every** possible 72-point set, and may overlap.
The exact incidence bounds and projection exclusion below are proved
without a solver verdict. The CNFs are a downstream decision formulation;
their generation does not exclude any case. The numerical interval remains
[70–72](../upper_bound72.md), and existence at 71 or 72 remains open in this work.

## 1. Complete incidence system

The planar enumeration visits all (2^{25}\) labelled subsets. There is no
line-free 17-subset, so every section has size at most 16. Four other
parallel planes contain at most 64 points, so every section of (S\) has
size at least eight.

For an affine line ℓ meeting (S\) in (k\) points, its six containing
planes satisfy

\[
\sum_{H\supset\ell}|S\cap H|=72+5k. \tag{1}
\]

If a section has size at most 11, it has no four-point line: otherwise
(1) would give (92\le11+5\cdot16=91\). The enumeration therefore retains
all planar subsets of sizes 8–11 with line intersections at most three,
and of sizes 12–16 with line intersections at most four. It produces
exactly 70 distinct spectra (s=(m,n_0,n_1,n_2,n_3,n_4)\), where (n_k\)
counts the planar lines meeting the subset in (k\) points. Labelled
multiplicities are recorded for complete replay but are not LP coefficients.

Introduce nonnegative variables:

* (X_s\): number of planes with spectrum (s\), for the 70 spectra;
* (P_p\): number of parallel plane classes with size multiset (p\), for
  all 18 nondecreasing five-tuples in ([8,16]\) summing to 72;
* (Y_{k,t}\): number of (k\)-point lines with pencil size multiset (t\),
  for all 375 pairs with (0\le k\le4\), six nondecreasing entries in
  ([\max(8,5k-8),16]\), and sum (72+5k\).

The lower pencil entry bound follows from (1) and the other five entries
being at most 16. Every actual (S\) gives an integer nonnegative solution
of these **61 equations**:

\[
\begin{aligned}
\sum_sX_s&=155,&\sum_s mX_s&=2232,&
\sum_s\binom m2X_s&=15336,\\
\sum_pP_p&=31,&
\sum_{s:m(s)=m}X_s&=\sum_p\#_m(p)P_p\quad(8\le m\le16),\\
\sum_{s:m(s)=m}n_k(s)X_s&=\sum_t\#_m(t)Y_{k,t}
&&\quad(0\le k\le4,\ 8\le m\le16),\\
\sum_{k,t}Y_{k,t}&=775,&\sum_{k,t}kY_{k,t}&=2232,&
\sum_{k,t}\binom k2Y_{k,t}&=2556.
\end{aligned}
\]

Here #_m denotes multiplicity. A point lies in 31 affine planes and 31
affine lines; a pair lies in six planes and one line. Plane/pencil flags
give the middle incidence equations. [model.py](model.py) regenerates
their exact integer matrix (M\), right side (b\), and fixed row order.

For cutoff (c\), let (q_c\) be one on the (X_s\) columns with (m\le c\)
and zero elsewhere. Each published incidence certificate has integer
multipliers (z\) and positive denominator (D\). The checker verifies all
463 inequalities

\[
M^Tz\le Dq_c.
\]

Thus (q_c^Tu\ge b^Tz/D\) for every nonnegative solution (Mu=b\).
The three exact certified lower bounds are

| Cutoff | Rational bound | Integer consequence |
|---|---:|---:|
| 9 | (88133/20000\) | at least 5 planes |
| 10 | (329933/50000\) | at least 7 planes |
| 11 | (1333/160\) | at least 9 planes |

Floating-point LP optimization discovered the multipliers. Published
integer multipliers were rounded and corrected so every column inequality
holds exactly. Optimization, floating-point feasibility and integrality
solver output are not premises of the theorem.

The [integral control](incidence_integer_control.json) is an exactly checked
nonnegative integer solution of this aggregate system. It represents
incidence counts, not an actual set of affine points. It demonstrates a
specific limit of this formulation: a 72-point exclusion needs geometric
compatibility constraints beyond these 61 aggregate equations.

## 2. Excluding five collinear low-plane normals

Two planes of size at most nine cannot be parallel: those two and the
other three parallel planes would contain at most (18+48=66<72\)
points. Their normal directions are therefore distinct.

If five such normals lie on a projective line, the corresponding planes
are all parallel to a common one-dimensional direction (d\). Project
along (d\) to (\operatorname{AG}(2,5)\). Let (w(p)\) be the number of
selected points in the fiber over (p\). Then

\[
0\le w(p)\le4,\qquad \sum_pw(p)=72,\qquad
\sum_{p\in L}w(p)\le16\quad\text{for all 30 quotient lines }L.
\]

The five small planes give five nonparallel quotient lines of weight at
most nine. A linear change of coordinates sends the omitted sixth
direction to the vertical direction. The five lines are then

\[
y=ax+b_a\quad(a\in\mathbb F_5).
\]

A translation sets (b_0=b_1=0\); it leaves exactly (5^3=125\) triples
((b_2,b_3,b_4)\). This normalization includes every arrangement, including
concurrent lines. The certificates enumerate every triple individually.

For each arrangement, write (A\) for the 30-by-25 line incidence matrix
and (d\) for the 30 bounds (nine on the selected lines, 16 elsewhere).
The certificate gives nonnegative integer vectors λ (length 30), μ
(length 25), and a positive integer (D\), with

\[
A^T\lambda+\mu\ge D\mathbf1,\qquad
\frac{\lambda^Td+4\mathbf1^T\mu}{D}\le\frac{1499}{21}<72.
\]

Multiplying the line and point constraints gives this upper bound on
(\sum_pw(p)\), a contradiction. This argument even permits real fiber
weights. Every inequality is checked using integers; the largest certified
bound among all 125 arrangements is exactly (1499/21\).

## 3. Global coordinate cover and CNF meaning

There are at least five low planes, with distinct normals, and these
normals cannot all lie on one projective line. Hence they span the
three-dimensional dual vector space. Choose three independent normals.
Their planes intersect in a unique point. Translating that point to the
origin and taking the normal forms as coordinates makes the planes
(x=0,y=0,z=0\).

An eight-point zero plane forces the other four parallel planes to have
size 16. A nine-point zero plane forces one other plane of size 15 and
three of size 16. In the second case multiply that coordinate by the
inverse of the nonzero label of the 15-plane, making its label one.
These three scalings are independent. Permuting the coordinates leaves
the four unordered A/B triples in the theorem. Arbitrary permutations of
the five coordinate labels are **not** assumed.

[generate.py](generate.py) uses primary variables (1+25x+5y+z\) and
encodes all 775 forbidden complete lines, exactly 72 points, the bound
16 on every plane, and the exact coordinate profiles. Low coordinate
planes receive their proved three-points-per-line constraints. For the
intersection line of two low coordinate planes, (1) also gives

\[
k\le\left\lfloor\frac{m_1+m_2+64-72}{5}\right\rfloor,
\]

which is one for AA or AB, and two for BB.

The theorem supplies at least two further low planes beyond the three
coordinate zero planes. Each of the 140 planes outside the coordinate
parallel classes gets an indicator (v_H\). The implication
(v_H\Rightarrow |S\cap H|\le9\), and its three-points-per-line
consequence, are encoded; at least two indicators must be true. The
indicators need not characterize all low planes. Every actual candidate
admits these auxiliary values. Conversely, any satisfying assignment to
any CNF directly gives a 72-point line-free set through its 125 primary
variables. This establishes equivalence for the union of the four cases.

## Replay and evidence limits

Requires Python 3.10+ and a C++20 compiler; tested with Python 3.11.2 and
GCC 12.2. From this directory:

```sh
python3 verify.py --out build/low_planes72
```

Expected status: `GLOBAL_72_LOW_PLANE_REDUCTION_VERIFIED`, matching
[expected.json](expected.json). The replay enumerates all labelled planar
subsets, checks the three dual certificates column by column, checks all
125 projection certificates point by point, and verifies the affine
incidence identities using independently generated planes and lines.
No Python dependency, optimizer, solver, network or external catalogue is
needed. The written mathematical reduction and ordinary compiled code are
trust boundaries; this is not a proof-assistant formalization.

Only the optional CNF generator needs `python-sat==1.9.dev15`:

```sh
python3 -m pip install -r requirements.txt
python3 generate.py --case 0 --out build/case0.cnf
```

Repeat for cases 1, 2 and 3. [runs.json](runs.json) records the generated
hashes and actual search statuses. Large CNFs and partial solver traces
remain outside Git; they can be regenerated. No incomplete run is a proof
of exclusion. The compact certificate and source hashes are in
[manifest.json](manifest.json).

The parameter and prior 70-point construction are from Elsholtz et al.,
*Maximal line-free sets in F_p^n*, Periodica Mathematica Hungarica 90 (2025),
7–21 ([primary paper](https://arxiv.org/abs/2310.03382v2),
[DOI](https://doi.org/10.1007/s10998-024-00617-x)). This contribution is a
conditional global structure theorem at 72, separate from the earlier
[upper bound](../upper_bound72.md) and [sparse-direction exclusion](../sparse_directions/README.md).
