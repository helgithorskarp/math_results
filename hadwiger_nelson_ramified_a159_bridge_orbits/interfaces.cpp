#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <vector>
using namespace std; using I=__int128_t; using Q=array<int64_t,8>;
bool unit(Q x,int64_t s){I a=x[0],b=x[1],c=x[2],d=x[3],e=x[4],f=x[5],g=x[6],h=x[7];return a*a+33*b*b+3*c*c+11*d*d+6*(e*e+33*f*f+3*g*g+11*h*h)==I(s)*s && 2*(a*b+c*d)+12*(e*f+g*h)==0 && a*e+33*b*f+3*c*g+11*d*h==0 && a*f+b*e+c*h+d*g==0;}
int main(int argc,char**argv){if(argc!=3)return 2;ifstream in(argv[1]);ofstream out(argv[2]);int n,m,k;int64_t s;in>>n>>m>>k>>s;if(!in||n<1||m<1||k<1||s<1)return 3;vector<Q>a(n),b(m);for(auto&p:a)for(auto&x:p)in>>x;uint64_t checks=0,hits=0,collisions=0;
for(int t=0;t<k;++t){for(auto&p:b)for(auto&x:p)in>>x;if(!in)return 4;for(int i=0;i<n;++i)for(int j=0;j<m;++j){Q d{};for(int c=0;c<8;++c)d[c]=a[i][c]-b[j][c];++checks;if(d==Q{}){out<<t<<' '<<i<<' '<<j<<" C\n";++collisions;}else if(unit(d,s)){out<<t<<' '<<i<<' '<<j<<" E\n";++hits;}}}cout<<checks<<' '<<hits<<' '<<collisions<<'\n';}
