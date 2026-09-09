// Independent lower-bound recursion for a supplied finite-difference polynomial.
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <vector>
using I=std::int64_t;
struct Check {
  int n; std::vector<I> field,negative;
  std::vector<std::vector<I>> b; std::uint64_t nodes=0,witness=0; I value=0;
  bool visit(int at,I partial,std::uint64_t chosen) {
    nodes++;
    I lower=partial+negative[at];
    for(int j=at;j<n;j++) lower+=std::min<I>(0,field[j]);
    if(lower>=0) return true;
    if(at==n) { witness=chosen;value=partial;return false; }
    if(!visit(at+1,partial,chosen))return false;
    const I add=field[at];
    for(int j=at+1;j<n;j++)field[j]+=b[at][j];
    const bool ok=visit(at+1,partial+add,chosen|(std::uint64_t{1}<<at));
    for(int j=at+1;j<n;j++)field[j]-=b[at][j];
    return ok;
  }
};
int main(int argc,char** argv) { try {
  if(argc!=2)throw std::runtime_error("usage: certify POLYNOMIALS");
  std::ifstream in(argv[1]);int count;
  if(!(in>>count) || count<1)throw std::runtime_error("count");
  for(int index=0;index<count;index++) {
    Check c;I constant;
    if(!(in>>c.n>>constant) || c.n<0 || c.n>21)throw std::runtime_error("dimension");
    std::vector<I> a(c.n);std::vector<std::vector<I>> b(c.n,std::vector<I>(c.n));
    for(auto& x:a)if(!(in>>x))throw std::runtime_error("linear");
    for(auto& row:b)for(auto& x:row)if(!(in>>x))throw std::runtime_error("quadratic");
    for(int i=0;i<c.n;i++)for(int j=0;j<c.n;j++) {
      if(b[i][j]!=b[j][i] || (i==j && b[i][j]!=0))throw std::runtime_error("symmetric zero diagonal");
      if(b[i][j]>10000000 || b[i][j]<-10000000)throw std::runtime_error("coefficient bound");
    }
    for(I x:a)if(x>10000000 || x<-10000000)throw std::runtime_error("linear bound");
    std::vector<int> order(c.n);std::iota(order.begin(),order.end(),0);
    std::stable_sort(order.begin(),order.end(),[&](int i,int j){return a[i]>a[j];});
    c.field.resize(c.n);c.b.assign(c.n,std::vector<I>(c.n));
    for(int i=0;i<c.n;i++){c.field[i]=a[order[i]];for(int j=0;j<c.n;j++)c.b[i][j]=b[order[i]][order[j]];}
    c.negative.assign(c.n+1,0);
    for(int i=c.n-1;i>=0;i--){c.negative[i]=c.negative[i+1];for(int j=i+1;j<c.n;j++)c.negative[i]+=std::min<I>(0,c.b[i][j]);}
    if(!c.visit(0,0,0)) {
      std::uint64_t original=0;for(int i=0;i<c.n;i++)if((c.witness>>i)&1)original|=std::uint64_t{1}<<order[i];
      std::cout<<"NEGATIVE "<<index<<' '<<c.value<<' '<<original<<' '<<c.nodes<<'\n';return 2;
    }
    std::cout<<"NONNEGATIVE "<<index<<' '<<c.nodes<<'\n';
  }
  std::string extra;if(in>>extra)throw std::runtime_error("trailing input");
  return 0;
}catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 1;} }
