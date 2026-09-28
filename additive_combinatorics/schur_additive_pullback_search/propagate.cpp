// Experimental complete search with global propagation on exact triples.
#include <chrono>
#include <cstdlib>
#include <iostream>
#include <vector>
struct Domain {bool zero=true; int nz;};
struct Triple {int x,y,z;};
struct State {std::vector<Domain> d; std::vector<int> value; bool normalized=false;};
struct Search {
  int n,m,all; long long cap,nodes=0,branches=0,rejected=0;
  bool unknown=false; std::vector<int> answer;
  std::vector<Triple> triples;
  std::vector<std::vector<int>> incident;
  Search(int n_,int m_,long long c):n(n_),m(m_),all(m+1),cap(c),incident(n+1) {
    for(int x=1;x<=n;++x) for(int y=x;x+y<=n;++y) {
      int i=triples.size();triples.push_back({x,y,x+y});
      incident[x].push_back(i);if(y!=x)incident[y].push_back(i);incident[x+y].push_back(i);
    }
  }
  // keep == all only removes zero; otherwise intersect with {0,keep},
  // where keep==0 denotes no permitted nonzero value.
  bool restrict(State &s,int v,bool permit_zero,int keep,std::vector<int>&queue) {
    Domain &d=s.d[v];d.zero=d.zero && permit_zero;
    if(keep!=all) {
      if(d.nz==all)d.nz=keep;
      else if(d.nz!=keep)d.nz=0;
    }
    if(!d.zero && d.nz==0)return false;
    int forced=all;
    if(d.zero && d.nz==0)forced=0;
    if(!d.zero && d.nz!=all)forced=d.nz;
    if(forced!=all && s.value[v]==all) {
      s.value[v]=forced;queue.push_back(v);
      if(forced!=0)s.normalized=true;
    }
    return true;
  }
  int bounded(int a) const {return a!=0 && a>=-m && a<=m?a:0;}
  bool propagate(State &s,std::vector<int>&queue) {
    for(size_t at=0;at<queue.size();++at) for(int i:incident[queue[at]]) {
      auto t=triples[i];int a=s.value[t.x],b=s.value[t.y],c=s.value[t.z];
      if(t.x==t.y) {
        if(a!=all) {
          if(a==0) {if(!restrict(s,t.z,false,all,queue))return false;}
          else if(!restrict(s,t.z,true,bounded(2*a),queue))return false;
        }
        if(c!=all) {
          if(c==0) {if(!restrict(s,t.x,false,all,queue))return false;}
          else if(!restrict(s,t.x,true,c%2==0?bounded(c/2):0,queue))return false;
        }
        continue;
      }
      int known=(a!=all)+(b!=all)+(c!=all);
      if(known==3) {
        if(a==0 && b==0 && c==0)return false;
        if(a!=0 && b!=0 && c!=0 && a+b!=c)return false;
      } else if(known==2) {
        int target,first,second,label;
        if(c==all) {target=t.z;first=a;second=b;label=a+b;}
        else if(a==all) {target=t.x;first=b;second=c;label=c-b;}
        else {target=t.y;first=a;second=c;label=c-a;}
        if(first==0 && second==0) {
          if(!restrict(s,target,false,all,queue))return false;
        } else if(first!=0 && second!=0) {
          if(!restrict(s,target,true,bounded(label),queue))return false;
        }
      }
    }
    return true;
  }
  bool visit(const State &s) {
    if(++nodes>cap) {unknown=true;return false;}
    int v=1;while(v<=n && s.value[v]!=all)++v;
    if(v>n) {answer=s.value;return true;}
    std::vector<int> values;
    if(s.d[v].zero)values.push_back(0);
    if(s.d[v].nz==all) {
      for(int a=-m;a<=m;++a)if(a!=0 && (s.normalized || a>0))values.push_back(a);
    } else if(s.d[v].nz!=0)values.push_back(s.d[v].nz);
    for(int a:values) {
      ++branches;State child=s;std::vector<int>queue;
      if(restrict(child,v,a==0,a,queue) && propagate(child,queue)) {
        if(visit(child))return true;
      } else ++rejected;
      if(unknown)return false;
    }
    return false;
  }
  bool run() {State s{std::vector<Domain>(n+1,Domain{true,all}),std::vector<int>(n+1,all),false};return visit(s);}
};
int main(int argc,char**argv) {
  if(argc<3)return 2;
  int n=std::atoi(argv[1]),m=std::atoi(argv[2]);
  long long cap=argc>3?std::atoll(argv[3]):100000;
  if(n<1 || n>2000 || m<1 || m>1000 || cap<1)return 2;
  auto start=std::chrono::steady_clock::now();Search s(n,m,cap);bool sat=s.run();
  std::cout<<"{\"n\":"<<n<<",\"m\":"<<m<<",\"status\":\""
    <<(sat?"SAT":s.unknown?"UNKNOWN":"UNSAT_ENUMERATION")<<"\",\"nodes\":"<<s.nodes
    <<",\"branches\":"<<s.branches<<",\"rejected\":"<<s.rejected
    <<",\"seconds\":"<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
  if(sat) {std::cout<<",\"labels\":[";for(int v=1;v<=n;++v)std::cout<<(v==1?"":",")<<s.answer[v];std::cout<<"]";}
  std::cout<<"}"<<std::endl;
}
