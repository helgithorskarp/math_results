# A counterexample family for the three-color restricted Schur formula

For every integer $k\ge2$,

$$S_3(k;2)\ge k(k+1)(k+2)-2.$$

Here $S_3(k;2)$ is the least integer forcing a monochromatic equation
$x_1+\cdots+x_k=y$ with exactly two distinct summand values in every
three-coloring. The bound exceeds $k^3+3k^2+k-1$ by $k-1$, answering
[Gaiser's Open Question 6.2](https://arxiv.org/html/2608.08789v1#S6)
negatively for every $k\ge2$.

The [complete proof](proof.md) appends $k-1$ red integers to the six
intervals of Gaiser's Proposition 6.1. It proves avoidance even when any
number of distinct summand values from two through $k$ is allowed. The
extension is unique and maximal with the published prefix fixed; this
does not give a global upper bound or an exact formula for $S_3(k;2)$.

## Reproduce

Use Python 3.11 or later and the standard library only. Tested with
CPython 3.11.2 on Linux; no packages or downloads are required. From this
directory run:

```bash
python3 verify.py --check-expected
python3 -O verify.py --check-expected
sha256sum -c SHA256SUMS
```

Each Python command prints the same deterministic JSON, reproduced in
[expected.json](expected.json), and exits zero only when all checks pass.
One run takes about one second in the publication environment. It reports:

- `ALL_EXACT_CHECKS_PASSED` for the eleven colorings with $2\le k\le12$;
- full dynamic-programming checks of nonconstant sums and separate direct
  checks of equations with exactly two summand values;
- 384 comparisons of the sum enumerator against literal multiset
  enumeration, covering every subset of $[1,7]$ and $k=2,3,4$;
- a control where one sum has both constant and nonconstant
  representations, preventing an invalid subtraction shortcut;
- 165 checked extension witnesses and 66 rejections of forbidden
  extensions by the two separate auditors;
- 13 malformed-certificate rejections and 15 compact endpoint witnesses
  at three large integer parameters, the largest exceeding $10^{100}$.

The deterministic record SHA-256 is
`98264b776321f9e8874f007befda97440da0ed2a015ea4cfce273985c00823a2`.
It hashes the JSON object excluding its `record_sha256` field, serialized
with `json.dumps(result, sort_keys=True, separators=(",", ":"))`.

## Evidence and source

| File | Role |
| --- | --- |
| [proof.md](proof.md) | Universal interval proof and exact fixed-prefix extension theorem |
| [construction.py](construction.py) | Seven intervals and compact obstruction witnesses |
| [audit.py](audit.py) | Independent definition-level sum and witness auditors; imports no construction code |
| [verify.py](verify.py) | Deterministic finite validation and controls |
| [expected.json](expected.json) | Complete compact expected result, including per-coloring hashes |
| [SOURCES.md](SOURCES.md) | Primary-source attribution, graph selection, and novelty scope |
| [SHA256SUMS](SHA256SUMS) | Hashes of the other eight public files |

All computations use exact Python integers. The finite checks validate
the source and boundary cases; the theorem for every $k$ rests on the
written proof. No solver, external dataset, floating point, or large
omitted certificate is required. Exploratory SAT files are not part of
the theorem's evidence dependency. No independent researcher review or
proof-assistant formalization is claimed.

This is a complete negative answer to the specified eventual-equality
question. It preserves the validity of the paper's earlier lower bound,
does not change its leading cubic scale, and does not claim that the new
bound is optimal.
