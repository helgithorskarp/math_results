#include "engine.hpp"
int main(int argc, char **argv) {
  try {
    if (argc != 6)
      throw std::runtime_error("method weights catalog parent domains");
    int method = integer(argv[1]);
    Weights w(argv[2]);
    Catalog catalog(argv[3], w, 10, 0, method);
    std::ifstream parent_in(argv[4]), domain_in(argv[5]);
    std::string line;
    std::getline(parent_in, line);
    U parent = readset(line);
    if (pop(parent) != 60)
      throw std::runtime_error("parent size");
    std::ostringstream plain_trace, cached_trace;
    Solver plain{w, &catalog, method, &plain_trace, nullptr, 0, 0,
                 0, 0,        0,      {},           {}};
    Solver cached{w, &catalog, method, &cached_trace, nullptr, 0, 0, 0, 0,
                  0, {},       {}};
    cached.set_parent(parent, cap);
    Profile profile{10, 10, 10, 10, 9};
    uint64_t domains = 0;
    while (std::getline(domain_in, line)) {
      U domain = readset(line);
      if (pop(domain) != 49 || (domain & ~parent) || w(parent ^ domain) > cap)
        throw std::runtime_error("control domain");
      auto reference = plain.run(domain, {profile});
      // The query counter changes only when the exact cache is constructed.
      // Force that performance branch to exercise reuse even on easy positives.
      cached.local.reset();
      cached.root_domain = domain;
      cached.root_lower = std::max(0, w(domain) - 3 * cap - cached.classcap(9));
      cached.root_queries = 32;
      cached.cache_enabled = true;
      auto answer = cached.visit(domain, profile, 0, cap);
      if (answer.empty() || answer != reference)
        throw std::runtime_error("positive completion");
      U used = 0;
      std::vector<int> sizes;
      for (U row : answer) {
        if (!sidon(row, 0) || (used & row))
          throw std::runtime_error("partition");
        used |= row;
        sizes.push_back(pop(row));
      }
      std::sort(sizes.begin(), sizes.end());
      if (used != domain || sizes != std::vector<int>{9, 10, 10, 10, 10})
        throw std::runtime_error("partition sizes");
      ++domains;
    }
    if (!domain_in.eof() || domains != 10 || !cached.parent_ready ||
        cached.parent_preparations != 10 ||
        plain_trace.str() != cached_trace.str())
      throw std::runtime_error("cache reuse/trace");
    std::cout << "{\"verified\":true,\"method\":" << method
              << ",\"positive_domains\":" << domains
              << ",\"parent_preparations\":" << cached.parent_preparations
              << ",\"parent_rows\":" << cached.parent_rows.size()
              << ",\"exact_compared_trace_bytes\":" << plain_trace.str().size()
              << "}\n";
    return 0;
  } catch (const std::exception &e) {
    std::cerr << e.what() << '\n';
    return 1;
  }
}
