#include <cstdint>
using I=__int128_t;
using L=std::int64_t;
extern "C" int contacts(int n,L den,L sd,L s0,L s1,const L* p,int* edges){
 if(n<1||n>20000||den<1||den>1000000000||sd<1||sd>1000000000||s0 < -1000000000||s0>1000000000||s1 < -1000000000||s1>1000000000)return -1;
 for(int j=0;j<8*n;j++)if(p[j] < -1000000000||p[j]>1000000000)return -2;
 int e=0;
 for(int i=0;i<n;i++)for(int j=i+1;j<n;j++){
  I a=p[8*i]-p[8*j],b=p[8*i+1]-p[8*j+1],c=p[8*i+2]-p[8*j+2],d=p[8*i+3]-p[8*j+3];
  I A=p[8*i+4]-p[8*j+4],B=p[8*i+5]-p[8*j+5],C=p[8*i+6]-p[8*j+6],D=p[8*i+7]-p[8*j+7];
  if(a*A+33*b*B+3*c*C+11*d*D)continue;
  if(a*B+b*A+c*D+d*C)continue;
  I n0=a*a+33*b*b+3*c*c+11*d*d,n1=2*(a*b+c*d);
  I N0=A*A+33*B*B+3*C*C+11*D*D,N1=2*(A*B+C*D);
  if(sd*n1+s0*N1+s1*N0)continue;
  if(sd*n0+s0*N0+33*s1*N1!=I(sd)*den*den)continue;
  edges[2*e]=i;edges[2*e+1]=j;e++;
 }
 return e;
}
// Separate real-coordinate metric: x in F(sqrt(s)), y=sqrt(3)*Y.
// Scale both coordinates by 3 to keep all numerators integral.
static void real_square(const I* z,I sd,I s0,I s1,I* q){
 q[0]=sd*(z[0]*z[0]+33*z[1]*z[1])+s0*(z[2]*z[2]+33*z[3]*z[3])+66*s1*z[2]*z[3];
 q[1]=sd*2*z[0]*z[1]+s0*2*z[2]*z[3]+s1*(z[2]*z[2]+33*z[3]*z[3]);
 q[2]=sd*2*(z[0]*z[2]+33*z[1]*z[3]);
 q[3]=sd*2*(z[0]*z[3]+z[1]*z[2]);
}
extern "C" int real_contacts(int n,L den,L sd,L s0,L s1,const L* p,int* edges){
 if(n<1||n>20000||den<1||den>1000000000||sd<1||sd>1000000000||s0 < -1000000000||s0>1000000000||s1 < -1000000000||s1>1000000000)return -1;
 for(int j=0;j<8*n;j++)if(p[j] < -1000000000||p[j]>1000000000)return -2;
 int e=0;
 for(int i=0;i<n;i++)for(int j=i+1;j<n;j++){
  I d[8];for(int k=0;k<8;k++)d[k]=I(p[8*i+k])-p[8*j+k];
  I x[4]={3*d[0],3*d[1],3*d[4],3*d[5]},y[4]={3*d[2],d[3],3*d[6],d[7]},qx[4],qy[4];
  real_square(x,sd,s0,s1,qx);real_square(y,sd,s0,s1,qy);
  if(qx[0]+3*qy[0]!=9*I(sd)*den*den)continue;
  if(qx[1]+3*qy[1]||qx[2]+3*qy[2]||qx[3]+3*qy[3])continue;
  edges[2*e]=i;edges[2*e+1]=j;e++;
 }
 return e;
}
