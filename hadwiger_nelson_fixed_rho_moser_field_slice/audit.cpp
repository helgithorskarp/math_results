#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>
using I=__int128_t; using P=std::array<int64_t,8>;
void need(bool b,const char*s){if(!b)throw std::runtime_error(s);}
bool unit(const P&p,const P&q,int64_t den){
 I a=I(p[0])-q[0],b=I(p[1])-q[1],c=I(p[2])-q[2],d=I(p[3])-q[3];
 I e=I(p[4])-q[4],f=I(p[5])-q[5],g=I(p[6])-q[6],h=I(p[7])-q[7];
 I A=a*a+5*b*b+33*c*c+165*d*d+3*e*e+15*f*f+99*g*g+495*h*h;
 if(A!=I(den)*den)return false;
 return a*b+33*c*d+3*e*f+99*g*h==0 &&
        a*c+5*b*d+3*e*g+15*f*h==0 &&
        a*d+b*c+3*e*h+3*f*g==0;
}
int main(){try{
 std::ios::sync_with_stdio(false);std::cin.tie(nullptr);
 int cases;need(bool(std::cin>>cases),"case count");long long pairs=0,edges=0,collisions=0;
 for(int t=0;t<cases;++t){
  int n,expectn,m;int64_t den;need(bool(std::cin>>n>>den>>expectn>>m),"case header");
  need(n==343 && den>0 && den<(int64_t(1)<<50),"size or denominator bound");
  std::map<P,int> index;std::vector<P> ps;std::vector<int> colors;std::vector<int> labels;
  for(int i=0;i<n;++i){P p;for(auto&x:p){need(bool(std::cin>>x),"coordinate");need(x>-(int64_t(1)<<50)&&x<(int64_t(1)<<50),"coordinate overflow bound");}
   int col;need(bool(std::cin>>col)&&col>=0&&col<4,"colour");auto it=index.find(p);
   if(it==index.end()){int k=ps.size();index[p]=k;ps.push_back(p);colors.push_back(col);labels.push_back(k);}
   else{need(colors[it->second]==col,"colour does not descend");labels.push_back(it->second);++collisions;}
  }
  need(int(ps.size())==expectn,"collision count");
  std::vector<std::vector<bool>> expected(expectn,std::vector<bool>(expectn,false));
  for(int i=0;i<m;++i){int a,b;need(bool(std::cin>>a>>b),"edge");need(a>=0&&a<b&&b<expectn&&!expected[a][b],"edge format");expected[a][b]=true;}
  int count=0;
  for(int a=0;a<expectn;++a)for(int b=a+1;b<expectn;++b){++pairs;bool edge=unit(ps[a],ps[b],den);
   need(edge==expected[a][b],"incomplete or spurious physical edge");if(edge){++count;++edges;need(colors[a]!=colors[b],"bad physical colouring");}}
  need(count==m,"edge count");
 }
 std::string rest;need(!(std::cin>>rest),"trailing input");
 std::cout<<"{\"status\":\"DIRECT_INTEGER_GEOMETRY_PASS\",\"cases\":"<<cases<<",\"merged_pair_checks\":"<<pairs<<",\"unit_edges_checked\":"<<edges<<",\"collision_address_losses\":"<<collisions<<"}\n";
 return 0;
}catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 1;}}
