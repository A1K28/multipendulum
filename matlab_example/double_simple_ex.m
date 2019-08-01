clc
clear

syms g;
syms m1 m2;
syms l1 l2;
   
syms fi1 dfi1 ddfi1;
syms fi2 dfi2 ddfi2;

x1 = sin(fi1)*l1;
y1 = -cos(fi1)*l1;
x2 = x1+sin(fi2)*l2;
y2 = y1-cos(fi2)*l2;
 
x1_p = diff(x1, fi1)*dfi1;
y1_p = diff(y1, fi1)*dfi1;
x2_p = diff(x2, fi2)*dfi2 + x1_p;
y2_p = diff(y2, fi2)*dfi2 + y1_p;


V=g*(m1*y1+m2*y2);
T=0.5*(m1*(x1_p^2+y1_p^2)+m2*(x2_p^2+y2_p^2));
L=T-V;


Equations=Lagrange(L,[fi1,dfi1,ddfi1,fi2,dfi2,ddfi2]);
eq1=Equations(1);
eq2=Equations(2);

solf=solve(eq1,eq2,ddfi1,ddfi2);
addfi1=ccode(simplify(solf.ddfi1))
addfi2=ccode(simplify(solf.ddfi2))

fid = fopen('example.json', 'a+');
fprintf(fid, '%s%s', addfi1,addfi2);
fclose(fid);