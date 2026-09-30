// six-vdw-1, researcher. Direct independent full-cyclic encoder.
// Explicit cosets for H2/H3; signed affine orbits for the reflection template.
#include <algorithm>
#include <array>
#include <cstdlib>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>
using Clause = std::vector<int>;
void require(bool b,const char* s) { if (!b) throw std::runtime_error(s); }
int power(int a,int e) { int r=1; for (int j=0;j<e;++j) r=r*a%103; return r; }

int main(int argc,char** argv) {
  try {
    require(argc==2,"usage: direct_encode h2|h3|reflection");
    const std::string family=argv[1];
    require(family=="h2" || family=="h3" || family=="reflection","bad family");
    std::array<int,618> lookup{};
    const bool reflection=family=="reflection";
    const int index=family=="h2" ? 51 : 34;
    if (!reflection) {
      std::array<int,103> ids; ids.fill(-1); ids[0]=index;
      const int generator=power(5,index);
      for (int i=0;i<index;++i) {
        const int representative=power(5,i); int x=representative;
        for (int j=0;j<102/index;++j) {
          require(ids[static_cast<std::size_t>(x)]==-1,"overlapping cosets");
          ids[static_cast<std::size_t>(x)]=i; x=x*generator%103;
        }
        require(x==representative,"wrong subgroup order");
      }
      for (int id:ids) require(id>=0,"incomplete coset coverage");
      for (int t=0;t<618;++t) {
        const int v=3*ids[static_cast<std::size_t>(t%103)]+t%3+1;
        lookup[static_cast<std::size_t>(t)]=t%6<3 ? v : -v;
      }
    } else {
      auto put=[&](int t,int value) {
        auto& slot=lookup[static_cast<std::size_t>(t)];
        require(slot==0 || slot==value,"inconsistent signed orbit"); slot=value;
      };
      for (int x=1;x<=51;++x) for (int y=0;y<3;++y) {
        const int t=x+103*(((y-x)%6+6)%6);
        const int v=3*(x-1)+y+1;
        put(t,v); put((t+309)%618,-v);
        put((206-t+618)%618,v); put((515-t+618)%618,-v);
      }
      for (int j=0;j<6;++j) {
        require(lookup[static_cast<std::size_t>(103*j)]==0,"zero orbit overlap");
        put(103*j,j<3 ? 154 : -154);
      }
      for (int t=0;t<618;++t) {
        require(lookup[static_cast<std::size_t>(t)]!=0,"incomplete orbit coverage");
        require(lookup[static_cast<std::size_t>((t+309)%618)]==-lookup[static_cast<std::size_t>(t)],"bad antipodal relation");
        require(lookup[static_cast<std::size_t>((206-t+618)%618)]==lookup[static_cast<std::size_t>(t)],"bad reflection relation");
      }
    }
    std::set<Clause> constraints;
    for (int d=1;d<618;++d) for (int a=0;a<618;++a) {
      Clause edge;
      for (int j=0;j<7;++j) edge.push_back(lookup[static_cast<std::size_t>((a+j*d)%618)]);
      for (int sign:{1,-1}) {
        Clause c; bool tautology=false;
        for (int v:edge) {
          const int lit=sign*v;
          if (reflection && std::abs(lit)==154) {
            if (lit<0) tautology=true;
          } else c.push_back(lit);
        }
        std::sort(c.begin(),c.end()); c.erase(std::unique(c.begin(),c.end()),c.end());
        for (int v:c) if (std::binary_search(c.begin(),c.end(),-v)) tautology=true;
        if (tautology) continue;
        if (!reflection) {
          Clause opposite; for (int v:c) opposite.push_back(-v);
          std::sort(opposite.begin(),opposite.end()); c=std::min(c,opposite);
        }
        constraints.insert(c);
      }
    }
    const int variables=reflection ? 153 : 3*(index+1);
    std::cout<<"p cnf "<<variables<<' '<<(reflection ? constraints.size() : 2*constraints.size()+3)<<'\n';
    for (const auto& c:constraints) { for (int v:c) std::cout<<v<<' '; std::cout<<"0\n"; }
    if (!reflection) {
      for (const auto& c:constraints) { for (int v:c) std::cout<<-v<<' '; std::cout<<"0\n"; }
      for (int k=1;k<=3;++k) std::cout<<-(3*index+k)<<" 0\n";
    }
    require(bool(std::cout),"output failed");
    return 0;
  } catch (const std::exception& e) { std::cerr<<e.what()<<'\n'; return 2; }
}
