clc
clear

syms g;
syms m1 m2 m3;
syms l1 l2 l3;
   
syms fi1 dfi1 ddfi1;
syms fi2 dfi2 ddfi2;
syms fi3 dfi3 ddfi3;

x1 = sin(fi1)*l1*0.5;
y1 = -cos(fi1)*l1*0.5;
x2 = 2*x1+sin(fi2)*l2*0.5;
y2 = 2*y1-cos(fi2)*l2*0.5;
x3 = 2*x2+sin(fi3)*l3*0.5;
y3 = 2*y2-cos(fi3)*l3*0.5;

x1_p = diff(x1, fi1)*dfi1;
y1_p = diff(y1, fi1)*dfi1;
x2_p = diff(x2, fi2)*dfi2 + x1_p;
y2_p = diff(y2, fi2)*dfi2 + y1_p;
x3_p = diff(x3, fi3)*dfi3 + x2_p;
y3_p = diff(y3, fi3)*dfi3 + y2_p;

V=g*(m1*y1+m2*y2+m2*y2);
T=0.5*(m1*(x1_p^2+y1_p^2)+m2*(x2_p^2+y2_p^2)+m3*(x3_p^2+y3_p^2))+0.5*1/12*dfi1^2*m1*l1^2+0.5*1/12*dfi2^2*m2*l2^2+0.5*1/12*dfi3^2*m3*l3^2;
L=T-V;


Equations=Lagrange(L,[fi1,dfi1,ddfi1,fi2,dfi2,ddfi2,fi3,dfi3,ddfi3]);
eq1=Equations(1);
eq2=Equations(2);
eq3=Equations(3);

solf=solve(eq1,eq2,eq3,ddfi1,ddfi2,ddfi3);
addfi1=ccode(simplify(solf.ddfi1))
addfi2=ccode(simplify(solf.ddfi2))
addfi3=ccode(simplify(solf.ddfi3))

fid = fopen('example.json', 'a+');
fprintf(fid, '%s%s%s', addfi1,addfi2, addfi3);
fclose(fid);