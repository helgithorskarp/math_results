# Source and transformation record

The package reads, hashes, and independently reconstructs complete unit-edge
sets from these repository inputs:

```text
../hadwiger_nelson_nonmono159_214_lowden2/points159.tsv
SHA-256 4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02

../hadwiger_nelson_nonmono159_214_lowden2/points214.tsv
SHA-256 97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f
```

Their upstream coordinate provenance is recorded in the sibling source
package.  The Golomb coordinates are written directly in `verify.py` at scale
36 and are independently checked to give ten distinct points and eighteen
complete unit edges.

The selected B214 transformations are exactly

```text
L(x,y)=(x-1/2,y),
R(x,y)=(-x+1/2,y).
```

The A159 completion uses the archived coordinates without transformation.
No approximate coordinates, tolerance merge, selected edge list, or omitted
placement parameter enters the result.

