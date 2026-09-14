#include <iostream>
#include <fstream>
#include <vector>
#include <array>
using I=long long;constexpr I p=1000000021;
I mm(I a,I b){return a*b%p;}I sub(I a,I b){return(a-b+p)%p;}
int main(int argc,char**argv){if(argc!=2)return 2;std::ifstream f(argv[1]);int n;I s;f>>n>>s;if(!f||n<490||n>100000||s<0||s>=p)return 2;std::vector<std::array<I,4>>P(n);for(auto&z:P)for(auto&x:z){f>>x;if(!f||x<0||x>=p)return 2;}
long long count=0,hits=0;
for(int j=490;j<n;j++)for(int i=0;i<j;i++){I a=sub(P[i][0],P[j][0]),ca=sub(P[i][1],P[j][1]),b=sub(P[i][2],P[j][2]),cb=sub(P[i][3],P[j][3]);count++;
if((mm(a,cb)+mm(ca,b))%p)continue;
if((mm(a,ca)+mm(s,mm(b,cb)))%p!=1)continue;
std::cout<<i<<' '<<j<<'\n';hits++;}
std::cerr<<"pairs "<<count<<" hits "<<hits<<'\n';return 0;}
