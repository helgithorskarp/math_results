#include "engine.hpp"
int main(int argc, char **argv) {
  try {
    auto start = std::chrono::steady_clock::now();
    if (argc < 2)
      throw std::runtime_error("mode");
    std::string mode = argv[1];
    if (mode == "complete") {
      if (argc != 9 && argc != 10)
        throw std::runtime_error("complete method weights profiles domains "
                                 "trace decisions done [ten_catalog]");
      int method = integer(argv[2]);
      if (method < 0 || method > 1)
        throw std::runtime_error("method");
      Weights w(argv[3]);
      auto profiles = readprofiles(argv[4]);
      std::ifstream in(argv[5]);
      std::ofstream trace(argv[6], std::ios::binary), out(argv[7]);
      if (!in || !trace || !out)
        throw std::runtime_error("IO");
      std::unique_ptr<Catalog> catalog;
      if (argc == 10)
        catalog = std::make_unique<Catalog>(argv[9], w, 10, 0, method);
      Solver s{w, catalog.get(), method, &trace, nullptr, 0, 0, 0, 0, 0, {},
               {}};
      std::string line;
      uint64_t domains = 0;
      while (std::getline(in, line)) {
        U d = readset(line);
        auto a = s.run(d, profiles);
        out << "{\"found\":" << (!a.empty() ? "true" : "false")
            << ",\"partition\":[";
        for (size_t i = 0; i < a.size(); ++i) {
          if (i)
            out << ',';
          printset(a[i], out);
        }
        out << "]}\n";
        ++domains;
      }
      out.flush();
      trace.flush();
      if (!in.eof() || !out || !trace)
        throw std::runtime_error("completion IO");
      std::ofstream done(argv[8]);
      done << "complete\n";
      done.close();
      if (!done)
        throw std::runtime_error("done");
      std::cout << "{\"complete\":true,\"domains\":" << domains
                << ",\"found\":" << s.found << ",\"calls\":" << s.calls
                << ",\"queries\":" << s.queries << ",\"options\":" << s.options
                << ",\"leaves\":" << s.leaves << "}\n";
      return 0;
    }
    if (mode == "count") {
      if (argc != 7)
        throw std::runtime_error("count method anchors orbit weights cases");
      int method = integer(argv[2]);
      if (method < 0 || method > 1)
        throw std::runtime_error("method");
      Weights w(argv[5]);
      std::ofstream out(argv[6]);
      if (!out)
        throw std::runtime_error("output");
      Packing p(argv[4], w, nullptr, method, integer(argv[3]), 0, 1, out);
      p.run();
      std::cout << "{\"complete\":true,\"packings\":" << p.packings << "}\n";
      return 0;
    }
    if (mode != "sweep" || (argc != 13 && argc != 14))
      throw std::runtime_error("sweep method anchors orbit weights full_ten "
                               "shard parts cases trace terminals done");
    int method = integer(argv[2]);
    Weights w(argv[5]);
    Catalog c(argv[6], w, 10, 0, method);
    if (c.masks.size() != 17249580 ||
        *std::max_element(c.weights.begin(), c.weights.end()) > cap)
      throw std::runtime_error("full ten catalog");
    std::ofstream out(argv[9]), trace(argv[10], std::ios::binary),
        terminal(argv[11]);
    if (!out || !trace || !terminal)
      throw std::runtime_error("outputs");
    Solver s{w, &c, method, &trace, &terminal, 0, 0, 0, 0, 0, {}, {}};
    Packing p(argv[4], w, &s, method, integer(argv[3]), integer(argv[7]),
              integer(argv[8]), out);
    p.minimum = argc == 14 ? integer(argv[13]) : 0;
    if (p.minimum < 0 || p.minimum > 4107)
      throw std::runtime_error("minimum orbit");
    p.run();
    out.flush();
    trace.flush();
    terminal.flush();
    if (!out || !trace || !terminal)
      throw std::runtime_error("output completion");
    std::ofstream done(argv[12]);
    done << "complete\n";
    done.close();
    if (!done)
      throw std::runtime_error("done");
    std::cout << "{\"complete\":true,\"packings\":" << p.packings
              << ",\"found\":" << p.found << ",\"seconds\":"
              << std::chrono::duration<double>(
                     std::chrono::steady_clock::now() - start)
                     .count()
              << "}\n";
  } catch (const std::exception &e) {
    std::cerr << e.what() << '\n';
    return 1;
  }
}
