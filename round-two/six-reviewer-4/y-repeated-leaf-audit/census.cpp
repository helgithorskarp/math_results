// six-reviewer-4: independent physical-neighbor census for LEMMA9327.
// Defining proof and claimed totals visible; no author source/fixtures imported.
// Prior owned 9537 supplies the credited general projection method, not inputs.
#include <array>
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using U=std::uint32_t;
int pc(U x){return __builtin_popcount(x);}
U bit(int i){return U(1)<<i;}
void need(bool b,const char*s){if(!b)throw std::runtime_error(s);}
struct G{
 std::array<U,22> r{};
 void edge(int i,int j){need(i!=j,"loop");r[i]|=bit(j);r[j]|=bit(i);}
};
void row(G&g,int i,int start,int mask,int n){for(int j=0;j<n;++j)if(mask&(1<<j))g.edge(i,start+j);}
std::vector<int> subsets(int rank){std::vector<int>a;for(int i=0;i<64;++i)if(pc(i)==rank)a.push_back(i);return a;}
G core(){
 G g;g.edge(0,1);g.edge(0,2);g.edge(1,2);
 for(int i=3;i<=10;++i)g.edge(0,i);
 for(int t=13;t<=15;++t)g.edge(2,t);
 g.edge(2,9);g.edge(2,10);
 const std::array<int,6> cycle={0,4,3,1,2,5};
 for(int k=0;k<6;++k)g.edge(3+cycle[k],3+cycle[(k+1)%6]);
 g.edge(9,6);g.edge(9,8);g.edge(10,5);g.edge(10,7);
 row(g,9,13,5,3);row(g,10,13,3,3);
 return g;
}
// All colors of known pairs are assigned. The omitted vertices are unrestricted.
// For each color, intersection size >= max(0, both row sizes - omitted count).
bool projected(const G&g,U known,const std::array<int,22>&d,int omitted,
               std::array<int,22>&q){
 std::array<U,22>b{};
 for(int i=0;i<22;++i)if(known&bit(i)){
  q[i]=d[i]-pc(g.r[i]&known);if(q[i]<0||q[i]>omitted)return false;
  b[i]=known&~(g.r[i]|bit(i));
 }
 for(int i=0;i<22;++i)if(known&bit(i))for(int j=i+1;j<22;++j)if(known&bit(j)){
  if(g.r[i]&bit(j)){
   if(pc(g.r[i]&g.r[j]&known)+std::max(0,q[i]+q[j]-omitted)>3)return false;
  }else if(pc(b[i]&b[j])+std::max(0,omitted-q[i]-q[j])>6)return false;
 }
 return true;
}
int main(int argc,char**argv){try{
 need(argc==2,"usage: census OUTPUT_PREFIX");std::string p=argv[1];
 std::ofstream out(p+"-interfaces.txt"),meta(p+"-counts.txt");need(out.good()&&meta.good(),"output");
 const U k16=(bit(16)-1),k14=k16&~(bit(11)|bit(12));
 std::array<std::uint64_t,32> tested{},survive{};
 std::uint64_t total=0;
 for(int tf=0;tf<8;++tf){
  int l0=tf&1,l1=(tf>>1)&1,l2=(tf>>2)&1;
  std::array<int,22>d{};d.fill(10);d[2]=9;d[13]-=l0;d[14]-=l1;d[15]-=l2;
  auto a=subsets(3-l0),b=subsets(4-l1),c=subsets(4-l2);
  std::uint64_t triples=0,pass14=0;
  for(int t0:a)for(int t1:b)for(int t2:c){
   ++triples;G g=core();row(g,13,3,t0,6);row(g,14,3,t1,6);row(g,15,3,t2,6);
   std::array<int,22>q{};if(!projected(g,k14,d,8,q))continue;++pass14;
   for(int s0=0;s0<64;++s0)if(pc(s0)==3||pc(s0)==4)
    for(int s1=0;s1<64;++s1)if(pc(s1)==3||pc(s1)==4){
     int ls0=4-pc(s0),ls1=4-pc(s1),flag=tf|(ls0<<3)|(ls1<<4);
     if(pc(flag)>3)continue;
     ++tested[flag];G h=g;
     for(int s=11;s<=12;++s){h.edge(1,s);h.edge(2,s);row(h,s,13,6,3);}
     row(h,11,3,s0,6);row(h,12,3,s1,6);d[11]=10-ls0;d[12]=10-ls1;
     if(!projected(h,k16,d,6,q))continue;
     ++survive[flag];++total;
     out<<flag<<' '<<t0<<' '<<t1<<' '<<t2<<' '<<s0<<' '<<s1;
     for(int i=3;i<9;++i)out<<' '<<q[i];
     out<<'\n';
     need(q[0]==0&&q[1]==6&&q[2]==0,"root ranks");
     need(q[9]==4&&q[10]==4&&q[11]==2&&q[12]==2,"special ranks");
     need(q[13]==4&&q[14]==2&&q[15]==2,"T ranks");
    }
  }
  meta<<"T "<<tf<<' '<<triples<<' '<<pass14<<'\n';
 }
 for(int flag=0;flag<32;++flag)if(pc(flag)<=3)meta<<"F "<<flag<<' '<<tested[flag]<<' '<<survive[flag]<<'\n';
 meta<<"complete "<<total<<'\n';need(out.good()&&meta.good(),"write");std::cout<<"complete "<<total<<'\n';
 return 0;
}catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 2;}}
