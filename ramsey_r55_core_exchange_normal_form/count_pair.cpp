#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <vector>
#include <stdexcept>
using U=std::uint64_t;
U count(const std::vector<int>& d,bool blue){
 const int n=static_cast<int>(d.size());U total=0;
 for(int x=0;x<=n;++x)for(int y=0;y<=n;++y){
  std::array<U,256> a{},b{};a[0]=1;
  int used=0;
  for(int degree:d){
   b.fill(0);int f0=blue?(degree<n-1-x):(degree<x);int f1=blue?(degree<n-1-y):(degree<y);
   for(int i=0;i<=std::min(x,used);++i)for(int j=0;j<=std::min(y,used);++j){
    U v=a[16*i+j];if(!v)continue;
    b[16*i+j]+=4*v;
    if(i<x)b[16*(i+1)+j]+=(4-f1)*v;
    if(j<y)b[16*i+j+1]+=(4-f0)*v;
    if(i<x&&j<y)b[16*(i+1)+j+1]+=3*v;
   }
   a=b;++used;
  }
  total+=a[16*x+y];
 }
 return total;
}
int main(){int id,n;while(std::cin>>id>>n){if(n<1||n>15)throw std::runtime_error("n");std::vector<int>d(n);for(int&i:d){if(!(std::cin>>i)||i<0||i>=n)throw std::runtime_error("degree");}std::cout<<id<<' '<<count(d,false)<<' '<<count(d,true)<<'\n';}return 0;}
