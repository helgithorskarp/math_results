#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>
using I=long long;
I p;
I norm(I a){a%=p;return a<0?a+p:a;}
I mul(I a,I b){return a*b%p;}
I power(I a,I e){I r=1;for(;e;e>>=1,a=mul(a,a))if(e&1)r=mul(r,a);return r;}
I sqnorm(I x,I y){return (mul(x,x)+3*mul(y,y))%p;}
int main(int argc,char**argv){try{
 if(argc!=3)throw std::runtime_error("input and output required");
 std::ifstream in(argv[1]);int n;in>>p>>n;
 if(!in||p<1000||p>1000001000||n!=509)throw std::runtime_error("invalid header");
 std::vector<std::array<I,2>> P(n);
 for(auto&v:P)for(auto&x:v){in>>x;if(!in||x<0||x>=p)throw std::runtime_error("invalid coordinate");}
 std::string extra;if(in>>extra)throw std::runtime_error("trailing input");
 std::ofstream out(argv[2],std::ios::binary);I comparisons=0;
 for(int a=0;a<n;a++){
  std::vector<std::array<I,2>> Q;
  for(int i=0;i<n;i++)if(i!=a){I x=norm(P[i][0]-P[a][0]),y=norm(P[i][1]-P[a][1]);I d=sqnorm(x,y);
   if(!d)throw std::runtime_error("zero pole distance");
   I inverse=power(d,p-2);Q.push_back({mul(x,inverse),mul(y,inverse)});
  }
  std::vector<unsigned char> row;row.reserve(128778*4);
  for(int i=0;i<508;i++)for(int j=i+1;j<508;j++){
   I d=sqnorm(norm(Q[i][0]-Q[j][0]),norm(Q[i][1]-Q[j][1]));
   if(!d)throw std::runtime_error("zero inverted distance");
   for(int k=0;k<4;k++)row.push_back(static_cast<unsigned char>((d>>(8*k))&255));
   comparisons++;
  }
  out.write(reinterpret_cast<const char*>(row.data()),row.size());
 }
 if(!out)throw std::runtime_error("write failed");
 std::cout<<"pairs="<<comparisons<<"\n";
}catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}}
