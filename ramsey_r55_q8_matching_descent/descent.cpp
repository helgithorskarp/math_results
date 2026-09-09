#include <algorithm>
#include <array>
#include <bit>
#include <chrono>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <functional>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>
using I = std::int64_t;
struct Constraint { std::array<int,10> edge{}; int size=0; bool both=true; };
struct Poly { I c=0; std::vector<I> a; std::vector<std::vector<I>> b; };
struct Graph {
  int n,k,tail; std::string bits,fixed;
  std::vector<std::pair<int,int>> pairs;
  std::vector<std::vector<int>> id, match;
  std::vector<Constraint> clauses;
  explicit Graph(const std::string& file) {
    std::ifstream in(file); if (!(in>>n>>k>>tail>>bits>>fixed)) throw std::runtime_error("input");
    if(n<3 || n>43 || k<3 || k>5 || tail<0 || tail>n) throw std::runtime_error("dimensions");
    if(bits.size()!=static_cast<std::size_t>(n*(n-1)/2) || fixed.size()!=bits.size()) throw std::runtime_error("length");
    for(char c:bits+fixed) if(c!='0' && c!='1') throw std::runtime_error("bit");
    id.assign(n,std::vector<int>(n,-1));
    for(int u=0;u<n;u++) for(int v=u+1;v<n;v++) { id[u][v]=id[v][u]=static_cast<int>(pairs.size()); pairs.emplace_back(u,v); }
    auto add=[&](int begin,int size,bool both) {
      std::vector<int> q;
      std::function<void(int)> visit=[&](int next) {
        if(q.size()==static_cast<std::size_t>(size)) {
          Constraint t; t.both=both;
          for(int i=0;i<size;i++) for(int j=i+1;j<size;j++) t.edge[t.size++]=id[q[i]][q[j]];
          clauses.push_back(t); return;
        }
        for(int v=next;v<n;v++) { q.push_back(v); visit(v+1); q.pop_back(); }
      }; visit(begin);
    };
    add(0,k,true); if(tail<n) add(tail,4,false);
    const int N=(n%2)?n+1:n;
    for(int r=0;r<N-1;r++) {
      std::vector<int> m;
      auto put=[&](int u,int v) { if(u<n && v<n && fixed[id[u][v]]=='0') m.push_back(id[u][v]); };
      put(N-1,r);
      for(int j=1;j<N/2;j++) put((r+j)%(N-1),(r-j+N-1)%(N-1));
      std::sort(m.begin(),m.end()); match.push_back(m);
    }
    std::vector<int> seen(bits.size());
    for(const auto& m:match) for(int e:m) seen[e]++;
    for(std::size_t e=0;e<bits.size();e++) if(seen[e]!=(fixed[e]=='0')) throw std::runtime_error("factorization");
  }
  I cost() const {
    I total=0;
    for(const auto& t:clauses) {
      int red=0; for(int j=0;j<t.size;j++) red+=bits[t.edge[j]]=='1';
      total+=(red==t.size); total+=(t.both && red==0);
    } return total;
  }
  Poly polynomial(int r) const {
    const auto& m=match.at(r); const int dim=static_cast<int>(m.size());
    Poly p; p.a.assign(dim,0); p.b.assign(dim,std::vector<I>(dim,0));
    std::vector<int> pos(bits.size(),-1); for(int j=0;j<dim;j++) pos[m[j]]=j;
    for(const auto& t:clauses) {
      int color=-1, count=0; std::array<int,2> var{},old{}; bool mixed=false;
      for(int j=0;j<t.size;j++) {
        const int e=t.edge[j], x=bits[e]-'0';
        if(pos[e]>=0) { if(count==2) throw std::runtime_error("not quadratic"); var[count]=pos[e]; old[count++]=x; }
        else { if(color>=0 && color!=x) { mixed=true; break; } color=x; }
      }
      if(mixed || (!t.both && color==0)) continue;
      if(color<0) throw std::runtime_error("no fixed pair in subset");
      if(count==0) { p.c++; continue; }
      const int i=var[0], x=old[0]^color;
      if(count==1) { if(x) p.a[i]++; else {p.c++;p.a[i]--;} continue; }
      const int j=var[1], y=old[1]^color;
      I coupling=0;
      if(!x && !y) {p.c++;p.a[i]--;p.a[j]--;coupling=1;}
      else if(!x && y) {p.a[j]++;coupling=-1;}
      else if(x && !y) {p.a[i]++;coupling=-1;}
      else coupling=1;
      p.b[i][j]+=coupling;p.b[j][i]+=coupling;
    } return p;
  }
};
std::pair<I,std::uint64_t> minimum(const Poly& p) {
  const unsigned m=static_cast<unsigned>(p.a.size()); if(m>21) throw std::runtime_error("dimension");
  std::vector<I> field=p.a; I val=0,best=0; std::uint64_t mask=0,winner=0;
  for(std::uint64_t t=1;t<(std::uint64_t{1}<<m);t++) {
    const unsigned k=std::countr_zero(t); const I sign=((mask>>k)&1)?-1:1;
    val+=sign*field[k];mask^=std::uint64_t{1}<<k;
    for(unsigned j=0;j<m;j++) if(j!=k) field[j]+=sign*p.b[k][j];
    if(val<best) {best=val;winner=mask;}
  } return {p.c+best,winner};
}
void writepoly(const Poly& p) {
  std::cout<<p.a.size()<<' '<<p.c<<'\n';
  for(I x:p.a)std::cout<<x<<' ';
  std::cout<<'\n';
  for(const auto& row:p.b) {for(I x:row)std::cout<<x<<' ';std::cout<<'\n';}
}
int main(int argc,char** argv) { try {
  if(argc<3) throw std::runtime_error("usage: descent MODE INPUT [ARG]");
  const std::string mode=argv[1];
  if(mode=="benchmark") {
    Poly p;p.a.assign(21,1);p.b.assign(21,std::vector<I>(21,0));
    const auto start=std::chrono::steady_clock::now();const auto [v,m]=minimum(p);
    if(v!=0 || m!=0)throw std::runtime_error("benchmark truth");
    std::cout<<"{\"assignments\":2097152,\"variables\":21,\"seconds\":"
      <<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<"}\n";
    return 0;
  }
  Graph g(argv[2]);
  if(mode=="poly" || mode=="min") {
    if(argc!=4)throw std::runtime_error("index");
    const int r=std::stoi(argv[3]); const auto p=g.polynomial(r);
    if(p.c!=g.cost())throw std::runtime_error("constant");
    if(mode=="poly")writepoly(p); else {const auto [v,m]=minimum(p);std::cout<<v<<' '<<m<<'\n';}
    return 0;
  }
  if(mode!="run" || argc!=4)throw std::runtime_error("mode");
  const std::filesystem::path out(argv[3]); if(!std::filesystem::create_directory(out))throw std::runtime_error("existing output");
  std::ofstream started(out/"STARTED");started<<"single writer; do not restart\n";started.close();
  std::ofstream trace(out/"trace.tsv"); trace<<"sweep\tmatching\tbefore\tafter\tmask\n";
  const auto begin=std::chrono::steady_clock::now(); I score=g.cost(); const I initial=score;
  int sweep=0,moves=0,kernels=0;
  while(score>0) {
    bool changed=false;sweep++;
    for(int r=0;r<static_cast<int>(g.match.size());r++) {
      const auto p=g.polynomial(r);if(p.c!=score)throw std::runtime_error("score mismatch");
      const auto [next,mask]=minimum(p); kernels++;
      if(next>score || (next==score && mask!=0))throw std::runtime_error("nonmonotone tie");
      trace<<sweep<<'\t'<<r<<'\t'<<score<<'\t'<<next<<'\t'<<mask<<'\n';trace.flush();
      if(next<score) {
        for(unsigned j=0;j<g.match[r].size();j++)if((mask>>j)&1)g.bits[g.match[r][j]]^=1;
        if(g.cost()!=next)throw std::runtime_error("physical score");
        score=next;changed=true;moves++;
        std::ofstream state(out/"latest.txt");state<<g.n<<' '<<g.k<<' '<<g.tail<<'\n'<<g.bits<<'\n'<<g.fixed<<'\n';
      }
      if(score==0)break;
    }
    std::cout<<"sweep "<<sweep<<" score "<<score<<" accepted "<<moves<<std::endl;
    if(!changed)break;
  }
  std::ofstream end(out/"endpoint.txt");end<<g.n<<' '<<g.k<<' '<<g.tail<<'\n'<<g.bits<<'\n'<<g.fixed<<'\n';end.close();
  const double elapsed=std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count();
  std::ofstream receipt(out/"RESULT.json");
  receipt<<"{\"status\":\""<<(score==0?"UNVERIFIED_TARGET":"MATCHING_STATIONARY_NONZERO")<<"\",\"initial\":"<<initial<<",\"final\":"<<score<<",\"sweeps\":"<<sweep<<",\"accepted_moves\":"<<moves<<",\"exact_kernels\":"<<kernels<<",\"elapsed_seconds\":"<<elapsed<<"}\n";
  return 0;
} catch(const std::exception& e) {std::cerr<<e.what()<<'\n';return 1;} }
