#define main parts_affine_overlap_original_main
#include "../hadwiger_nelson_parts509_affine_overlap_scan/enumerate_overlaps.cpp"
#undef main

struct Transform {
    unsigned overlaps{};
    bool reflected{};
    i64 denominator{};
    Field c{}, s{}, tx{}, ty{};
};

static std::vector<std::string> split_any(const std::string& text, char separator) {
    std::vector<std::string> result;
    std::istringstream input(text);
    std::string item;
    while (std::getline(input, item, separator)) result.push_back(item);
    return result;
}

static Field parse_field_any(const std::string& text) {
    const auto values = split_any(text, ',');
    if (values.size() != 8) throw std::runtime_error("bad field encoding");
    Field result{};
    for (int i = 0; i < 8; ++i) result[i] = std::stoll(values[i]);
    return result;
}

static std::vector<Transform> read_transforms_any(const std::string& path) {
    std::ifstream input(path);
    if (!input) throw std::runtime_error("cannot open transforms file");
    std::vector<Transform> result;
    std::string line;
    while (std::getline(input, line)) {
        if (!line.starts_with("placement=")) continue;
        std::map<std::string, std::string> row;
        for (const std::string& item : split_any(line, ';')) {
            const auto equals = item.find('=');
            if (equals == std::string::npos) throw std::runtime_error("bad transform row");
            row[item.substr(0, equals)] = item.substr(equals + 1);
        }
        result.push_back(Transform{
            static_cast<unsigned>(std::stoul(row.at("placement"))),
            static_cast<bool>(std::stoi(row.at("reflected"))),
            std::stoll(row.at("denominator")),
            parse_field_any(row.at("c")), parse_field_any(row.at("s")),
            parse_field_any(row.at("tx")), parse_field_any(row.at("ty"))
        });
    }
    std::sort(result.begin(), result.end(), [](const Transform& a, const Transform& b) {
        return std::tie(a.reflected, a.denominator, a.c, a.s, a.tx, a.ty)
             < std::tie(b.reflected, b.denominator, b.c, b.s, b.tx, b.ty);
    });
    return result;
}

static std::vector<Point> read_points_any(const std::string& path, i64& scale_out) {
    std::ifstream input(path);
    if (!input) throw std::runtime_error("cannot open points file");
    std::vector<Point> points;
    std::string line;
    scale_out = 0;
    while (std::getline(input, line)) {
        if (line.starts_with("# scale ")) {
            scale_out = std::stoll(line.substr(8));
            continue;
        }
        if (line.empty() || line[0] == '#') continue;
        std::istringstream row(line);
        Point point;
        for (i64& value : point.x) row >> value;
        for (i64& value : point.y) row >> value;
        std::string extra;
        if (!row || row >> extra) throw std::runtime_error("bad points row");
        points.push_back(point);
    }
    if (scale_out <= 0) throw std::runtime_error("missing positive scale header");
    return points;
}

static Field scale_field(const Field& a, i64 factor) {
    Field result{};
    for (int i = 0; i < 8; ++i) result[i] = narrow(static_cast<i128>(a[i]) * factor);
    return result;
}

static Point transform_any(const Point& p, const Transform& t) {
    const Field cx = multiply(t.c, p.x), sy = multiply(t.s, p.y);
    const Field sx = multiply(t.s, p.x), cy = multiply(t.c, p.y);
    Point result = t.reflected ? Point{add(cx, sy), subtract(sx, cy)}
                               : Point{subtract(cx, sy), add(sx, cy)};
    result.x = add(result.x, t.tx);
    result.y = add(result.y, t.ty);
    return result;
}

static bool is_unit_any(const Point& a, const Point& b, i64 scale) {
    Vector difference{subtract(a.x, b.x), subtract(a.y, b.y)};
    Field target{};
    target[0] = narrow(static_cast<i128>(scale) * scale);
    return squared_norm(difference) == target;
}

#ifndef NONMONO_EMIT_LIBRARY
int main(int argc, char** argv) {
    if (argc != 4) {
        std::cerr << "usage: emit_graphs LEFT.tsv RIGHT.tsv TRANSFORMS.txt\n";
        return 2;
    }
    i64 left_scale = 0, right_scale = 0;
    const auto left = read_points_any(argv[1], left_scale);
    const auto right = read_points_any(argv[2], right_scale);
    if (left_scale != right_scale) throw std::runtime_error("point scales differ");
    const auto transforms = read_transforms_any(argv[3]);
    std::cout << "graphs=" << transforms.size() << '\n';
    for (std::size_t index = 0; index < transforms.size(); ++index) {
        const Transform& t = transforms[index];
        std::vector<Point> labelled;
        labelled.reserve(left.size() + right.size());
        for (const Point& p : left) labelled.push_back(
            Point{scale_field(p.x, t.denominator), scale_field(p.y, t.denominator)});
        for (const Point& p : right) labelled.push_back(transform_any(p, t));

        std::map<Point, std::uint16_t> point_index;
        std::vector<std::uint16_t> labels;
        for (const Point& p : labelled) {
            const auto [found, inserted] = point_index.emplace(p, point_index.size());
            (void)inserted;
            labels.push_back(found->second);
        }
        if (point_index.size() != left.size() + right.size() - t.overlaps) {
            throw std::runtime_error("reported overlap count mismatch");
        }
        std::vector<Point> points(point_index.size());
        for (const auto& [p, i] : point_index) points[i] = p;
        std::vector<std::pair<std::uint16_t, std::uint16_t>> edges;
        const i64 transformed_scale = narrow(static_cast<i128>(left_scale) * t.denominator);
        for (std::uint16_t u = 0; u < points.size(); ++u) {
            for (std::uint16_t v = u + 1; v < points.size(); ++v) {
                if (is_unit_any(points[u], points[v], transformed_scale)) edges.emplace_back(u, v);
            }
        }
        std::cout << "graph=" << index << ";overlaps=" << t.overlaps
                  << ";order=" << points.size() << ";edges=" << edges.size()
                  << ";edge_list=";
        for (std::size_t e = 0; e < edges.size(); ++e) {
            if (e) std::cout << ',';
            std::cout << edges[e].first << '-' << edges[e].second;
        }
        std::cout << '\n';
    }
    std::cout << "exact_graph_emission=true\n";
}
#endif
