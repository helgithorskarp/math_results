// Independently audit the mathematical content of wustep/maths q4's f=8 CNF.
// No external generator source is compiled or called by this checker.
#include <algorithm>
#include <array>
#include <fstream>
#include <functional>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {
constexpr int n = 43, fixed = 8, cycles = 7, edge_vars = 203;
using Clause = std::vector<int>;
using Formula = std::vector<Clause>;
using Matrix = std::array<std::array<int, n>, n>;

void check(bool value, const std::string &message) {
  if (!value) throw std::runtime_error(message);
}
int vertex(int cycle, int position = 0) { return fixed + 5 * cycle + position; }

struct DSU {
  std::vector<int> parent;
  explicit DSU(int size) : parent(static_cast<std::size_t>(size)) {
    std::iota(parent.begin(), parent.end(), 0);
  }
  int root(int v) {
    int &p = parent.at(static_cast<std::size_t>(v));
    if (p != v) p = root(p);
    return p;
  }
  void join(int u, int v) { parent.at(static_cast<std::size_t>(root(u))) = root(v); }
};

Matrix read_edge_labels(const std::string &path) {
  Matrix pair_id{};
  std::vector<std::pair<int, int>> pairs;
  for (int u = 0; u < n; ++u) for (int v = u+1; v < n; ++v) {
    pair_id[u][v] = pair_id[v][u] = static_cast<int>(pairs.size());
    pairs.emplace_back(u, v);
  }
  auto next = [](int v) {
    return v < fixed ? v : fixed + 5*((v-fixed)/5) + ((v-fixed+1)%5);
  };
  DSU dsu(static_cast<int>(pairs.size()));
  for (std::size_t i=0; i<pairs.size(); ++i) {
    auto [u,v] = pairs[i];
    dsu.join(static_cast<int>(i), pair_id[next(u)][next(v)]);
  }
  std::ifstream in(path);
  check(bool(in), "cannot open label file");
  std::set<int> ids;
  std::map<int,int> orbit_label;
  std::string line;
  while (std::getline(in,line)) {
    std::istringstream row(line);
    int id, a, b, d=0, u=-1, v=-1;
    std::string tag, extra;
    check(bool(row >> id >> tag >> a >> b), "malformed edge label");
    check(id>=1 && id<=edge_vars && ids.insert(id).second, "bad/duplicate variable id");
    if (tag=="ff") {
      check(0<=a && a<b && b<fixed, "bad fixed pair"); u=a; v=b;
    } else if (tag=="fc") {
      check(0<=a && a<fixed && 0<=b && b<cycles, "bad fixed-cycle label");
      u=a; v=vertex(b);
    } else if (tag=="cc") {
      check(0<=a && a<cycles && 1<=b && b<=2, "bad internal distance");
      u=vertex(a); v=vertex(a,b);
    } else if (tag=="cb") {
      check(bool(row>>d) && 0<=a && a<b && b<cycles && 0<=d && d<5,
            "bad between-cycle label");
      u=vertex(a); v=vertex(b,d);
    } else throw std::runtime_error("unknown label type");
    check(!(row>>extra), "extra label tokens");
    check(orbit_label.emplace(dsu.root(pair_id[u][v]),id).second,
          "two labels name the same actual edge orbit");
  }
  check(ids.size()==edge_vars, "incomplete edge labels");
  Matrix result{};
  std::map<int,int> sizes;
  for (std::size_t i=0; i<pairs.size(); ++i) {
    auto [u,v]=pairs[i];
    const int id=orbit_label.at(dsu.root(static_cast<int>(i)));
    result[u][v]=result[v][u]=id;
    ++sizes[id];
  }
  int singletons=0, fives=0;
  for (const auto &[id,size]:sizes) {
    (void)id;
    singletons += size==1; fives += size==5;
  }
  check(singletons==28 && fives==175, "wrong orbit-size distribution");
  return result;
}

void add(Formula &formula, Clause c) {
  std::sort(c.begin(),c.end());
  c.erase(std::unique(c.begin(),c.end()),c.end());
  for (int x:c) if (std::binary_search(c.begin(),c.end(),-x)) return;
  formula.push_back(std::move(c));
}

// Obtain minimal CNF clauses from the gate's truth table, rather than copy
// the source generator's clause templates. A cube is a partial assignment;
// it gives a prime implicate iff it minimally excludes all satisfying rows.
Formula prime_cnf(int arity, const std::function<bool(unsigned)> &truth) {
  std::vector<unsigned> satisfying;
  for (unsigned a=0; a<(1U<<arity); ++a) if (truth(a)) satisfying.push_back(a);
  auto allows = [&satisfying](const std::vector<int> &cube) {
    for (unsigned a:satisfying) {
      bool fits=true;
      for (std::size_t i=0;i<cube.size();++i) {
        if (cube[i]>=0 && int((a>>i)&1U)!=cube[i]) fits=false;
      }
      if (fits) return true;
    }
    return false;
  };
  int total=1;
  for (int i=0;i<arity;++i) total*=3;
  Formula out;
  for (int code=0;code<total;++code) {
    std::vector<int> cube(static_cast<std::size_t>(arity));
    int rest=code;
    for (int i=0;i<arity;++i) { cube[i]=rest%3-1; rest/=3; }
    if (allows(cube)) continue;
    bool minimal=true;
    for (int i=0;i<arity;++i) if (cube[i]>=0) {
      auto smaller=cube; smaller[i]=-1;
      if (!allows(smaller)) minimal=false;
    }
    if (!minimal) continue;
    Clause clause;
    for (int i=0;i<arity;++i) if (cube[i]>=0) {
      clause.push_back(cube[i] ? -(i+1) : i+1);
    }
    out.push_back(std::move(clause));
  }
  return out;
}
bool bit(unsigned a,int i) { return ((a>>i)&1U)!=0; }

const std::array<Formula,4> gates{
  prime_cnf(2,[](unsigned a){return bit(a,1)==bit(a,0);}),
  prime_cnf(3,[](unsigned a){return bit(a,2)==(bit(a,0)||bit(a,1));}),
  prime_cnf(4,[](unsigned a){return bit(a,3)==(bit(a,0)||(bit(a,1)&&bit(a,2)));}),
  prime_cnf(4,[](unsigned a){return bit(a,3)==(bit(a,0)&&(bit(a,1)==bit(a,2)));})
};
void gate(Formula &f,int kind,const std::vector<int> &v) {
  for (const auto &pattern:gates.at(static_cast<std::size_t>(kind))) {
    Clause c;
    for(int x:pattern) c.push_back((x>0?1:-1)*v.at(static_cast<std::size_t>(std::abs(x)-1)));
    add(f,std::move(c));
  }
}

void degree_counter(Formula &f,const std::vector<int> &inputs,int &top) {
  check(inputs.size()==42,"degree row must have all 42 incidences");
  std::array<std::array<int,24>,42> at_least{};
  for(auto &row:at_least) for(int &v:row) v=++top;
  gate(f,0,{inputs[0],at_least[0][0]});
  for(int j=1;j<24;++j) add(f,{-at_least[0][j]});
  for(int i=1;i<42;++i) {
    gate(f,1,{at_least[i-1][0],inputs[i],at_least[i][0]});
    for(int j=1;j<24;++j) {
      gate(f,2,{at_least[i-1][j],inputs[i],at_least[i-1][j-1],at_least[i][j]});
    }
    add(f,{-inputs[i],-at_least[i-1][23]});
  }
  add(f,{at_least[41][17]});
}

void lex(Formula &f,const std::vector<int> &a,const std::vector<int> &b,int &top) {
  check(a.size()==b.size(),"lex widths differ");
  int prefix=++top;
  add(f,{prefix});
  for(std::size_t i=0;i<a.size();++i) {
    add(f,{-prefix,-a[i],b[i]});
    const int next=++top;
    gate(f,3,{prefix,a[i],b[i],next});
    prefix=next;
  }
}

Formula expected(const Matrix &v,int &top) {
  std::set<Clause> keys;
  for(int a=0;a<n-4;++a) for(int b=a+1;b<n-3;++b)
  for(int c=b+1;c<n-2;++c) for(int d=c+1;d<n-1;++d) for(int e=d+1;e<n;++e) {
    const std::array<int,5> s{a,b,c,d,e};
    Clause key;
    for(int i=0;i<5;++i) for(int j=i+1;j<5;++j) key.push_back(v[s[i]][s[j]]);
    std::sort(key.begin(),key.end());
    key.erase(std::unique(key.begin(),key.end()),key.end());
    keys.insert(std::move(key));
  }
  Formula f;
  for(const auto &key:keys) {
    add(f,key); Clause neg;
    for(int x:key) neg.push_back(-x);
    add(f,std::move(neg));
  }
  const auto base=f.size();
  for(int orbit=0;orbit<fixed+cycles;++orbit) {
    const int u=orbit<fixed?orbit:vertex(orbit-fixed);
    std::vector<int> inputs;
    for(int w=0;w<n;++w) if(w!=u) inputs.push_back(v[u][w]);
    degree_counter(f,inputs,top);
  }
  const auto degree=f.size()-base;
  for(int c=0;c<cycles;++c) add(f,{c<3?v[0][vertex(c)]:-v[0][vertex(c)]});
  for(int a=0;a+1<cycles;++a) if(a!=2) {
    lex(f,{v[vertex(a)][vertex(a,1)],v[vertex(a)][vertex(a,2)]},
          {v[vertex(a+1)][vertex(a+1,1)],v[vertex(a+1)][vertex(a+1,2)]},top);
  }
  for(int c=1;c<cycles;++c) for(int shift=1;shift<5;++shift) {
    std::vector<int> a,b;
    for(int r=0;r<5;++r) {
      a.push_back(v[vertex(0)][vertex(c,r)]);
      b.push_back(v[vertex(0)][vertex(c,(r+shift)%5)]);
    }
    lex(f,a,b,top);
  }
  std::cout << "PASS reconstructed base_clauses=" << base << " degree_clauses=" << degree
            << " prefix_and_symmetry_clauses=" << f.size()-base-degree << '\n';
  return f;
}

Formula read_cnf(const std::string &path,int variables) {
  std::ifstream in(path);
  check(bool(in),"cannot open CNF");
  std::string line;
  int declared=-1; bool header=false;
  Formula result;
  while(std::getline(in,line)) {
    if(line.empty() || line[0]=='c') continue;
    std::istringstream row(line);
    if(line[0]=='p') {
      std::string p,cnf,extra; int nv;
      check(!header && bool(row>>p>>cnf>>nv>>declared) && p=="p" && cnf=="cnf" &&
            nv==variables && declared>=0 && !(row>>extra),"bad CNF header");
      header=true; continue;
    }
    check(header,"clause before header");
    Clause c; int x; bool terminated=false;
    while(row>>x) {
      if(x==0) { terminated=true; break; }
      check(x>=-variables && x<=variables,"literal out of range"); c.push_back(x);
    }
    std::string extra;
    check(terminated && !(row>>extra) && !c.empty(),"malformed clause");
    std::sort(c.begin(),c.end());
    check(std::adjacent_find(c.begin(),c.end())==c.end(),"duplicate literal");
    for(int y:c) check(!std::binary_search(c.begin(),c.end(),-y),"tautological clause");
    result.push_back(std::move(c));
  }
  check(header && static_cast<int>(result.size())==declared,"clause count mismatch");
  return result;
}
} // namespace

int main(int argc,char **argv) {
  try {
    check(argc==3,"usage: independent_formula EDGE_LABELS.tsv FORMULA.cnf");
    check(gates[0].size()==2 && gates[1].size()==3 && gates[2].size()==4 && gates[3].size()==5,
          "truth-table prime-implicate counts differ");
    const auto mapping=read_edge_labels(argv[1]);
    int top=edge_vars;
    Formula want=expected(mapping,top), got=read_cnf(argv[2],top);
    std::sort(want.begin(),want.end()); std::sort(got.begin(),got.end());
    check(want==got,"complete CNF clause multiset differs");
    std::cout << "PASS edge_orbits=203 singleton_orbits=28 moving_orbits=175\n"
              << "PASS all_962598_five_sets_and_truth_table_gate_clauses_verified=true\n"
              << "PASS variables=" << top << " clauses=" << got.size()
              << " complete_formula_verified=true\n";
  } catch(const std::exception &e) {
    std::cerr << "ERROR: " << e.what() << '\n'; return 1;
  }
}
