#include <algorithm>
#include <array>
#include <compare>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <map>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

using i64 = std::int64_t;
using i128 = __int128_t;
using Field = std::array<i64, 8>;

struct Point {
    Field x{}, y{};
    auto operator<=>(const Point&) const = default;
};

struct Transform {
    unsigned overlaps{};
    bool reflected{};
    i64 denominator{};
    Field c{}, s{}, tx{}, ty{};
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

static Field squared_distance(const Point& a, const Point& b) {
    const Field dx = subtract(a.x, b.x), dy = subtract(a.y, b.y);
    return add(multiply(dx, dx), multiply(dy, dy));
}

static Field scale(const Field& a, i64 factor) {
    Field out{};
    for (int i = 0; i < 8; ++i) out[i] = narrow(static_cast<i128>(a[i]) * factor);
    return out;
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

static std::vector<std::string> split(const std::string& text, char separator) {
    std::vector<std::string> result;
    std::istringstream input(text);
    std::string item;
    while (std::getline(input, item, separator)) result.push_back(item);
    return result;
}

static Field parse_field(const std::string& text) {
    const std::vector<std::string> values = split(text, ',');
    if (values.size() != 8) throw std::runtime_error("bad field encoding");
    Field result{};
    for (int i = 0; i < 8; ++i) result[i] = std::stoll(values[i]);
    return result;
}

static std::vector<Transform> read_transforms(const std::string& path) {
    std::ifstream input(path);
    if (!input) throw std::runtime_error("cannot open scan file");
    std::vector<Transform> result;
    std::string line;
    while (std::getline(input, line)) {
        if (!line.starts_with("high_overlap=")) continue;
        std::map<std::string, std::string> row;
        for (const std::string& item : split(line, ';')) {
            const std::size_t equals = item.find('=');
            if (equals == std::string::npos) throw std::runtime_error("bad transform item");
            row[item.substr(0, equals)] = item.substr(equals + 1);
        }
        result.push_back(Transform{
            static_cast<unsigned>(std::stoul(row.at("high_overlap"))),
            static_cast<bool>(std::stoi(row.at("reflected"))),
            std::stoll(row.at("denominator")),
            parse_field(row.at("c")),
            parse_field(row.at("s")),
            parse_field(row.at("tx")),
            parse_field(row.at("ty")),
        });
    }
    std::sort(result.begin(), result.end(), [](const Transform& a, const Transform& b) {
        return std::tie(a.reflected, a.denominator, a.c, a.s, a.tx, a.ty)
             < std::tie(b.reflected, b.denominator, b.c, b.s, b.tx, b.ty);
    });
    return result;
}

static Point transform(const Point& point, const Transform& transformation) {
    const Field cx = multiply(transformation.c, point.x);
    const Field sy = multiply(transformation.s, point.y);
    const Field sx = multiply(transformation.s, point.x);
    const Field cy = multiply(transformation.c, point.y);
    Point result;
    if (transformation.reflected) {
        result = Point{add(cx, sy), subtract(sx, cy)};
    } else {
        result = Point{subtract(cx, sy), add(sx, cy)};
    }
    result.x = add(result.x, transformation.tx);
    result.y = add(result.y, transformation.ty);
    return result;
}

static std::vector<std::pair<std::uint16_t, std::uint16_t>> internal_edges(
    const std::vector<Point>& points
) {
    Field unit{};
    unit[0] = 96 * 96;
    std::vector<std::pair<std::uint16_t, std::uint16_t>> result;
    for (std::uint16_t u = 0; u < points.size(); ++u) {
        for (std::uint16_t v = u + 1; v < points.size(); ++v) {
            if (squared_distance(points[u], points[v]) == unit) result.emplace_back(u, v);
        }
    }
    return result;
}

int main(int argc, char** argv) {
    if (argc != 3) {
        std::cerr << "usage: emit_graphs POINTS.tsv OVERLAP_SCAN.txt\n";
        return 2;
    }
    const std::vector<Point> source = read_points(argv[1]);
    const std::vector<Point> left(source.begin(), source.begin() + 374);
    std::vector<Point> small;
    small.push_back(source[0]);
    small.insert(small.end(), source.begin() + 374, source.end());
    const auto left_edges = internal_edges(left);
    const auto small_edges = internal_edges(small);
    if (left_edges.size() != 1860 || small_edges.size() != 564) {
        throw std::runtime_error("internal strict-edge census mismatch");
    }

    const std::vector<Transform> transformations = read_transforms(argv[2]);
    std::cout << "graphs=" << transformations.size() << '\n';
    for (std::size_t index = 0; index < transformations.size(); ++index) {
        const Transform& transformation = transformations[index];
        std::vector<Point> labelled;
        labelled.reserve(510);
        for (const Point& point : left) {
            labelled.push_back(Point{scale(point.x, transformation.denominator),
                                     scale(point.y, transformation.denominator)});
        }
        for (const Point& point : small) labelled.push_back(transform(point, transformation));

        std::map<Point, std::uint16_t> point_index;
        std::vector<std::uint16_t> label_index;
        label_index.reserve(labelled.size());
        for (const Point& point : labelled) {
            const auto [found, inserted] = point_index.emplace(point, point_index.size());
            (void)inserted;
            label_index.push_back(found->second);
        }
        const std::size_t order = point_index.size();
        if (order != 510 - transformation.overlaps) {
            throw std::runtime_error("reported overlap count mismatch");
        }

        std::set<std::pair<std::uint16_t, std::uint16_t>> edges;
        const auto add_edge = [&](std::uint16_t a, std::uint16_t b) {
            a = label_index[a];
            b = label_index[b];
            if (a != b) edges.emplace(std::min(a, b), std::max(a, b));
        };
        for (const auto& [u, v] : left_edges) add_edge(u, v);
        for (const auto& [u, v] : small_edges) add_edge(374 + u, 374 + v);

        Field unit{};
        unit[0] = narrow(static_cast<i128>(96) * 96 * transformation.denominator * transformation.denominator);
        for (std::uint16_t p = 0; p < 374; ++p) {
            for (std::uint16_t q = 0; q < 136; ++q) {
                if (squared_distance(labelled[p], labelled[374 + q]) == unit) add_edge(p, 374 + q);
            }
        }

        std::cout << "graph=" << index << ";overlaps=" << transformation.overlaps
                  << ";order=" << order << ";edges=" << edges.size() << ";edge_list=";
        bool first = true;
        for (const auto& [u, v] : edges) {
            if (!first) std::cout << ',';
            first = false;
            std::cout << u << '-' << v;
        }
        std::cout << '\n';
        if ((index + 1) % 100 == 0) {
            std::cerr << "emitted_graphs=" << index + 1 << '/' << transformations.size() << '\n';
        }
    }
    std::cout << "exact_graph_emission=true\n";
}
