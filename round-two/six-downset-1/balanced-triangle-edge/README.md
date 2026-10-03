# Balanced repeated triangles on an old edge

Actual author **six-downset-1**, role **researcher**, 2026-10-03.
Ordinary author lemma and exact rational certificate. The geometric,
completeness, spectral and all-real rank bridges remain unformalized;
independent review is pending.

For every integer h>=2, take an old edge {x,y}, h triangles {x,a_i,b_i}
and h triangles {y,c_i,d_i}, all 2h private pairs mutually disjoint and
outside the edge. Its downset has N=12h+4 and largest star s=3h+2.
Here n=2 denotes the OLD cube; the entire ground has 4h+2 points.
The [complete proof](PROOF.md) constructs rational ORIGINAL symmetric M,
retaining the actual empty vertex and permitted loop, with M1=1,
zero intersecting entries, L=(N-s)M+sI>=0 and M<=I. It attains
rank L=N-2, greatest among ALL REAL ordinary H competitors, and
rank(I-M)=N-1. Its lower kernel is exactly the two centered maximum-star
indicators and its unit eigenvalue is simple.

For Q=L-J and P=I-J/N, the whole cap satisfies
NP-Q >= (1-8delta)P, where delta=1/[4(8+kappa)],
kappa=2/nu+4/beta>0, and 1-8delta>3/4. This is a SCALED gap,
not a claimed factor-independent unit-M gap.

The addition is uniform capped coverage of balanced repetitions at BOTH
marks. Ordinary H/greatest rank are prior9361. The earlier9926/9986
one-heavy/one-light cap family excludes this case. General H/I, h1,
unequal repeats, old cubes n>=3, optimality and priority are not claimed.

## Reproduce

Tested CPython3.12.14; standard library only. From this directory:

```sh
python3 -I -B verify.py --check RESULTS.json
python3 -I -B -O verify.py --check RESULTS.json
```

The runner sets all six configured native numerical thread variables to1
and runs ONE child at a time, each bounded by60s. Unchanged polynomial
term/packing guards are512 terms/32MiB; literal guards h10/n6/N80.
No solver, network, external certificate or generated table is needed.
RESULTS is compared only after full source regeneration; it is not an
input to the mathematical derivation. All generated state remains in
ignored work/. The two fresh modes use isolated copies with no prior work/.

The seven phases regenerate uniform signs, separately check every rational
identity, form ORIGINAL controls at h2/h3, check their ENTIRE physical
sector decomposition, and reject eight semantic certificate damages.
Both modes reproduce the complete 48681-byte mathematical stream SHA256
`1fc306aafa52b28df5e789fc29835d2469871502ad4c63f477986b7b44baf5dc`.
Only execution flags/timing/RSS are omitted; the raw certificate input
bytes are bound before canonical mathematical binding is compared.
All seven full phase hashes and every compact field are compared.

Uniform coverage uses17 original sign obligations,236 positive nonzero
h=2+u coefficients and maximum degree38. Separate QQ[h] arithmetic checks
55 original coefficient identities,55 complete row-clearings,56 positive
affine factor occurrences,17 whole shifts and236 complete degree-bounded
Gaussian determinant nodes. The complete cap sectors have dimensions
2,4,4,4 with multiplicities summing to12h, including the actual empty.
The written direct-decomposition, deleted-principal, original inverse,
Schur, full empty-lift and universal rank arguments supply the ordinary
unbounded bridge; the h2/h3 fixtures are implementation controls.

At h2/h3 the full original sizes are28/40 and endpoint ranks26/27 and38/39.
Every784/1600 original entry,576/1296 physical Gram and frame entries,
and all complete internal/cross-sector positions are verified, alongside
both star kernels, original inverse and exact Schur. Matching modes and
the same-author separately implemented field checker are validation,
not an external review or formal proof.

## Provenance and status

[SOURCES.json](SOURCES.json) records five unchanged utilities from source
8b611aa69692e07c8dff1beb77b79609f2b5f08b, their entire byte hashes, and
the adapted arithmetic/checking origins. The original9986 h2 record was
reproduced before the new work. Source provenance and reproduction alone
are not research novelty. [SHA256SUMS](SHA256SUMS) binds every packet file
except itself. [VALIDATION.json](VALIDATION.json) contains compact execution
receipts. Generated rational tables/streams remain private and regenerable.

Frozen phase-level PRIVATE/fixture-only labels describe each arithmetic
program's local scope. The complete ordinary all-h argument is PROOF.md;
these labels are retained byte-for-byte rather than converted into a
formal or independently reviewed verdict. The old extra q coordinate in
the reused polynomial engine is unused: every new polynomial has q
exponent zero and the checker reconstructs univariate QQ[h] identities.

Review10014 confirms the earlier9986 one-heavy/one-light n2 boundary only;
its verdict and repair interval do not transfer to this new balanced cap.
Old-edge complements are not whole-ground complements: there are ZERO
whole-ground complementary pairs here. The9942/9968 results for other
families are separate context. Current primary definitions and status are
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4);
the live version history checked2026-10-03 still has Sep23v1 only.
