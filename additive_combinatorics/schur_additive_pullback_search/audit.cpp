// Separate implementation using literal bit domains and integer equation rows.
// Rows are formed in z-first order, with repeated variables combined.
#include <array>
#include <bitset>
#include <chrono>
#include <cstdlib>
#include <iostream>
#include <vector>
using Bits=std::bitset<321>;
struct Row {int size; std::array<int,3> vertex,coefficient;};
struct State {std::vector<Bits> domain;std::vector<int> fixed;bool any_nonzero=false;};
struct Audit {
  int n,m,unset;long long cap,nodes=0,branches=0,rejected=0;bool unknown=false;
  std::vector<Row> rows;std::vector<std::vector<int>> incident;std::vector<int> answer;
  Bits alphabet,nonzero;
  Audit(int n_,int m_,long long c):n(n_),m(m_),unset(m+1),cap(c),incident(n+1) {
    for(int p=0;p<=2*m;++p)alphabet.set(p);
    nonzero=alphabet;nonzero.reset(m);
    for(int z=2;z<=n;++z)for(int x=1;x<=z/2;++x) {
      int y=z-x,id=rows.size();
      Row r=x==y?Row{2,{x,z,0},{2,-1,0}}:Row{3,{x,y,z},{1,1,-1}};
      rows.push_back(r);for(int j=0;j<r.size;++j)incident[r.vertex[j]].push_back(id);
    }
  }
  bool meet(State &s,int v,const Bits &allowed,std::vector<int>&events) {
    Bits next=s.domain[v]&allowed;
    if(next.none())return false;
    if(next==s.domain[v])return true;
    s.domain[v]=next;
    if(next.count()==1 && s.fixed[v]==unset) {
      int p=0;while(!next.test(p))++p;
      s.fixed[v]=p-m;events.push_back(v);
      if(p!=m)s.any_nonzero=true;
    }
    return true;
  }
  bool close(State &s,std::vector<int>&events) {
    for(size_t e=0;e<events.size();++e)for(int index:incident[events[e]]) {
      const Row &r=rows[index];int missing=0,last=-1,total=0,zeros=0,known=0;
      for(int j=0;j<r.size;++j) {
        int value=s.fixed[r.vertex[j]];
        if(value==unset) {++missing;last=j;}
        else {++known;zeros+=(value==0);total+=r.coefficient[j]*value;}
      }
      if(missing==0) {
        if(zeros==known || (zeros==0 && total!=0))return false;
      } else if(missing==1) {
        int v=r.vertex[last];
        if(zeros==known) {
          if(!meet(s,v,nonzero,events))return false;
        } else if(zeros==0) {
          Bits allowed;allowed.set(m);int coefficient=r.coefficient[last];
          if(total%coefficient==0) {
            int value=-total/coefficient;
            if(value!=0 && value>=-m && value<=m)allowed.set(value+m);
          }
          if(!meet(s,v,allowed,events))return false;
        }
      }
    }
    return true;
  }
  bool visit(const State &s) {
    if(++nodes>cap){unknown=true;return false;}
    int v=1;while(v<=n && s.fixed[v]!=unset)++v;
    if(v>n){answer=s.fixed;return true;}
    std::vector<int> options;
    if(s.domain[v].test(m))options.push_back(0);
    for(int a=-m;a<=m;++a)
      if(a!=0 && (s.any_nonzero || a>0) && s.domain[v].test(a+m))options.push_back(a);
    for(int a:options) {
      ++branches;State child=s;Bits one;one.set(a+m);std::vector<int>events;
      if(meet(child,v,one,events) && close(child,events)) {
        if(visit(child))return true;
      } else ++rejected;
      if(unknown)return false;
    }
    return false;
  }
  bool run(){State s{std::vector<Bits>(n+1,alphabet),std::vector<int>(n+1,unset),false};return visit(s);}
};
int main(int argc,char**argv) {
  if(argc<3)return 2;
  int n=std::atoi(argv[1]),m=std::atoi(argv[2]);long long cap=argc>3?std::atoll(argv[3]):5000000;
  if(n<1 || n>2000 || m<1 || m>160 || cap<1)return 2;
  auto start=std::chrono::steady_clock::now();Audit a(n,m,cap);bool sat=a.run();
  std::cout<<"{\"n\":"<<n<<",\"m\":"<<m<<",\"status\":\""
    <<(sat?"SAT":a.unknown?"UNKNOWN":"UNSAT_ENUMERATION")<<"\",\"nodes\":"<<a.nodes
    <<",\"branches\":"<<a.branches<<",\"rejected\":"<<a.rejected
    <<",\"seconds\":"<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
  if(sat){std::cout<<",\"labels\":[";for(int v=1;v<=n;++v)std::cout<<(v==1?"":",")<<a.answer[v];std::cout<<"]";}
  std::cout<<"}"<<std::endl;
}
