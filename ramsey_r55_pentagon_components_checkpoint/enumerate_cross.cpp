#include <array>
#include <iostream>
#include <fstream>
#include <vector>
#include <cstdint>
using A=std::array<unsigned,10>;
bool cycle(const A& a,unsigned S){for(unsigned t=S;t;t&=t-1){int x=__builtin_ctz(t);if(__builtin_popcount(a[x]&S)!=2)return false;}return true;}
std::array<std::vector<unsigned>,10> subsets;
std::array<uint64_t,6> counts{};
std::ofstream out;
void dfs(A a,unsigned n,uint32_t m){counts[n-5]++;if(n==10){out<<m<<'\n';return;}
 for(unsigned r=0;r<32;r++){A b=a;b[n]=r;for(unsigned j=0;j<5;j++)if(r>>j&1)b[j]|=1U<<n;
 for(unsigned j=5;j<n;j++)if(n-j==1||n-j==4){b[n]|=1U<<j;b[j]|=1U<<n;}
 bool bad=false;for(unsigned s:subsets[n])if(cycle(b,s)){bad=true;break;}if(!bad)dfs(b,n+1,m|(r<<(5*(n-5))));}}
int main(int argc,char**argv){if(argc!=2)return 2;out.open(argv[1]);if(!out)return 2;A a{};for(unsigned i=0;i<5;i++)a[i]=(1U<<((i+1)%5))|(1U<<((i+4)%5));for(unsigned n=5;n<10;n++)for(unsigned s=0;s<(1U<<n);s++)if(__builtin_popcount(s)==4&&(s&31))subsets[n].push_back(s|(1U<<n));dfs(a,5,0);for(auto c:counts)std::cout<<c<<' ';std::cout<<'\n';return !out;}
