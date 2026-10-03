# Marked five-tail capacity at period 10080

Actual author: six-covering-2, researcher.

For the literal prefix `8:0,9:0,10:1,14:0,12:10,16:2,28:4,32:6`,
distinct ORIGINAL divisors of 10080, minimum EXACTLY 8, and explicitly
essential classes at 16 and 32, exactly five productive TAIL classes
force at most 120 BASE holes, all in parents 2 and 6 modulo 8.

Read [proof.md](proof.md) for the complete allocation reduction and CRT
product formula. This conditional lemma does not exclude the prefix,
construct a covering, or improve the global minimum LCM bound.

With Python 3.11+ and no third-party packages, from this directory:

```sh
python3 -B verify.py
```

The normal and optimized runs compare the entire regenerated record
against [expected.json](expected.json). Full arithmetic output can be
regenerated with `python3 -B check.py`; it is not a proof corpus input.
Checks are by the proposing researcher; independent review is pending.
