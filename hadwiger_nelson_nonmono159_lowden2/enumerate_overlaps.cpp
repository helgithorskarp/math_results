#define main parts_affine_overlap_original_main
#include "../hadwiger_nelson_parts509_affine_overlap_scan/enumerate_overlaps.cpp"
#undef main

static std::vector<Point> read_points_any(const std::string& path) {
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
    return points;
}

int main(int argc, char** argv) {
    if (argc < 3 || argc > 7 || argc % 2 == 0) {
        std::cerr << "usage: nonmono_overlap_scan LEFT.tsv RIGHT.tsv "
                     "[--emit-at-least N] [--max-denominator D]\n";
        return 2;
    }
    unsigned emit_threshold = 1000;
    i64 max_denominator = std::numeric_limits<i64>::max();
    for (int argument = 3; argument < argc; argument += 2) {
        const std::string option = argv[argument];
        if (option == "--emit-at-least") {
            emit_threshold = std::stoul(argv[argument + 1]);
            if (emit_threshold < 2) throw std::runtime_error("bad emission threshold");
        } else if (option == "--max-denominator") {
            max_denominator = std::stoll(argv[argument + 1]);
            if (max_denominator < 1) throw std::runtime_error("bad maximum denominator");
        } else {
            throw std::runtime_error("unknown option");
        }
    }
    const auto left = read_points_any(argv[1]);
    const auto right = read_points_any(argv[2]);
    const auto left_vectors = directed_vectors(left);
    const auto right_vectors = directed_vectors(right);
    const auto orientation_set = enumerate_orientations(left_vectors, right_vectors);
    const std::vector<Orientation> orientations(orientation_set.begin(), orientation_set.end());
    std::size_t rotations = 0;
    for (const auto& o : orientations) rotations += !o.reflected;
    std::cout << "left_vertices=" << left.size() << '\n';
    std::cout << "right_vertices=" << right.size() << '\n';
    std::cout << "rotations=" << rotations << '\n';
    std::cout << "reflections=" << orientations.size() - rotations << '\n';
    std::size_t lv = 0, rv = 0;
    for (const auto& [d,v] : left_vectors) { (void)d; lv += v.size(); }
    for (const auto& [d,v] : right_vectors) { (void)d; rv += v.size(); }
    std::cout << "distinct_left_vectors=" << lv << '\n';
    std::cout << "distinct_right_vectors=" << rv << '\n';
    std::map<unsigned, std::uint64_t> histogram;
    std::uint64_t placements = 0, certificates = 0;
    std::size_t oi = 0, selected_orientations = 0;
    for (const Orientation& orientation : orientations) {
        if (orientation.denominator > max_denominator) {
            ++oi;
            continue;
        }
        ++selected_orientations;
        std::vector<Point> image;
        for (const Point& p : right) image.push_back(transformed_numerator(orientation, p));
        std::unordered_map<Difference, std::uint16_t, DifferenceHash> multiplicities;
        multiplicities.reserve(left.size() * right.size() * 2);
        for (const Point& p : left) for (const Point& q : image)
            ++multiplicities[cross_difference(p, q, orientation.denominator)];
        for (const auto& [difference, m] : multiplicities) if (m >= 2) {
            ++placements;
            ++histogram[m];
            certificates += static_cast<std::uint64_t>(m) * (m - 1) / 2;
            if (m >= emit_threshold) {
                std::cout << "placement=" << m << ";reflected=" << orientation.reflected
                          << ";denominator=" << orientation.denominator << ";c=";
                print_field(orientation.c); std::cout << ";s="; print_field(orientation.s);
                std::cout << ";tx="; print_field(difference.x);
                std::cout << ";ty="; print_field(difference.y); std::cout << '\n';
            }
        }
        if (++oi % 100 == 0) std::cerr << "processed=" << oi << '/' << orientations.size() << '\n';
    }
    std::cout << "placements_with_at_least_two_overlaps=" << placements << '\n';
    std::cout << "selected_orientations=" << selected_orientations << '\n';
    std::cout << "pair_certificates=" << certificates << '\n';
    for (const auto& [m,n] : histogram) std::cout << "overlap_" << m << '=' << n << '\n';
    std::cout << "exact_scan=true\n";
}
