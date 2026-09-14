#include <array>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>
#include <cstdlib>
using V=std::array<long long,16>;
V conj(const V&a){V b{};for(int e=0;e<4;e++)for(int k=0;k<4;k++){
 long long x=a[4*e+k]*((e==1||e==2)?-1:1);
 if(k==1){for(int h=0;h<4;h++)b[4*e+h]-=x;}else b[4*e+(k?5-k:0)]+=x;
}return b;}
bool unit(const V&a,const V&b,const V&ca,const V&cb){V d{},c{},n{};
 for(int i=0;i<16;i++){d[i]=a[i]-b[i];c[i]=ca[i]-cb[i];}
 for(int i=0;i<16;i++)if(d[i])for(int j=0;j<16;j++)if(c[j]){
  int e=i/4,f=j/4,k=i%4+j%4,o=(e^f)*4;long long v=d[i]*c[j];
  if(e&f&1)v*=-3;
  if(e&f&2)v*=-11;
  if(k==4){for(int h=0;h<4;h++)n[o+h]-=v;}else n[o+k%5]+=v;
 }
 if(n[0]!=96*96)return false;
 for(int i=1;i<16;i++)if(n[i])return false;
 return true;
}
int main(int argc,char**argv){try{
 if(argc!=3)throw std::runtime_error("input and output required");
 std::ifstream in(argv[1]);std::ofstream out(argv[2]);int cases;in>>cases;
 if(!in||cases!=17)throw std::runtime_error("bad case count");
 long long pairs=0,edges=0;
 for(int k=0;k<cases;k++){int n;in>>n;if(!in||n<1||n>1801)throw std::runtime_error("bad order");std::vector<V>P(n),C(n);
  for(int i=0;i<n;i++){for(auto&x:P[i]){in>>x;if(!in||std::llabs(x)>1000000)throw std::runtime_error("coefficient bound");}C[i]=conj(P[i]);}
  for(int i=0;i<n;i++)for(int j=i+1;j<n;j++){pairs++;if(unit(P[i],P[j],C[i],C[j])){out<<k<<' '<<i<<' '<<j<<'\n';edges++;}}
 }
 std::string excess;if(in>>excess)throw std::runtime_error("trailing input");
 if(!out)throw std::runtime_error("output failure");
 std::cout<<"pairs="<<pairs<<" edges="<<edges<<'\n';
 }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}}
