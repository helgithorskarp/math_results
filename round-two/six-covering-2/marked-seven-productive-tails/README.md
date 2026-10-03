# Seven productive tails in a marked minimum-eight cover

Actual author: six-covering-2, researcher.

For distinct ORIGINAL divisors of 10080, minimum EXACTLY 8, containing
`8:0,9:0,10:1,14:0,12:10,16:2,28:4,32:6` with the placed 16 and 32
classes explicitly essential, every covering needs at least **seven
productive TAIL classes**.

[The proof](proof.md) combines a freshly certified 177-hole BASE lower
bound with complete five-/six-tail capacities 120/150. All remaining
BASE and TAIL phases and omissions are free. It does not improve the
global minimum LCM bound, exclude the entire prefix, or construct a cover.

Python 3.11+ standard library, from this directory:

```sh
python3 -B verify.py
```

Full records are regenerated in ignored `generated/`. The driver runs
six sequential normal/optimized children, each guarded at 20 seconds.
The expected manifest pins every deterministic mathematical record.
Ordinary completeness arguments remain unformalized; independent review
is pending. No external proof corpus or third-party package is required.
