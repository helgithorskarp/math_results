#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <map>
#include <numeric>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

using i64 = std::int64_t;
using i128 = __int128_t;
using Field = std::array<i64, 8>;

struct Point {
    Field x{}, y{};
    auto operator<=>(const Point&) const = default;
};

struct Vector {
    Field x{}, y{};
    auto operator<=>(const Vector&) const = default;
};

struct Orientation {
    bool reflected{};
    i64 denominator{};
    Field c{}, s{};
    auto operator<=>(const Orientation&) const = default;
};

static i64 narrow(i128 value) {
    const i128 low = std::numeric_limits<i64>::min();
    const i128 high = std::numeric_limits<i64>::max();
    if (value < low || value > high) throw std::overflow_error("int64 overflow");
    return static_cast<i64>(value);
}

static Field add(const Field& a, const Field& b) {
    Field out{};
    for (int i = 0; i < 8; ++i) out[i] = narrow(static_cast<i128>(a[i]) + b[i]);
    return out;
}

static Field subtract(const Field& a, const Field& b) {
    Field out{};
    for (int i = 0; i < 8; ++i) out[i] = narrow(static_cast<i128>(a[i]) - b[i]);
    return out;
}

static Field negate(const Field& a) {
    Field out{};
    for (int i = 0; i < 8; ++i) out[i] = narrow(-static_cast<i128>(a[i]));
    return out;
}

static Field multiply(const Field& a, const Field& b) {
    constexpr int primes[3] = {3, 5, 11};
    std::array<i128, 8> wide{};
    for (int i = 0; i < 8; ++i) {
        if (a[i] == 0) continue;
        for (int j = 0; j < 8; ++j) {
            if (b[j] == 0) continue;
            i128 term = static_cast<i128>(a[i]) * b[j];
            for (int bit = 0; bit < 3; ++bit) {
                if ((i & j) & (1 << bit)) term *= primes[bit];
            }
            wide[i ^ j] += term;
        }
    }
    Field out{};
    for (int i = 0; i < 8; ++i) out[i] = narrow(wide[i]);
    return out;
}

static Field squared_norm(const Vector& a) {
    return add(multiply(a.x, a.x), multiply(a.y, a.y));
}

static std::vector<Point> read_points(const std::string& path) {
    std::ifstream input(path);
    if (!input) throw std::runtime_error("cannot open points file");
    std::vector<Point> points;
    std::string line;
    while (std::getline(input, line)) {
        if (line.empty() || line[0] == '#') continue;
        std::istringstream row(line);
        Point point;
        for (i64& value : point.x) row >> value;
        for (i64& value : point.y) row >> value;
        std::string extra;
        if (!row || row >> extra) throw std::runtime_error("bad points row");
        points.push_back(point);
    }
    if (points.size() != 509) throw std::runtime_error("expected 509 points");
    return points;
}

using VectorsByDistance = std::map<Field, std::set<Vector>>;

static VectorsByDistance directed_vectors(const std::vector<Point>& points) {
    VectorsByDistance result;
    for (std::size_t i = 0; i < points.size(); ++i) {
        for (std::size_t j = 0; j < i; ++j) {
            Vector vector{subtract(points[i].x, points[j].x), subtract(points[i].y, points[j].y)};
            const Field distance = squared_norm(vector);
            result[distance].insert(vector);
            result[distance].insert(Vector{negate(vector.x), negate(vector.y)});
        }
    }
    return result;
}

static i64 absolute(i64 value) {
    if (value == std::numeric_limits<i64>::min()) throw std::overflow_error("abs overflow");
    return value < 0 ? -value : value;
}

static Orientation make_orientation(bool reflected, const Field& nc, const Field& ns, const Field& distance) {
    for (int i = 0; i < 8; ++i) {
        if (i != 0 && i != 5 && distance[i] != 0) {
            throw std::runtime_error("common distance escaped Q(sqrt(33))");
        }
    }
    const i64 d0 = distance[0], d5 = distance[5];
    const i64 denominator = narrow(static_cast<i128>(d0) * d0 - static_cast<i128>(33) * d5 * d5);
    Field conjugate{};
    conjugate[0] = d0;
    conjugate[5] = -d5;
    Field c = multiply(nc, conjugate);
    Field s = multiply(ns, conjugate);
    i64 divisor = absolute(denominator);
    for (i64 value : c) divisor = std::gcd(divisor, absolute(value));
    for (i64 value : s) divisor = std::gcd(divisor, absolute(value));
    i64 reduced_denominator = denominator / divisor;
    for (i64& value : c) value /= divisor;
    for (i64& value : s) value /= divisor;
    if (reduced_denominator < 0) {
        reduced_denominator = -reduced_denominator;
        c = negate(c);
        s = negate(s);
    }
    return Orientation{reflected, reduced_denominator, c, s};
}

static std::set<Orientation> enumerate_orientations(
    const VectorsByDistance& left,
    const VectorsByDistance& right
) {
    std::set<Orientation> result;
    for (const auto& [distance, left_vectors] : left) {
        const auto found = right.find(distance);
        if (found == right.end()) continue;
        for (const Vector& a : left_vectors) {
            for (const Vector& b : found->second) {
                const Field rotation_c = add(multiply(a.x, b.x), multiply(a.y, b.y));
                const Field rotation_s = subtract(multiply(b.x, a.y), multiply(b.y, a.x));
                result.insert(make_orientation(false, rotation_c, rotation_s, distance));
                const Field reflection_c = subtract(multiply(a.x, b.x), multiply(a.y, b.y));
                const Field reflection_s = add(multiply(a.x, b.y), multiply(a.y, b.x));
                result.insert(make_orientation(true, reflection_c, reflection_s, distance));
            }
        }
    }
    return result;
}

struct Difference {
    Field x{}, y{};
    bool operator==(const Difference&) const = default;
};

static std::uint64_t mix(std::uint64_t value) {
    value ^= value >> 30;
    value *= UINT64_C(0xbf58476d1ce4e5b9);
    value ^= value >> 27;
    value *= UINT64_C(0x94d049bb133111eb);
    return value ^ (value >> 31);
}

struct DifferenceHash {
    std::size_t operator()(const Difference& difference) const {
        std::uint64_t hash = UINT64_C(0x9e3779b97f4a7c15);
        for (i64 value : difference.x) hash = mix(hash ^ mix(static_cast<std::uint64_t>(value)));
        for (i64 value : difference.y) hash = mix(hash ^ mix(static_cast<std::uint64_t>(value)));
        return static_cast<std::size_t>(hash);
    }
};

static Point transformed_numerator(const Orientation& orientation, const Point& point) {
    const Field cx = multiply(orientation.c, point.x);
    const Field sy = multiply(orientation.s, point.y);
    const Field sx = multiply(orientation.s, point.x);
    const Field cy = multiply(orientation.c, point.y);
    if (orientation.reflected) return Point{add(cx, sy), subtract(sx, cy)};
    return Point{subtract(cx, sy), add(sx, cy)};
}

static Difference cross_difference(
    const Point& left,
    const Point& transformed_right,
    i64 denominator
) {
    Difference difference;
    for (int i = 0; i < 8; ++i) {
        difference.x[i] = narrow(static_cast<i128>(denominator) * left.x[i] - transformed_right.x[i]);
        difference.y[i] = narrow(static_cast<i128>(denominator) * left.y[i] - transformed_right.y[i]);
    }
    return difference;
}

static void print_field(const Field& value) {
    for (int i = 0; i < 8; ++i) {
        if (i) std::cout << ',';
        std::cout << value[i];
    }
}

int main(int argc, char** argv) {
    if (argc != 2) {
        std::cerr << "usage: enumerate_overlaps POINTS.tsv\n";
        return 2;
    }
    const std::vector<Point> all = read_points(argv[1]);
    const std::vector<Point> left(all.begin(), all.begin() + 374);
    std::vector<Point> small;
    small.reserve(136);
    small.push_back(all[0]);
    small.insert(small.end(), all.begin() + 374, all.end());

    const VectorsByDistance left_vectors = directed_vectors(left);
    const VectorsByDistance small_vectors = directed_vectors(small);
    const std::set<Orientation> orientation_set = enumerate_orientations(left_vectors, small_vectors);
    const std::vector<Orientation> orientations(orientation_set.begin(), orientation_set.end());
    std::size_t rotations = 0;
    for (const Orientation& orientation : orientations) rotations += !orientation.reflected;
    std::cout << "overlap_induced_rotations=" << rotations << '\n';
    std::cout << "overlap_induced_reflections=" << orientations.size() - rotations << '\n';

    std::size_t left_vector_count = 0, small_vector_count = 0;
    for (const auto& [distance, vectors] : left_vectors) {
        (void)distance;
        left_vector_count += vectors.size();
    }
    for (const auto& [distance, vectors] : small_vectors) {
        (void)distance;
        small_vector_count += vectors.size();
    }
    std::cout << "distinct_nonzero_L_vectors=" << left_vector_count << '\n';
    std::cout << "distinct_nonzero_S_vectors=" << small_vector_count << '\n';

    std::map<unsigned, std::uint64_t> overlap_histogram;
    std::uint64_t pair_certificates = 0;
    std::uint64_t candidate_placements = 0;
    std::uint64_t orientation_index = 0;
    for (const Orientation& orientation : orientations) {
        std::vector<Point> image;
        image.reserve(small.size());
        for (const Point& point : small) image.push_back(transformed_numerator(orientation, point));
        std::unordered_map<Difference, std::uint16_t, DifferenceHash> multiplicities;
        multiplicities.reserve(left.size() * small.size() * 2);
        for (const Point& p : left) {
            for (const Point& q : image) {
                ++multiplicities[cross_difference(p, q, orientation.denominator)];
            }
        }
        std::uint64_t local_candidates = 0;
        for (const auto& [difference, multiplicity] : multiplicities) {
            if (multiplicity >= 2) {
                ++overlap_histogram[multiplicity];
                ++local_candidates;
                pair_certificates += static_cast<std::uint64_t>(multiplicity) * (multiplicity - 1) / 2;
                if (multiplicity >= 84) {
                    std::cout << "high_overlap=" << multiplicity
                              << ";reflected=" << orientation.reflected
                              << ";denominator=" << orientation.denominator << ";c=";
                    print_field(orientation.c);
                    std::cout << ";s=";
                    print_field(orientation.s);
                    std::cout << ";tx=";
                    print_field(difference.x);
                    std::cout << ";ty=";
                    print_field(difference.y);
                    std::cout << '\n';
                }
            }
        }
        candidate_placements += local_candidates;
        ++orientation_index;
        if (orientation_index % 100 == 0) {
            std::cerr << "processed_orientations=" << orientation_index << '/' << orientations.size() << '\n';
        }
    }

    std::cout << "affine_placements_with_at_least_two_overlaps=" << candidate_placements << '\n';
    std::cout << "recovered_pair_certificates=" << pair_certificates << '\n';
    for (const auto& [overlaps, count] : overlap_histogram) {
        std::cout << "overlap_multiplicity_" << overlaps << '=' << count << '\n';
    }
    if (orientations.size() != 2840 || rotations != 1420 || pair_certificates != 17658256) {
        throw std::runtime_error("enumeration failed an inherited exact count");
    }
    std::cout << "exact_overlap_enumeration=true\n";
}
