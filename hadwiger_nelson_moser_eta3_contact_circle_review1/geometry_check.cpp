#include <cstdint>

// Independent exact metric in the reviewer's basis
//   (a+b*sqrt(33)) + alpha*(c+d*sqrt(33)), alpha^2=-3,
// with a second coordinate multiplying sqrt(s), s=s0+s1*sqrt(33).
// All inputs share the positive denominators den and sd.
using I = __int128_t;
using L = std::int64_t;

extern "C" int review_contacts(int n, L den, L sd, L s0, L s1,
                                const L* points, int* edges) {
  if (n < 1 || n > 343 || den < 1 || den > 1000000000LL ||
      sd < 1 || sd > 1000000000LL || s0 < -1000000000LL ||
      s0 > 1000000000LL || s1 < -1000000000LL || s1 > 1000000000LL)
    return -1;
  for (int k = 0; k < 8 * n; ++k)
    if (points[k] < -1000000000LL || points[k] > 1000000000LL) return -2;

  int count = 0;
  for (int i = 0; i < n; ++i) {
    for (int j = i + 1; j < n; ++j) {
      I a = I(points[8 * i]) - points[8 * j];
      I b = I(points[8 * i + 1]) - points[8 * j + 1];
      I c = I(points[8 * i + 2]) - points[8 * j + 2];
      I d = I(points[8 * i + 3]) - points[8 * j + 3];
      I A = I(points[8 * i + 4]) - points[8 * j + 4];
      I B = I(points[8 * i + 5]) - points[8 * j + 5];
      I C = I(points[8 * i + 6]) - points[8 * j + 6];
      I D = I(points[8 * i + 7]) - points[8 * j + 7];

      // Coefficient of sqrt(s) in z*conj(z).
      I cross0 = 2 * (a * A + 33 * b * B + 3 * c * C + 99 * d * D);
      I cross1 = 2 * (a * B + b * A + 3 * c * D + 3 * d * C);
      if (cross0 != 0 || cross1 != 0) continue;

      // Norms of the base and extension coordinates in Q(sqrt(33)).
      I n00 = a * a + 33 * b * b + 3 * c * c + 99 * d * d;
      I n01 = 2 * a * b + 6 * c * d;
      I n10 = A * A + 33 * B * B + 3 * C * C + 99 * D * D;
      I n11 = 2 * A * B + 6 * C * D;
      I q0 = I(sd) * n00 + I(s0) * n10 + 33 * I(s1) * n11;
      I q1 = I(sd) * n01 + I(s0) * n11 + I(s1) * n10;
      if (q1 != 0 || q0 != I(sd) * den * den) continue;
      edges[2 * count] = i;
      edges[2 * count + 1] = j;
      ++count;
    }
  }
  return count;
}
