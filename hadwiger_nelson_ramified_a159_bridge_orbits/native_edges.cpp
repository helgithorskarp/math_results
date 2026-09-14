#include <array>
#include <fstream>
#include <iostream>
#include <vector>
using namespace std;
int main(int argc,char**argv){if(argc!=3)return 2;ifstream in(argv[1]);ofstream out(argv[2]);int n;in>>n;vector<array<long long,4>>p(n);for(auto&v:p)for(auto&x:v)in>>x;unsigned long long count=0;for(int i=0;i<n;++i)for(int j=0;j<i;++j){long long a=p[i][0]-p[j][0],b=p[i][1]-p[j][1],c=p[i][2]-p[j][2],d=p[i][3]-p[j][3];if(a*a+33*b*b+3*c*c+11*d*d==144*144&&a*b+c*d==0){out<<j<<' '<<i<<'\n';++count;}}cout<<n<<' '<<count<<'\n';}
