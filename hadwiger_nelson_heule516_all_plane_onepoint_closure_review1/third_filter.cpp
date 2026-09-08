// Independent exhaustive superset filter for unit-circumcircle triples.
//
// This reviewer implementation deliberately uses neither finite-field modulus
// from the reviewed filter.  An exact zero in Q(sqrt(3),sqrt(5),sqrt(11))
// maps to zero under each checked radical evaluation, so rejecting a triple
// whose circumradius polynomial is nonzero in either image is sound.
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using u64 = std::uint64_t;
using Point = std::array<std::int64_t, 16>;

struct Image {
    u64 modulus;
    std::array<u64, 3> roots;
    std::vector<u64> squared_distances;
};

bool is_prime(u64 n) {
    if (n < 2) return false;
    if ((n & 1U) == 0) return n == 2;
    for (u64 d = 3; d * d <= n; d += 2)
        if (n % d == 0) return false;
    return true;
}

u64 product(u64 a, u64 b, u64 p) {
    // The checked moduli are about 10^6, so a*b < 2^64.
    return (a * b) % p;
}

void build_image(Image& image, const std::vector<Point>& points) {
    const u64 p = image.modulus;
    if (!is_prime(p)) throw std::runtime_error("review modulus is not prime");
    const std::array<u64, 3> radicands{3, 5, 11};
    for (std::size_t bit = 0; bit < 3; ++bit)
        if (product(image.roots[bit], image.roots[bit], p) != radicands[bit])
            throw std::runtime_error("invalid radical image");

    std::array<u64, 8> basis{};
    for (unsigned mask = 0; mask < 8; ++mask) {
        basis[mask] = 1;
        for (unsigned bit = 0; bit < 3; ++bit)
            if ((mask >> bit) & 1U)
                basis[mask] = product(basis[mask], image.roots[bit], p);
    }

    std::vector<std::array<u64, 2>> projected(points.size());
    for (std::size_t v = 0; v < points.size(); ++v) {
        for (std::size_t axis = 0; axis < 2; ++axis) {
            u64 value = 0;
            for (std::size_t k = 0; k < 8; ++k) {
                const auto coefficient = points[v][8 * axis + k];
                const auto signed_modulus = static_cast<std::int64_t>(p);
                const u64 residue = static_cast<u64>(
                    (coefficient % signed_modulus + signed_modulus) % signed_modulus);
                value = (value + product(residue, basis[k], p)) % p;
            }
            projected[v][axis] = value;
        }
    }

    const std::size_t n = points.size();
    image.squared_distances.assign(n * n, 0);
    for (std::size_t i = 0; i < n; ++i) {
        for (std::size_t j = i + 1; j < n; ++j) {
            const u64 dx = (projected[i][0] + p - projected[j][0]) % p;
            const u64 dy = (projected[i][1] + p - projected[j][1]) % p;
            const u64 d = (product(dx, dx, p) + product(dy, dy, p)) % p;
            image.squared_distances[i * n + j] = d;
            image.squared_distances[j * n + i] = d;
        }
    }
}

bool radius_one(u64 s, u64 t, u64 u, u64 scale, const Image& image) {
    const u64 p = image.modulus;
    const u64 st = product(s, t, p);
    const u64 su = product(s, u, p);
    const u64 tu = product(t, u, p);
    const u64 twice_cross = (2 * ((st + su + tu) % p)) % p;
    const u64 squares = (product(s, s, p) + product(t, t, p) + product(u, u, p)) % p;
    const u64 heron = (twice_cross + p - squares) % p;
    const u64 left = product(product(s, t, p), u, p);
    const u64 scale_squared = product(scale % p, scale % p, p);
    return left == product(scale_squared, heron, p);
}

int main(int argc, char** argv) {
    try {
        if (argc != 3) throw std::runtime_error("usage: third_filter points.txt survivors.tsv");
        std::ifstream input(argv[1]);
        std::size_t n = 0;
        u64 scale = 0;
        if (!(input >> n >> scale) || n != 516 || scale != 96)
            throw std::runtime_error("expected exactly 516 points at scale 96");
        std::vector<Point> points(n);
        for (auto& point : points)
            for (auto& coefficient : point)
                if (!(input >> coefficient) || coefficient < -144 || coefficient > 144)
                    throw std::runtime_error("invalid coordinate coefficient");
        std::string trailing;
        if (input >> trailing) throw std::runtime_error("trailing input");

        // Both primes and all six roots were selected independently of the
        // reviewed implementation and are rechecked above.
        Image first{1001219, {107392, 354837, 845400}, {}};
        Image second{1001459, {862581, 914097, 361022}, {}};
        build_image(first, points);
        build_image(second, points);

        std::ofstream output(argv[2]);
        if (!output) throw std::runtime_error("cannot create survivor stream");
        u64 triples = 0;
        u64 first_survivors = 0;
        u64 second_survivors = 0;
        for (std::size_t i = 0; i < n; ++i) {
            for (std::size_t j = i + 1; j < n; ++j) {
                for (std::size_t k = j + 1; k < n; ++k) {
                    ++triples;
                    const u64 s1 = first.squared_distances[i * n + j];
                    const u64 t1 = first.squared_distances[i * n + k];
                    const u64 u1 = first.squared_distances[j * n + k];
                    if (!radius_one(s1, t1, u1, scale, first)) continue;
                    ++first_survivors;
                    const u64 s2 = second.squared_distances[i * n + j];
                    const u64 t2 = second.squared_distances[i * n + k];
                    const u64 u2 = second.squared_distances[j * n + k];
                    if (!radius_one(s2, t2, u2, scale, second)) continue;
                    ++second_survivors;
                    output << i << ' ' << j << ' ' << k << '\n';
                }
            }
        }
        output.close();
        if (!output) throw std::runtime_error("survivor stream write failure");
        std::cout << "{\"moduli\":[1001219,1001459],\"vertices\":" << n
                  << ",\"triples\":" << triples
                  << ",\"first_survivors\":" << first_survivors
                  << ",\"second_survivors\":" << second_survivors << "}\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
