"""Decode the inspected source pickle with a closed constructor allowlist."""
import hashlib
import io
import json
import pickle
import argparse
from pathlib import Path

import sympy as s


class Array:
    def __setstate__(self, state):
        if len(state) != 5 or state[1] != (29,) or state[3] is not False:
            raise ValueError("unexpected array state")
        self.values = state[4]


class Dtype:
    def __init__(self, *args):
        if args != ("O8", False, True):
            raise ValueError("unexpected dtype")

    def __setstate__(self, state):
        if state != (3, "|", None, None, None, -1, -1, 63):
            raise ValueError("unexpected dtype state")


def reconstruct(cls, shape, dtype):
    if cls is not Array or shape != (0,) or dtype != b"b":
        raise ValueError("unexpected reconstruction")
    return Array()


allowed = {
    ("numpy._core.multiarray", "_reconstruct"): reconstruct,
    ("numpy", "ndarray"): Array,
    ("numpy", "dtype"): Dtype,
    ("sympy.core.add", "Add"): s.Add,
    ("sympy.core.mul", "Mul"): s.Mul,
    ("sympy.core.power", "Pow"): s.Pow,
}
for name in ["Integer", "Rational", "Half", "One", "Zero", "NegativeOne", "ImaginaryUnit"]:
    allowed[("sympy.core.numbers", name)] = getattr(s.core.numbers, name)


class Restricted(pickle.Unpickler):
    def find_class(self, module, name):
        if (module, name) not in allowed:
            raise ValueError(("unallowed constructor", module, name))
        return allowed[module, name]


base = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("npy", type=Path)
args = parser.parse_args()
data = args.npy.read_bytes()
if hashlib.sha256(data).hexdigest() != "19766f3a5c31d544c5b15aa2f64cb2996684dc17b1818d9a5e5b20a90d8614a3":
    raise ValueError("source input hash")
if data[:8] != b"\x93NUMPY\x01\x00":
    raise ValueError("npy header")
header_length = int.from_bytes(data[8:10], "little")
array = Restricted(io.BytesIO(data[10 + header_length:])).load()
if len(array.values) != 29 or not all(isinstance(v, s.Expr) for v in array.values):
    raise ValueError("source entries")
w, b, c, e = s.symbols("w b c e")
eta = s.I * s.sqrt((415 + 79 * s.sqrt(33)) / 8)
images = {s.sqrt((415 + 79 * s.sqrt(33)) / 8): e / (8*s.I)}
rows = []
radicals = {}
for mask in range(1,8):
    n = 1
    val = s.Integer(1)
    for bit, prime, replacement in [(0,3,(2*w-1)/s.I),(1,11,b/s.I),(2,5,c)]:
        if mask & (1<<bit):
            n *= prime
            val *= replacement
    radicals[s.sqrt(n)] = val
for i, value in enumerate(array.values):
    value2 = s.expand(value.xreplace(images))
    value2 = s.expand(value2.xreplace(radicals))
    poly = s.Poly(value2, w, b, c, e)
    row = [0]*16
    for powers, coefficient in poly.terms():
        if any(x > 1 for x in powers):
            raise ValueError(("nonlinear source monomial", i, powers))
        index = sum(x << k for k, x in enumerate(powers))
        coefficient = coefficient*384
        if not coefficient.is_Integer:
            raise ValueError(("noninteger numerator", i, coefficient))
        row[index] = int(coefficient)
    rows.append(row)
    # Independent symbolic substitution into the original expression.
    back = sum(s.Rational(v,384)*((1+s.I*s.sqrt(3))/2)**(j&1)
               *(s.I*s.sqrt(11))**((j>>1)&1)*s.sqrt(5)**((j>>2)&1)
               *(8*eta)**((j>>3)&1) for j,v in enumerate(row))
    if s.simplify(s.expand(back-value)) != 0:
        raise ValueError(("source reconstruction", i))
out = {"denominator":384,"basis":"w^i b^j c^k e^l, index=i+2*j+4*k+8*l", "numerators":rows,
       "source_npy_sha256":hashlib.sha256(data).hexdigest()}
import geometry
if rows != [list(x) for x in geometry.seed()]:
    raise ValueError("all source coordinates must equal published seed")
print(json.dumps({"verified":True,"symbolic_source_reconstructions":29,"source_npy_sha256":out["source_npy_sha256"]},indent=2))
