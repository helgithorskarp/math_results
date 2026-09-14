// Literal all-pairs integer norm audit, independent of quadratic event generation.
#include <array>
#include <iostream>
#include <stdexcept>
#include <vector>
#include <utility>
#include <set>
using I=__int128_t;
using Point=std::array<long long,16>;
const long long rad[8]={1,3,5,15,11,33,55,165};
void check(bool ok,const char*s){if(!ok)throw std::runtime_error(s);}
bool unit(const Point&a,const Point&b,long long den){
  I answer[8]={};
  for(int axis=0;axis<2;++axis){
    I d[8];for(int i=0;i<8;++i)d[i]=I(a[8*axis+i])-b[8*axis+i];
    for(int i=0;i<8;++i)if(d[i]){
      answer[0]+=rad[i]*d[i]*d[i];
      for(int j=i+1;j<8;++j)if(d[j])answer[i^j]+=2*rad[i&j]*d[i]*d[j];
    }
  }
  if(answer[0]!=I(den)*den)return false;
  for(int i=1;i<8;++i)if(answer[i])return false;
  return true;
}
int main(){try{
  int cases;std::cin>>cases;check(bool(std::cin)&&cases>0,"header");
  unsigned long long pairs=0,edges=0;
  for(int k=0;k<cases;++k){
    int n=0,m=0;long long den=0;std::cin>>n>>m>>den;
    check(bool(std::cin)&&n>0&&n<=530&&m>=0&&m<=n*(n-1)/2&&den>0&&den<(1LL<<50),"dimensions");
    std::vector<Point>P(n);
    for(auto&p:P)for(auto&x:p){std::cin>>x;check(bool(std::cin)&&x>-(1LL<<50)&&x<(1LL<<50),"coordinate bounds");}
    check(std::set<Point>(P.begin(),P.end()).size()==P.size(),"collision");
    std::vector<std::pair<int,int>>E(m);
    for(int i=0;i<m;++i){std::cin>>E[i].first>>E[i].second;check(bool(std::cin)&&0<=E[i].first&&E[i].first<E[i].second&&E[i].second<n,"edge domain");if(i)check(E[i-1]<E[i],"edge ordering");}
    int at=0;
    for(int i=0;i<n;++i)for(int j=i+1;j<n;++j){
      ++pairs;
      if(unit(P[i],P[j],den)){
        check(at<m&&E[at]==std::make_pair(i,j),"omitted or incorrect unit edge");++at;++edges;
      }
    }
    check(at==m,"listed non-unit edge");
  }
  std::string extra;check(!(std::cin>>extra),"trailing input");
  std::cout<<"{\"cases\":"<<cases<<",\"pairs\":"<<pairs<<",\"unit_edges\":"<<edges<<",\"status\":\"ALL_PHYSICAL_PAIRS_MATCH\"}\n";
}catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 1;}}
