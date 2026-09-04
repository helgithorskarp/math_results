#include <algorithm>
#include <array>
#include <compare>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <map>
#include <numeric>
#include <optional>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
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

struct Difference {
    Field x{}, y{};
    bool operator==(const Difference&) const = default;
};

struct Bucket {
    i64 x{}, y{};
    bool operator==(const Bucket&) const = default;
};

struct ColourLibraries {
    std::vector<std::vector<std::uint8_t>> left;
    std::vector<std::vector<std::uint8_t>> small;
};

static i64 narrow(i128 value) {
    if (value < std::numeric_limits<i64>::min() || value > std::numeric_limits<i64>::max()) {
        throw std::overflow_error("int64 overflow");
    }
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
        if (!a[i]) continue;
        for (int j = 0; j < 8; ++j) {
            if (!b[j]) continue;
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

static Field squared_norm(const Vector& vector) {
    return add(multiply(vector.x, vector.x), multiply(vector.y, vector.y));
}

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

struct BucketHash {
    std::size_t operator()(const Bucket& bucket) const {
        return static_cast<std::size_t>(mix(static_cast<std::uint64_t>(bucket.x))
                                      ^ mix(static_cast<std::uint64_t>(bucket.y)));
    }
};

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

static ColourLibraries read_colour_libraries(const std::string& path) {
    std::ifstream input(path);
    if (!input) throw std::runtime_error("cannot open colour-library file");
    ColourLibraries libraries;
    std::string line;
    while (std::getline(input, line)) {
        if (line.empty()) continue;
        std::vector<std::uint8_t>* destination = nullptr;
        std::size_t expected_size = 0;
        if (line.starts_with("L:")) {
            libraries.left.emplace_back();
            destination = &libraries.left.back();
            expected_size = 374;
        } else if (line.starts_with("S:")) {
            libraries.small.emplace_back();
            destination = &libraries.small.back();
            expected_size = 136;
        } else {
            throw std::runtime_error("bad colour-library row prefix");
        }
        if (line.size() != expected_size + 2) {
            throw std::runtime_error("bad colour-library row length");
        }
        destination->reserve(expected_size);
        for (char value : line.substr(2)) {
            if (value < '0' || value > '3') {
                throw std::runtime_error("bad colour-library value");
            }
            destination->push_back(static_cast<std::uint8_t>(value - '0'));
        }
    }
    if (libraries.left.size() != 135 || libraries.small.size() != 194) {
        throw std::runtime_error("colour-library census mismatch");
    }
    return libraries;
}

using VectorsByDistance = std::map<Field, std::set<Vector>>;

static VectorsByDistance directed_vectors(const std::vector<Point>& points) {
    VectorsByDistance result;
    for (std::size_t i = 0; i < points.size(); ++i) {
        for (std::size_t j = 0; j < i; ++j) {
            const Vector vector{subtract(points[i].x, points[j].x),
                                subtract(points[i].y, points[j].y)};
            const Field distance = squared_norm(vector);
            result[distance].insert(vector);
            result[distance].insert(Vector{negate(vector.x), negate(vector.y)});
        }
    }
    return result;
}

static std::size_t vector_count(const VectorsByDistance& vectors) {
    std::size_t result = 0;
    for (const auto& [distance, members] : vectors) {
        (void)distance;
        result += members.size();
    }
    return result;
}

static i64 absolute(i64 value) {
    if (value == std::numeric_limits<i64>::min()) throw std::overflow_error("abs overflow");
    return value < 0 ? -value : value;
}

static Orientation make_orientation(
    bool reflected,
    const Field& numerator_c,
    const Field& numerator_s,
    const Field& distance
) {
    for (int i = 0; i < 8; ++i) {
        if (i != 0 && i != 5 && distance[i] != 0) {
            throw std::runtime_error("common distance escaped Q(sqrt(33))");
        }
    }
    const i64 d0 = distance[0], d5 = distance[5];
    const i64 denominator = narrow(static_cast<i128>(d0) * d0
                                 - static_cast<i128>(33) * d5 * d5);
    Field conjugate{};
    conjugate[0] = d0;
    conjugate[5] = -d5;
    Field c = multiply(numerator_c, conjugate);
    Field s = multiply(numerator_s, conjugate);
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
        difference.x[i] = narrow(static_cast<i128>(denominator) * left.x[i]
                               - transformed_right.x[i]);
        difference.y[i] = narrow(static_cast<i128>(denominator) * left.y[i]
                               - transformed_right.y[i]);
    }
    return difference;
}

static std::vector<std::vector<bool>> internal_edges(const std::vector<Point>& points) {
    Field unit{};
    unit[0] = 96 * 96;
    std::vector<std::vector<bool>> result(points.size(), std::vector<bool>(points.size()));
    for (std::size_t u = 0; u < points.size(); ++u) {
        for (std::size_t v = u + 1; v < points.size(); ++v) {
            const Vector difference{subtract(points[u].x, points[v].x),
                                    subtract(points[u].y, points[v].y)};
            if (squared_norm(difference) == unit) result[u][v] = result[v][u] = true;
        }
    }
    return result;
}

static std::size_t edge_count(const std::vector<std::vector<bool>>& edges) {
    std::size_t result = 0;
    for (std::size_t u = 0; u < edges.size(); ++u) {
        for (std::size_t v = u + 1; v < edges.size(); ++v) result += edges[u][v];
    }
    return result;
}

static void validate_colour_library(
    const std::vector<std::vector<std::uint8_t>>& colourings,
    const std::vector<std::vector<bool>>& edges
) {
    for (const auto& colours : colourings) {
        if (colours.size() != edges.size()) {
            throw std::runtime_error("colour-library graph order mismatch");
        }
        for (std::size_t u = 0; u < edges.size(); ++u) {
            for (std::size_t v = u + 1; v < edges.size(); ++v) {
                if (edges[u][v] && colours[u] == colours[v]) {
                    throw std::runtime_error("improper colour-library witness");
                }
            }
        }
    }
}

template <std::size_t VertexCount>
using PatternMask = std::array<std::uint64_t, (std::size_t{1} << (2 * VertexCount)) / 64>;

template <std::size_t VertexCount>
using CompatibilityTable = std::array<
    PatternMask<VertexCount>, std::size_t{1} << (2 * VertexCount)
>;

template <std::size_t VertexCount>
static CompatibilityTable<VertexCount> make_compatibility_table() {
    constexpr int pattern_count = 1 << (2 * VertexCount);
    CompatibilityTable<VertexCount> compatible{};
    for (int small_pattern = 0; small_pattern < pattern_count; ++small_pattern) {
        std::array<int, VertexCount> small_colours{};
        for (std::size_t i = 0; i < VertexCount; ++i) {
            small_colours[i] = (small_pattern >> (2 * i)) & 3;
        }
        for (int left_pattern = 0; left_pattern < pattern_count; ++left_pattern) {
            std::array<int, VertexCount> left_colours{};
            for (std::size_t i = 0; i < VertexCount; ++i) {
                left_colours[i] = (left_pattern >> (2 * i)) & 3;
            }
            std::array<int, 4> permutation{0, 1, 2, 3};
            bool works = false;
            do {
                works = permutation[small_colours[0]] == left_colours[0]
                     && permutation[small_colours[1]] == left_colours[1]
                     && std::equal(
                            small_colours.begin() + 2, small_colours.end(),
                            left_colours.begin() + 2,
                            [&permutation](int small, int left) {
                                return permutation[small] != left;
                            }
                        );
                if (works) break;
            } while (std::next_permutation(permutation.begin(), permutation.end()));
            if (works) {
                compatible[small_pattern][left_pattern / 64]
                    |= UINT64_C(1) << (left_pattern % 64);
            }
        }
    }
    return compatible;
}

template <std::size_t VertexCount>
struct CanonicalCompatibilityTable {
    static constexpr std::size_t raw_pattern_count =
        std::size_t{1} << (2 * VertexCount);
    std::array<std::uint16_t, raw_pattern_count> rank_by_raw_pattern{};
    std::vector<std::vector<std::uint64_t>> compatible;
    std::size_t compatible_pair_count{};
};

template <std::size_t VertexCount>
static int canonical_colour_pattern(int pattern) {
    std::array<int, 4> renamed{-1, -1, -1, -1};
    int next_colour = 0;
    int canonical = 0;
    for (std::size_t i = 0; i < VertexCount; ++i) {
        const int colour = (pattern >> (2 * i)) & 3;
        if (renamed[colour] < 0) renamed[colour] = next_colour++;
        canonical |= renamed[colour] << (2 * i);
    }
    return canonical;
}

template <std::size_t VertexCount>
static CanonicalCompatibilityTable<VertexCount>
make_canonical_compatibility_table() {
    constexpr int raw_pattern_count = 1 << (2 * VertexCount);
    std::set<int> representative_set;
    for (int pattern = 0; pattern < raw_pattern_count; ++pattern) {
        representative_set.insert(canonical_colour_pattern<VertexCount>(pattern));
    }
    const std::vector<int> representatives(
        representative_set.begin(), representative_set.end()
    );
    if (representatives.size() > std::numeric_limits<std::uint16_t>::max()) {
        throw std::runtime_error("too many canonical colour patterns");
    }
    CanonicalCompatibilityTable<VertexCount> result;
    for (int pattern = 0; pattern < raw_pattern_count; ++pattern) {
        const int canonical = canonical_colour_pattern<VertexCount>(pattern);
        const auto found = std::lower_bound(
            representatives.begin(), representatives.end(), canonical
        );
        if (found == representatives.end() || *found != canonical) {
            throw std::runtime_error("missing canonical colour pattern");
        }
        result.rank_by_raw_pattern[pattern] = static_cast<std::uint16_t>(
            found - representatives.begin()
        );
    }
    const std::size_t word_count = (representatives.size() + 63) / 64;
    result.compatible.assign(
        representatives.size(), std::vector<std::uint64_t>(word_count)
    );
    for (std::size_t small_rank = 0; small_rank < representatives.size(); ++small_rank) {
        std::array<int, VertexCount> small_colours{};
        for (std::size_t i = 0; i < VertexCount; ++i) {
            small_colours[i] = (representatives[small_rank] >> (2 * i)) & 3;
        }
        for (std::size_t left_rank = 0; left_rank < representatives.size(); ++left_rank) {
            std::array<int, VertexCount> left_colours{};
            for (std::size_t i = 0; i < VertexCount; ++i) {
                left_colours[i] = (representatives[left_rank] >> (2 * i)) & 3;
            }
            std::array<int, 4> permutation{0, 1, 2, 3};
            bool works = false;
            do {
                works = permutation[small_colours[0]] == left_colours[0]
                     && permutation[small_colours[1]] == left_colours[1]
                     && std::equal(
                            small_colours.begin() + 2, small_colours.end(),
                            left_colours.begin() + 2,
                            [&permutation](int small, int left) {
                                return permutation[small] != left;
                            }
                        );
                if (works) break;
            } while (std::next_permutation(permutation.begin(), permutation.end()));
            if (works) {
                result.compatible[small_rank][left_rank / 64]
                    |= UINT64_C(1) << (left_rank % 64);
                ++result.compatible_pair_count;
            }
        }
    }
    return result;
}

template <std::size_t VertexCount>
static int colour_pattern(
    const std::vector<std::uint8_t>& colours,
    const std::array<std::size_t, VertexCount>& vertices
) {
    int pattern = 0;
    for (std::size_t i = 0; i < VertexCount; ++i) {
        pattern |= colours[vertices[i]] << (2 * i);
    }
    return pattern;
}

template <std::size_t CrossEdgeCount>
static bool absorbed_by_colour_libraries(
    const std::vector<std::uint32_t>& overlaps,
    const std::array<std::uint32_t, 6>& genuine_keys,
    const ColourLibraries& libraries,
    const CompatibilityTable<2 + CrossEdgeCount>& compatible
) {
    if (overlaps.size() != 2) throw std::runtime_error("bad overlap count");
    std::array<std::size_t, 2 + CrossEdgeCount> left_vertices{};
    std::array<std::size_t, 2 + CrossEdgeCount> small_vertices{};
    left_vertices[0] = overlaps[0] / 136;
    left_vertices[1] = overlaps[1] / 136;
    small_vertices[0] = overlaps[0] % 136;
    small_vertices[1] = overlaps[1] % 136;
    for (std::size_t edge = 0; edge < CrossEdgeCount; ++edge) {
        left_vertices[edge + 2] = genuine_keys[edge] / 510;
        small_vertices[edge + 2] = genuine_keys[edge] % 510 - 374;
    }
    PatternMask<2 + CrossEdgeCount> left_patterns{};
    for (const auto& colours : libraries.left) {
        const int pattern = colour_pattern(colours, left_vertices);
        left_patterns[pattern / 64] |= UINT64_C(1) << (pattern % 64);
    }
    for (const auto& colours : libraries.small) {
        const int pattern = colour_pattern(colours, small_vertices);
        for (std::size_t word = 0; word < left_patterns.size(); ++word) {
            if (left_patterns[word] & compatible[pattern][word]) return true;
        }
    }
    return false;
}

template <std::size_t CrossEdgeCount>
static bool absorbed_by_canonical_colour_libraries(
    const std::vector<std::uint32_t>& overlaps,
    const std::array<std::uint32_t, 6>& genuine_keys,
    const ColourLibraries& libraries,
    const CanonicalCompatibilityTable<2 + CrossEdgeCount>& compatible
) {
    if (overlaps.size() != 2) throw std::runtime_error("bad overlap count");
    std::array<std::size_t, 2 + CrossEdgeCount> left_vertices{};
    std::array<std::size_t, 2 + CrossEdgeCount> small_vertices{};
    left_vertices[0] = overlaps[0] / 136;
    left_vertices[1] = overlaps[1] / 136;
    small_vertices[0] = overlaps[0] % 136;
    small_vertices[1] = overlaps[1] % 136;
    for (std::size_t edge = 0; edge < CrossEdgeCount; ++edge) {
        left_vertices[edge + 2] = genuine_keys[edge] / 510;
        small_vertices[edge + 2] = genuine_keys[edge] % 510 - 374;
    }
    std::vector<std::uint64_t> left_patterns(compatible.compatible.front().size());
    for (const auto& colours : libraries.left) {
        const int pattern = colour_pattern(colours, left_vertices);
        const std::size_t rank = compatible.rank_by_raw_pattern[pattern];
        left_patterns[rank / 64] |= UINT64_C(1) << (rank % 64);
    }
    for (const auto& colours : libraries.small) {
        const int pattern = colour_pattern(colours, small_vertices);
        const std::size_t rank = compatible.rank_by_raw_pattern[pattern];
        for (std::size_t word = 0; word < left_patterns.size(); ++word) {
            if (left_patterns[word] & compatible.compatible[rank][word]) return true;
        }
    }
    return false;
}

// Exact lower bounds floor(sqrt(n)*10^12), indexed by the radical basis.
constexpr i128 ROOT_SCALE = INT64_C(1000000000000);
constexpr std::array<i64, 8> RADICANDS{1, 3, 5, 15, 11, 33, 55, 165};
constexpr std::array<i64, 8> ROOT_FLOORS{
    INT64_C(1000000000000), INT64_C(1732050807568),
    INT64_C(2236067977499), INT64_C(3872983346207),
    INT64_C(3316624790355), INT64_C(5744562646538),
    INT64_C(7416198487095), INT64_C(12845232578665),
};

static void check_radical_bounds() {
    for (int i = 1; i < 8; ++i) {
        const i128 lower = ROOT_FLOORS[i];
        const i128 target = static_cast<i128>(RADICANDS[i]) * ROOT_SCALE * ROOT_SCALE;
        if (!(lower * lower < target && target < (lower + 1) * (lower + 1))) {
            throw std::runtime_error("invalid rational radical bound");
        }
    }
}

static i128 lower_scaled_value(const Field& value) {
    i128 result = static_cast<i128>(value[0]) * ROOT_SCALE;
    for (int i = 1; i < 8; ++i) {
        const i128 bound = value[i] >= 0 ? ROOT_FLOORS[i] : ROOT_FLOORS[i] + 1;
        result += static_cast<i128>(value[i]) * bound;
    }
    return result;
}

static i128 uncertain_width(const Field& value) {
    i128 result = 0;
    for (int i = 1; i < 8; ++i) result += absolute(value[i]);
    return result;
}

struct RadicalInterval {
    i128 lower{};
    i128 width{};
};

static RadicalInterval radical_interval(const Field& value) {
    return RadicalInterval{lower_scaled_value(value), uncertain_width(value)};
}

static i128 floor_divide(i128 numerator, i128 denominator) {
    if (denominator <= 0) throw std::runtime_error("nonpositive floor divisor");
    i128 quotient = numerator / denominator;
    const i128 remainder = numerator % denominator;
    if (remainder < 0) --quotient;
    return quotient;
}

static i64 bucket_coordinate(const RadicalInterval& interval, i64 denominator) {
    const i128 coordinate_denominator = ROOT_SCALE * 96 * denominator;
    // The exact coordinate is less than 1/1000 above its certified lower bound.
    if (1000 * interval.width >= coordinate_denominator) {
        throw std::runtime_error("radical interval too wide for certified bucket search");
    }
    return narrow(floor_divide(4 * interval.lower, coordinate_denominator));
}

static Bucket bucket(
    const RadicalInterval& x,
    const RadicalInterval& y,
    i64 denominator
) {
    return Bucket{bucket_coordinate(x, denominator), bucket_coordinate(y, denominator)};
}

static bool unit_separated(const Difference& a, const Difference& b, i64 denominator) {
    Field unit{};
    unit[0] = narrow(static_cast<i128>(96) * 96 * denominator * denominator);
    const Vector difference{subtract(a.x, b.x), subtract(a.y, b.y)};
    return squared_norm(difference) == unit;
}

static i128 absolute128(i128 value) {
    return value < 0 ? -value : value;
}

static std::pair<i128, i128> square_range(i128 low, i128 high) {
    // Twice SAFE^2 remains below the signed-int128 maximum.
    constexpr i128 SAFE = static_cast<i128>(6000000000000000000LL);
    if (low > high || absolute128(low) >= SAFE || absolute128(high) >= SAFE) {
        throw std::overflow_error("interval square outside certified int128 range");
    }
    const i128 low_square = low * low, high_square = high * high;
    const i128 minimum = low <= 0 && high >= 0 ? 0 : std::min(low_square, high_square);
    return {minimum, std::max(low_square, high_square)};
}

static bool interval_can_be_unit(
    const RadicalInterval& ax,
    const RadicalInterval& ay,
    const RadicalInterval& bx,
    const RadicalInterval& by,
    i64 denominator
) {
    const auto [x_minimum, x_maximum] = square_range(
        ax.lower - bx.lower - bx.width,
        ax.lower + ax.width - bx.lower
    );
    const auto [y_minimum, y_maximum] = square_range(
        ay.lower - by.lower - by.width,
        ay.lower + ay.width - by.lower
    );
    const i128 coordinate_denominator = ROOT_SCALE * 96 * denominator;
    constexpr i128 SAFE = static_cast<i128>(6000000000000000000LL);
    if (coordinate_denominator >= SAFE) {
        throw std::overflow_error("unit interval outside certified int128 range");
    }
    const i128 unit_square = coordinate_denominator * coordinate_denominator;
    return x_minimum + y_minimum <= unit_square && unit_square <= x_maximum + y_maximum;
}

static bool bucket_offset_can_be_unit(i64 offset_x, i64 offset_y) {
    // Scale 4000: a bucket has width 1000 and the certified radical error is < 4.
    const auto square_bounds = [](i64 offset) {
        const i64 low = (offset - 1) * 1000 - 4;
        const i64 high = (offset + 1) * 1000 + 4;
        const i64 low_square = low * low, high_square = high * high;
        const i64 minimum = low <= 0 && high >= 0 ? 0 : std::min(low_square, high_square);
        return std::pair<i64, i64>{minimum, std::max(low_square, high_square)};
    };
    const auto [x_minimum, x_maximum] = square_bounds(offset_x);
    const auto [y_minimum, y_maximum] = square_bounds(offset_y);
    constexpr i64 UNIT = 4000 * 4000;
    return x_minimum + y_minimum <= UNIT && UNIT <= x_maximum + y_maximum;
}

static std::optional<std::uint32_t> new_strict_edge_key(
    std::uint32_t cross_pair,
    const std::vector<std::uint32_t>& overlaps,
    const std::vector<std::vector<bool>>& left_edges,
    const std::vector<std::vector<bool>>& small_edges
) {
    const std::size_t p = cross_pair / 136;
    const std::size_t q = cross_pair % 136;
    std::size_t q_vertex = 374 + q;
    for (std::uint32_t overlap : overlaps) {
        const std::size_t overlap_p = overlap / 136;
        const std::size_t overlap_q = overlap % 136;
        if (q == overlap_q) {
            q_vertex = overlap_p;
            if (left_edges[p][overlap_p]) return std::nullopt;
        }
        if (p == overlap_p && small_edges[q][overlap_q]) return std::nullopt;
    }
    const std::size_t u = std::min(p, q_vertex), v = std::max(p, q_vertex);
    if (u == v) throw std::runtime_error("unit cross edge collapsed to a loop");
    return static_cast<std::uint32_t>(510 * u + v);
}

struct BucketNode {
    const Difference* difference{};
    const std::vector<std::uint32_t>* pairs{};
    RadicalInterval x{}, y{};
};

int main(int argc, char** argv) {
    if (argc != 3 && argc != 4) {
        std::cerr << "usage: census POINTS.tsv COLOUR_LIBRARIES.txt"
                  << " [--through-three|--through-four|--through-five]\n";
        return 2;
    }
    int through_edges = 2;
    if (argc == 4 && std::string(argv[3]) == "--through-three") through_edges = 3;
    if (argc == 4 && std::string(argv[3]) == "--through-four") through_edges = 4;
    if (argc == 4 && std::string(argv[3]) == "--through-five") through_edges = 5;
    if (argc == 4 && through_edges == 2) {
        std::cerr << "unknown census mode: " << argv[3] << '\n';
        return 2;
    }
    const std::size_t genuine_cutoff = static_cast<std::size_t>(through_edges + 1);
    check_radical_bounds();
    const std::vector<Point> all = read_points(argv[1]);
    const std::vector<Point> left(all.begin(), all.begin() + 374);
    std::vector<Point> small;
    small.push_back(all[0]);
    small.insert(small.end(), all.begin() + 374, all.end());
    if (std::set<Point>(left.begin(), left.end()).size() != left.size()
        || std::set<Point>(small.begin(), small.end()).size() != small.size()) {
        throw std::runtime_error("gadget points are not distinct");
    }
    const auto left_edges = internal_edges(left);
    const auto small_edges = internal_edges(small);
    if (edge_count(left_edges) != 1860 || edge_count(small_edges) != 564) {
        throw std::runtime_error("internal edge census mismatch");
    }
    const ColourLibraries colour_libraries = read_colour_libraries(argv[2]);
    validate_colour_library(colour_libraries.left, left_edges);
    validate_colour_library(colour_libraries.small, small_edges);
    const auto compatible_two = make_compatibility_table<4>();
    const auto compatible_three = make_compatibility_table<5>();
    const auto compatible_four = make_compatibility_table<6>();
    std::optional<CanonicalCompatibilityTable<7>> compatible_five;
    if (through_edges >= 5) {
        compatible_five.emplace(make_canonical_compatibility_table<7>());
        if (compatible_five->compatible.size() != 715
            || compatible_five->compatible_pair_count != 124925) {
            throw std::runtime_error("seven-label partition census mismatch");
        }
    }
    const auto left_vectors = directed_vectors(left);
    const auto small_vectors = directed_vectors(small);
    if (vector_count(left_vectors) != 11650 || vector_count(small_vectors) != 1666) {
        throw std::runtime_error("directed-vector census mismatch");
    }
    const auto orientation_set = enumerate_orientations(left_vectors, small_vectors);
    const std::vector<Orientation> orientations(orientation_set.begin(), orientation_set.end());
    if (orientations.size() != 2840) throw std::runtime_error("orientation census mismatch");
    const std::size_t rotations = std::count_if(
        orientations.begin(), orientations.end(),
        [](const Orientation& orientation) { return !orientation.reflected; }
    );
    if (rotations != 1420) throw std::runtime_error("rotation/reflection census mismatch");
    std::cout << "overlap_induced_rotations=" << rotations << '\n';
    std::cout << "overlap_induced_reflections=" << orientations.size() - rotations << '\n';
    std::cout << "distinct_nonzero_L_vectors=" << vector_count(left_vectors) << '\n';
    std::cout << "distinct_nonzero_S_vectors=" << vector_count(small_vectors) << '\n';
    std::cout << "internal_L_edges=" << edge_count(left_edges) << '\n';
    std::cout << "internal_Splus_edges=" << edge_count(small_edges) << '\n';
    std::cout << "explicit_L_colourings=" << colour_libraries.left.size() << '\n';
    std::cout << "explicit_Splus_colourings=" << colour_libraries.small.size() << '\n';
    if (through_edges >= 5) {
        std::cout << "canonical_seven_label_colour_partitions="
                  << compatible_five->compatible.size() << '\n';
        std::cout << "compatible_seven_label_partition_pairs="
                  << compatible_five->compatible_pair_count << '\n';
    }

    std::uint64_t total_multi_overlap = 0;
    std::uint64_t pair_certificates = 0;
    std::uint64_t total_two = 0;
    std::uint64_t total_with_cross = 0;
    std::uint64_t total_with_genuine = 0;
    std::array<std::uint64_t, 7> total_genuine_categories{};
    std::array<std::uint64_t, 3> total_two_edge_topologies{};
    std::array<std::uint64_t, 4> total_disjoint_adjacencies{};
    std::uint64_t total_two_absorbed = 0;
    std::array<std::uint64_t, 3> total_two_absorbed_by_topology{};
    std::array<std::uint64_t, 6> total_three_edge_topologies{};
    std::uint64_t total_three_absorbed = 0;
    std::array<std::uint64_t, 6> total_three_absorbed_by_topology{};
    std::array<std::uint64_t, 11> total_four_edge_profiles{};
    std::uint64_t total_four_absorbed = 0;
    std::array<std::uint64_t, 11> total_four_absorbed_by_profile{};
    std::uint64_t total_five_absorbed = 0;
    std::uint64_t interval_candidates = 0;
    std::uint64_t exact_distance_checks = 0;
    std::vector<std::pair<i64, i64>> bucket_offsets;
    for (i64 dx = -6; dx <= 6; ++dx) {
        for (i64 dy = -6; dy <= 6; ++dy) {
            if (bucket_offset_can_be_unit(dx, dy)) bucket_offsets.emplace_back(dx, dy);
        }
    }
    if (bucket_offsets.size() != 68) throw std::runtime_error("bucket-offset census mismatch");
    for (std::size_t orientation_index = 0; orientation_index < orientations.size(); ++orientation_index) {
        const Orientation& orientation = orientations[orientation_index];
        std::vector<Point> image;
        image.reserve(small.size());
        for (const Point& point : small) image.push_back(transformed_numerator(orientation, point));

        std::unordered_map<Difference, std::vector<std::uint32_t>, DifferenceHash> differences;
        differences.reserve(left.size() * small.size() * 2);
        for (std::size_t p = 0; p < left.size(); ++p) {
            for (std::size_t q = 0; q < image.size(); ++q) {
                differences[cross_difference(left[p], image[q], orientation.denominator)]
                    .push_back(static_cast<std::uint32_t>(136 * p + q));
            }
        }
        for (const auto& [difference, pairs] : differences) {
            (void)difference;
            if (pairs.size() < 2) continue;
            ++total_multi_overlap;
            pair_certificates += pairs.size() * (pairs.size() - 1) / 2;
        }

        std::unordered_map<Bucket, std::vector<BucketNode>, BucketHash> grid;
        grid.reserve(differences.size() * 2);
        for (const auto& [difference, pairs] : differences) {
            const RadicalInterval x = radical_interval(difference.x);
            const RadicalInterval y = radical_interval(difference.y);
            grid[bucket(x, y, orientation.denominator)].push_back(
                BucketNode{&difference, &pairs, x, y}
            );
        }

        std::uint64_t local_two = 0;
        std::uint64_t local_with_cross = 0;
        std::uint64_t local_with_genuine = 0;
        std::array<std::uint64_t, 7> local_genuine_categories{};
        std::array<std::uint64_t, 3> local_two_edge_topologies{};
        std::array<std::uint64_t, 4> local_disjoint_adjacencies{};
        std::uint64_t local_two_absorbed = 0;
        std::array<std::uint64_t, 3> local_two_absorbed_by_topology{};
        std::array<std::uint64_t, 6> local_three_edge_topologies{};
        std::uint64_t local_three_absorbed = 0;
        std::array<std::uint64_t, 6> local_three_absorbed_by_topology{};
        std::array<std::uint64_t, 11> local_four_edge_profiles{};
        std::uint64_t local_four_absorbed = 0;
        std::array<std::uint64_t, 11> local_four_absorbed_by_profile{};
        std::uint64_t local_five_absorbed = 0;
        const std::uint64_t checks_before = exact_distance_checks;
        const std::uint64_t candidates_before = interval_candidates;
        for (const auto& [translation, overlaps] : differences) {
            if (overlaps.size() != 2) continue;
            ++local_two;
            bool has_cross = false;
            std::array<std::uint32_t, 6> genuine_keys{};
            std::size_t genuine_count = 0;
            const RadicalInterval translation_x = radical_interval(translation.x);
            const RadicalInterval translation_y = radical_interval(translation.y);
            const Bucket centre = bucket(
                translation_x, translation_y, orientation.denominator
            );
            for (const auto& [dx, dy] : bucket_offsets) {
                if (genuine_count >= genuine_cutoff) break;
                const auto found = grid.find(Bucket{centre.x + dx, centre.y + dy});
                if (found == grid.end()) continue;
                for (const BucketNode& node : found->second) {
                    if (!interval_can_be_unit(
                            translation_x, translation_y, node.x, node.y,
                            orientation.denominator)) {
                        continue;
                    }
                    ++interval_candidates;
                    ++exact_distance_checks;
                    if (!unit_separated(translation, *node.difference, orientation.denominator)) continue;
                    has_cross = true;
                    for (std::uint32_t pair : *node.pairs) {
                        const auto key = new_strict_edge_key(
                            pair, overlaps, left_edges, small_edges
                        );
                        if (!key) continue;
                        if (std::find(
                                genuine_keys.begin(), genuine_keys.begin() + genuine_count, *key
                            ) == genuine_keys.begin() + genuine_count) {
                            genuine_keys[genuine_count++] = *key;
                            if (genuine_count >= genuine_cutoff) break;
                        }
                    }
                    if (genuine_count >= genuine_cutoff) break;
                }
            }
            local_with_cross += has_cross;
            local_with_genuine += genuine_count > 0;
            ++local_genuine_categories[genuine_count];
            if (genuine_count == 2) {
                const std::size_t left_a = genuine_keys[0] / 510;
                const std::size_t left_b = genuine_keys[1] / 510;
                const std::size_t small_a = genuine_keys[0] % 510 - 374;
                const std::size_t small_b = genuine_keys[1] % 510 - 374;
                int topology = 2;
                if (left_a == left_b) {
                    topology = 0;
                } else if (small_a == small_b) {
                    topology = 1;
                } else {
                    const int adjacency_type = 2 * left_edges[left_a][left_b]
                                             + small_edges[small_a][small_b];
                    ++local_disjoint_adjacencies[adjacency_type];
                }
                ++local_two_edge_topologies[topology];
                if (absorbed_by_colour_libraries<2>(
                        overlaps, genuine_keys, colour_libraries, compatible_two)) {
                    ++local_two_absorbed;
                    ++local_two_absorbed_by_topology[topology];
                }
            } else if (through_edges >= 3 && genuine_count == 3) {
                const std::size_t distinct_left = std::set<std::size_t>{
                    genuine_keys[0] / 510, genuine_keys[1] / 510,
                    genuine_keys[2] / 510,
                }.size();
                const std::size_t distinct_small = std::set<std::size_t>{
                    genuine_keys[0] % 510, genuine_keys[1] % 510,
                    genuine_keys[2] % 510,
                }.size();
                int topology = -1;
                if (distinct_left == 1 && distinct_small == 3) topology = 0;
                if (distinct_left == 3 && distinct_small == 1) topology = 1;
                if (distinct_left == 2 && distinct_small == 2) topology = 2;
                if (distinct_left == 2 && distinct_small == 3) topology = 3;
                if (distinct_left == 3 && distinct_small == 2) topology = 4;
                if (distinct_left == 3 && distinct_small == 3) topology = 5;
                if (topology < 0) throw std::runtime_error("bad three-edge topology");
                ++local_three_edge_topologies[topology];
                if (absorbed_by_colour_libraries<3>(
                        overlaps, genuine_keys, colour_libraries, compatible_three)) {
                    ++local_three_absorbed;
                    ++local_three_absorbed_by_topology[topology];
                }
            } else if (through_edges >= 4 && genuine_count == 4) {
                std::set<std::size_t> left_endpoints, small_endpoints;
                for (std::size_t edge = 0; edge < 4; ++edge) {
                    left_endpoints.insert(genuine_keys[edge] / 510);
                    small_endpoints.insert(genuine_keys[edge] % 510 - 374);
                }
                const std::size_t distinct_left = left_endpoints.size();
                const std::size_t distinct_small = small_endpoints.size();
                int profile = -1;
                if (distinct_left == 1 && distinct_small == 4) profile = 0;
                if (distinct_left == 4 && distinct_small == 1) profile = 1;
                if (distinct_left == 2 && distinct_small == 2) profile = 2;
                if (distinct_left == 2 && distinct_small == 3) profile = 3;
                if (distinct_left == 2 && distinct_small == 4) profile = 4;
                if (distinct_left == 3 && distinct_small == 2) profile = 5;
                if (distinct_left == 3 && distinct_small == 3) profile = 6;
                if (distinct_left == 3 && distinct_small == 4) profile = 7;
                if (distinct_left == 4 && distinct_small == 2) profile = 8;
                if (distinct_left == 4 && distinct_small == 3) profile = 9;
                if (distinct_left == 4 && distinct_small == 4) profile = 10;
                if (profile < 0) throw std::runtime_error("bad four-edge profile");
                ++local_four_edge_profiles[profile];
                if (absorbed_by_colour_libraries<4>(
                        overlaps, genuine_keys, colour_libraries, compatible_four)) {
                    ++local_four_absorbed;
                    ++local_four_absorbed_by_profile[profile];
                }
            } else if (through_edges >= 5 && genuine_count == 5) {
                if (absorbed_by_canonical_colour_libraries<5>(
                        overlaps, genuine_keys, colour_libraries, *compatible_five)) {
                    ++local_five_absorbed;
                }
            }
        }
        total_two += local_two;
        total_with_cross += local_with_cross;
        total_with_genuine += local_with_genuine;
        for (int category = 0; category < 7; ++category) {
            total_genuine_categories[category] += local_genuine_categories[category];
        }
        for (int topology = 0; topology < 3; ++topology) {
            total_two_edge_topologies[topology] += local_two_edge_topologies[topology];
        }
        for (int topology = 0; topology < 6; ++topology) {
            total_three_edge_topologies[topology] += local_three_edge_topologies[topology];
            total_three_absorbed_by_topology[topology]
                += local_three_absorbed_by_topology[topology];
        }
        total_three_absorbed += local_three_absorbed;
        for (int profile = 0; profile < 11; ++profile) {
            total_four_edge_profiles[profile] += local_four_edge_profiles[profile];
            total_four_absorbed_by_profile[profile]
                += local_four_absorbed_by_profile[profile];
        }
        total_four_absorbed += local_four_absorbed;
        total_five_absorbed += local_five_absorbed;
        for (int adjacency_type = 0; adjacency_type < 4; ++adjacency_type) {
            total_disjoint_adjacencies[adjacency_type]
                += local_disjoint_adjacencies[adjacency_type];
        }
        total_two_absorbed += local_two_absorbed;
        for (int topology = 0; topology < 3; ++topology) {
            total_two_absorbed_by_topology[topology]
                += local_two_absorbed_by_topology[topology];
        }
        std::cout << "orientation=" << orientation_index
                  << ";reflected=" << orientation.reflected
                  << ";denominator=" << orientation.denominator
                  << ";exactly_two=" << local_two
                  << ";with_cross=" << local_with_cross
                  << ";with_genuine=" << local_with_genuine
                  << ";genuine_zero=" << local_genuine_categories[0]
                  << ";genuine_one=" << local_genuine_categories[1]
                  << ";genuine_two=" << local_genuine_categories[2];
        if (through_edges >= 3) {
            std::cout << ";genuine_three=" << local_genuine_categories[3];
            if (through_edges >= 4) {
                std::cout << ";genuine_four=" << local_genuine_categories[4];
                if (through_edges >= 5) {
                    std::cout << ";genuine_five=" << local_genuine_categories[5]
                              << ";genuine_six_plus=" << local_genuine_categories[6];
                } else {
                    std::cout << ";genuine_five_plus=" << local_genuine_categories[5];
                }
            } else {
                std::cout << ";genuine_four_plus=" << local_genuine_categories[4];
            }
        } else {
            std::cout << ";genuine_three_plus=" << local_genuine_categories[3];
        }
        std::cout << ";two_share_left=" << local_two_edge_topologies[0]
                  << ";two_share_small=" << local_two_edge_topologies[1]
                  << ";two_disjoint=" << local_two_edge_topologies[2]
                  << ";disjoint_adj00=" << local_disjoint_adjacencies[0]
                  << ";disjoint_adj01=" << local_disjoint_adjacencies[1]
                  << ";disjoint_adj10=" << local_disjoint_adjacencies[2]
                  << ";disjoint_adj11=" << local_disjoint_adjacencies[3]
                  << ";two_library_absorbed=" << local_two_absorbed
                  << ";absorbed_share_left=" << local_two_absorbed_by_topology[0]
                  << ";absorbed_share_small=" << local_two_absorbed_by_topology[1]
                  << ";absorbed_disjoint=" << local_two_absorbed_by_topology[2];
        if (through_edges >= 3) {
            std::cout << ";three_L1_S3=" << local_three_edge_topologies[0]
                      << ";three_L3_S1=" << local_three_edge_topologies[1]
                      << ";three_L2_S2=" << local_three_edge_topologies[2]
                      << ";three_L2_S3=" << local_three_edge_topologies[3]
                      << ";three_L3_S2=" << local_three_edge_topologies[4]
                      << ";three_L3_S3=" << local_three_edge_topologies[5]
                      << ";three_library_absorbed=" << local_three_absorbed
                      << ";absorbed_three_L1_S3="
                      << local_three_absorbed_by_topology[0]
                      << ";absorbed_three_L3_S1="
                      << local_three_absorbed_by_topology[1]
                      << ";absorbed_three_L2_S2="
                      << local_three_absorbed_by_topology[2]
                      << ";absorbed_three_L2_S3="
                      << local_three_absorbed_by_topology[3]
                      << ";absorbed_three_L3_S2="
                      << local_three_absorbed_by_topology[4]
                      << ";absorbed_three_L3_S3="
                      << local_three_absorbed_by_topology[5];
        }
        if (through_edges >= 4) {
            std::cout << ";four_L1_S4=" << local_four_edge_profiles[0]
                      << ";four_L4_S1=" << local_four_edge_profiles[1]
                      << ";four_L2_S2=" << local_four_edge_profiles[2]
                      << ";four_L2_S3=" << local_four_edge_profiles[3]
                      << ";four_L2_S4=" << local_four_edge_profiles[4]
                      << ";four_L3_S2=" << local_four_edge_profiles[5]
                      << ";four_L3_S3=" << local_four_edge_profiles[6]
                      << ";four_L3_S4=" << local_four_edge_profiles[7]
                      << ";four_L4_S2=" << local_four_edge_profiles[8]
                      << ";four_L4_S3=" << local_four_edge_profiles[9]
                      << ";four_L4_S4=" << local_four_edge_profiles[10]
                      << ";four_library_absorbed=" << local_four_absorbed
                      << ";absorbed_four_L1_S4="
                      << local_four_absorbed_by_profile[0]
                      << ";absorbed_four_L4_S1="
                      << local_four_absorbed_by_profile[1]
                      << ";absorbed_four_L2_S2="
                      << local_four_absorbed_by_profile[2]
                      << ";absorbed_four_L2_S3="
                      << local_four_absorbed_by_profile[3]
                      << ";absorbed_four_L2_S4="
                      << local_four_absorbed_by_profile[4]
                      << ";absorbed_four_L3_S2="
                      << local_four_absorbed_by_profile[5]
                      << ";absorbed_four_L3_S3="
                      << local_four_absorbed_by_profile[6]
                      << ";absorbed_four_L3_S4="
                      << local_four_absorbed_by_profile[7]
                      << ";absorbed_four_L4_S2="
                      << local_four_absorbed_by_profile[8]
                      << ";absorbed_four_L4_S3="
                      << local_four_absorbed_by_profile[9]
                      << ";absorbed_four_L4_S4="
                      << local_four_absorbed_by_profile[10];
        }
        if (through_edges >= 5) {
            std::cout << ";five_library_absorbed=" << local_five_absorbed;
        }
        std::cout << ";interval_candidates=" << interval_candidates - candidates_before
                  << ";exact_checks=" << exact_distance_checks - checks_before << '\n';
        if ((orientation_index + 1) % 100 == 0) {
            std::cerr << "processed_orientations=" << orientation_index + 1
                      << '/' << orientations.size() << '\n';
        }
    }

    std::cout << "affine_placements_with_at_least_two_overlaps=" << total_multi_overlap << '\n';
    std::cout << "recovered_pair_certificates=" << pair_certificates << '\n';
    std::cout << "exactly_two_overlap_placements=" << total_two << '\n';
    std::cout << "with_any_cross_unit_label_pair=" << total_with_cross << '\n';
    std::cout << "with_genuinely_new_cross_edge=" << total_with_genuine << '\n';
    std::cout << "with_zero_genuinely_new_cross_edges=" << total_genuine_categories[0] << '\n';
    std::cout << "with_exactly_one_genuinely_new_cross_edge=" << total_genuine_categories[1] << '\n';
    std::cout << "with_exactly_two_genuinely_new_cross_edges=" << total_genuine_categories[2] << '\n';
    if (through_edges >= 3) {
        std::cout << "with_exactly_three_genuinely_new_cross_edges="
                  << total_genuine_categories[3] << '\n';
        if (through_edges >= 4) {
            std::cout << "with_exactly_four_genuinely_new_cross_edges="
                      << total_genuine_categories[4] << '\n';
            if (through_edges >= 5) {
                std::cout << "with_exactly_five_genuinely_new_cross_edges="
                          << total_genuine_categories[5] << '\n';
                std::cout << "with_at_least_six_genuinely_new_cross_edges="
                          << total_genuine_categories[6] << '\n';
            } else {
                std::cout << "with_at_least_five_genuinely_new_cross_edges="
                          << total_genuine_categories[5] << '\n';
            }
        } else {
            std::cout << "with_at_least_four_genuinely_new_cross_edges="
                      << total_genuine_categories[4] << '\n';
        }
    } else {
        std::cout << "with_at_least_three_genuinely_new_cross_edges="
                  << total_genuine_categories[3] << '\n';
    }
    std::cout << "two_new_edges_share_left_endpoint=" << total_two_edge_topologies[0] << '\n';
    std::cout << "two_new_edges_share_small_endpoint=" << total_two_edge_topologies[1] << '\n';
    std::cout << "two_new_edges_vertex_disjoint=" << total_two_edge_topologies[2] << '\n';
    std::cout << "disjoint_two_edges_left_nonedge_small_nonedge=" << total_disjoint_adjacencies[0] << '\n';
    std::cout << "disjoint_two_edges_left_nonedge_small_edge=" << total_disjoint_adjacencies[1] << '\n';
    std::cout << "disjoint_two_edges_left_edge_small_nonedge=" << total_disjoint_adjacencies[2] << '\n';
    std::cout << "disjoint_two_edges_left_edge_small_edge=" << total_disjoint_adjacencies[3] << '\n';
    std::cout << "two_new_edges_absorbed_by_explicit_libraries=" << total_two_absorbed << '\n';
    std::cout << "absorbed_two_edges_share_left_endpoint=" << total_two_absorbed_by_topology[0] << '\n';
    std::cout << "absorbed_two_edges_share_small_endpoint=" << total_two_absorbed_by_topology[1] << '\n';
    std::cout << "absorbed_two_edges_vertex_disjoint=" << total_two_absorbed_by_topology[2] << '\n';
    std::cout << "two_new_edges_unresolved_by_explicit_libraries="
              << total_genuine_categories[2] - total_two_absorbed << '\n';
    if (through_edges >= 3) {
        std::cout << "three_new_edges_L1_S3=" << total_three_edge_topologies[0] << '\n';
        std::cout << "three_new_edges_L3_S1=" << total_three_edge_topologies[1] << '\n';
        std::cout << "three_new_edges_L2_S2=" << total_three_edge_topologies[2] << '\n';
        std::cout << "three_new_edges_L2_S3=" << total_three_edge_topologies[3] << '\n';
        std::cout << "three_new_edges_L3_S2=" << total_three_edge_topologies[4] << '\n';
        std::cout << "three_new_edges_L3_S3=" << total_three_edge_topologies[5] << '\n';
        std::cout << "three_new_edges_absorbed_by_explicit_libraries="
                  << total_three_absorbed << '\n';
        std::cout << "absorbed_three_new_edges_L1_S3="
                  << total_three_absorbed_by_topology[0] << '\n';
        std::cout << "absorbed_three_new_edges_L3_S1="
                  << total_three_absorbed_by_topology[1] << '\n';
        std::cout << "absorbed_three_new_edges_L2_S2="
                  << total_three_absorbed_by_topology[2] << '\n';
        std::cout << "absorbed_three_new_edges_L2_S3="
                  << total_three_absorbed_by_topology[3] << '\n';
        std::cout << "absorbed_three_new_edges_L3_S2="
                  << total_three_absorbed_by_topology[4] << '\n';
        std::cout << "absorbed_three_new_edges_L3_S3="
                  << total_three_absorbed_by_topology[5] << '\n';
        std::cout << "three_new_edges_unresolved_by_explicit_libraries="
                  << total_genuine_categories[3] - total_three_absorbed << '\n';
    }
    if (through_edges >= 4) {
        std::cout << "four_new_edges_L1_S4=" << total_four_edge_profiles[0] << '\n';
        std::cout << "four_new_edges_L4_S1=" << total_four_edge_profiles[1] << '\n';
        std::cout << "four_new_edges_L2_S2=" << total_four_edge_profiles[2] << '\n';
        std::cout << "four_new_edges_L2_S3=" << total_four_edge_profiles[3] << '\n';
        std::cout << "four_new_edges_L2_S4=" << total_four_edge_profiles[4] << '\n';
        std::cout << "four_new_edges_L3_S2=" << total_four_edge_profiles[5] << '\n';
        std::cout << "four_new_edges_L3_S3=" << total_four_edge_profiles[6] << '\n';
        std::cout << "four_new_edges_L3_S4=" << total_four_edge_profiles[7] << '\n';
        std::cout << "four_new_edges_L4_S2=" << total_four_edge_profiles[8] << '\n';
        std::cout << "four_new_edges_L4_S3=" << total_four_edge_profiles[9] << '\n';
        std::cout << "four_new_edges_L4_S4=" << total_four_edge_profiles[10] << '\n';
        std::cout << "four_new_edges_absorbed_by_explicit_libraries="
                  << total_four_absorbed << '\n';
        std::cout << "absorbed_four_new_edges_L1_S4="
                  << total_four_absorbed_by_profile[0] << '\n';
        std::cout << "absorbed_four_new_edges_L4_S1="
                  << total_four_absorbed_by_profile[1] << '\n';
        std::cout << "absorbed_four_new_edges_L2_S2="
                  << total_four_absorbed_by_profile[2] << '\n';
        std::cout << "absorbed_four_new_edges_L2_S3="
                  << total_four_absorbed_by_profile[3] << '\n';
        std::cout << "absorbed_four_new_edges_L2_S4="
                  << total_four_absorbed_by_profile[4] << '\n';
        std::cout << "absorbed_four_new_edges_L3_S2="
                  << total_four_absorbed_by_profile[5] << '\n';
        std::cout << "absorbed_four_new_edges_L3_S3="
                  << total_four_absorbed_by_profile[6] << '\n';
        std::cout << "absorbed_four_new_edges_L3_S4="
                  << total_four_absorbed_by_profile[7] << '\n';
        std::cout << "absorbed_four_new_edges_L4_S2="
                  << total_four_absorbed_by_profile[8] << '\n';
        std::cout << "absorbed_four_new_edges_L4_S3="
                  << total_four_absorbed_by_profile[9] << '\n';
        std::cout << "absorbed_four_new_edges_L4_S4="
                  << total_four_absorbed_by_profile[10] << '\n';
        std::cout << "four_new_edges_unresolved_by_explicit_libraries="
                  << total_genuine_categories[4] - total_four_absorbed << '\n';
    }
    if (through_edges >= 5) {
        std::cout << "five_new_edges_absorbed_by_explicit_libraries="
                  << total_five_absorbed << '\n';
        std::cout << "five_new_edges_unresolved_by_explicit_libraries="
                  << total_genuine_categories[5] - total_five_absorbed << '\n';
    }
    std::cout << "closed_by_single_cross_edge_absorption="
              << total_genuine_categories[0] + total_genuine_categories[1] << '\n';
    std::cout << "interval_candidates=" << interval_candidates << '\n';
    std::cout << "exact_distance_checks=" << exact_distance_checks << '\n';
    const std::uint64_t categorized = std::accumulate(
        total_genuine_categories.begin(),
        total_genuine_categories.begin() + genuine_cutoff + 1,
        std::uint64_t{0}
    );
    if (total_multi_overlap != 2992078 || pair_certificates != 17658256
        || total_two != 2373802 || total_with_genuine > total_with_cross
        || categorized != total_two
        || categorized - total_genuine_categories[0] != total_with_genuine
        || total_two_edge_topologies[0] + total_two_edge_topologies[1]
             + total_two_edge_topologies[2] != total_genuine_categories[2]
        || total_disjoint_adjacencies[0] + total_disjoint_adjacencies[1]
             + total_disjoint_adjacencies[2] + total_disjoint_adjacencies[3]
             != total_two_edge_topologies[2]
        || total_two_absorbed_by_topology[0] + total_two_absorbed_by_topology[1]
             + total_two_absorbed_by_topology[2] != total_two_absorbed
        || total_two_absorbed > total_genuine_categories[2]
        || (through_edges >= 3
            && (std::accumulate(
                    total_three_edge_topologies.begin(),
                    total_three_edge_topologies.end(), std::uint64_t{0})
                    != total_genuine_categories[3]
                || std::accumulate(
                       total_three_absorbed_by_topology.begin(),
                       total_three_absorbed_by_topology.end(), std::uint64_t{0})
                    != total_three_absorbed
                || total_three_absorbed > total_genuine_categories[3]))
        || (through_edges >= 4
            && (std::accumulate(
                    total_four_edge_profiles.begin(),
                    total_four_edge_profiles.end(), std::uint64_t{0})
                    != total_genuine_categories[4]
                || std::accumulate(
                       total_four_absorbed_by_profile.begin(),
                       total_four_absorbed_by_profile.end(), std::uint64_t{0})
                    != total_four_absorbed
                || total_four_absorbed > total_genuine_categories[4]))
        || (through_edges >= 5
            && total_five_absorbed > total_genuine_categories[5])) {
        throw std::runtime_error("census checksum mismatch");
    }
    std::cout << "exact_two_overlap_cross_census=true\n";
}
