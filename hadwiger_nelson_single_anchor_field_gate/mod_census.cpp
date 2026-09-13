#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <unordered_map>
#include <vector>
using I=long long; const I P=1000000021;
I mm(I a,I b){return a*b%P;} I pw(I a,I n){I r=1;for(;n;n>>=1,a=mm(a,a))if(n&1)r=mm(r,a);return r;}
struct Z{I z,c;};struct H{size_t operator()(const std::pair<I,I>&x)const{return x.first*1000000007ULL+x.second;}};
int main(int argc,char**argv){if(argc!=2)return 2;std::ifstream f(argv[1]);int n,k,m;f>>n>>k>>m;if(!f||n<2||n>500||k<1||k>20||m<2||m>10)return 2;std::vector<Z>A(n);for(auto&z:A)f>>z.z>>z.c;
std::vector<std::vector<Z>>B(k,std::vector<Z>(m));for(auto&b:B)for(auto&z:b)f>>z.z>>z.c;
if(!f)return 2;
for(auto z:A)if(z.z<0||z.z>=P||z.c<0||z.c>=P)return 2;
for(auto b:B)for(auto z:b)if(z.z<0||z.z>=P||z.c<0||z.c>=P)return 2;
long long cases=0,kept=0,singular=0;
for(int p=0;p<n;p++){std::vector<Z>D(n),IV(n);std::vector<I>N(n);for(int r=0;r<n;r++)if(r!=p){D[r]={(A[p].z-A[r].z+P)%P,(A[p].c-A[r].c+P)%P};if(!D[r].c){singular++;continue;}IV[r]={pw(D[r].z,P-2),pw(D[r].c,P-2)};N[r]=mm(D[r].z,D[r].c);}
for(int k0=0;k0<k;k0++){std::unordered_map<std::pair<I,I>,std::vector<std::pair<int,int>>,H> G;
for(int j=1;j<m;j++){Z b=B[k0][j];I nb=mm(b.z,b.c),bi=pw(b.z,P-2);if(!b.z){singular++;continue;}
for(int r=0;r<n;r++)if(r!=p&&D[r].c){I ci=mm(IV[r].c,bi),h=(N[r]+nb+P-1)%P;I t=(P-mm(h,ci))%P,jj=mm(mm(D[r].z,b.c),ci);G[{t,jj}].push_back({r,j});cases++;}}
std::vector<std::vector<int>> records;for(auto&[key,ev]:G){std::vector<int> old;for(auto [r,j]:ev)old.push_back(r);std::sort(old.begin(),old.end());old.erase(std::unique(old.begin(),old.end()),old.end());if(old.size()<3)continue;
std::sort(ev.begin(),ev.end());std::vector<int> row;row.push_back(p);row.push_back(k0);row.push_back(static_cast<int>(ev.size()));for(auto [r,j]:ev){row.push_back(r);row.push_back(j);}records.push_back(row);kept++;}std::sort(records.begin(),records.end());for(auto row:records){for(auto z:row)std::cout<<z<<' ';std::cout<<'\n';}}
}std::cerr<<"cases "<<cases<<" kept "<<kept<<" singular "<<singular<<"\n";return singular?3:0;}
