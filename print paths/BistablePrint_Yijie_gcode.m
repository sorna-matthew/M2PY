clc; clear; close all;
L=10.5;
a=45;
h1=2.5;
h2=sind(a)*L*0.65;
h3=h2*1;
w2=3;
dis=6;
z_offset = -144.3;


% DNozzle=0.2;
Layer=2*15;
SlowLayer=7;

w=2*w2+2*cosd(a)*L;
filename=['Bistable',num2str(h1),'_',num2str(h2),'_',num2str(w2),'_',num2str(L),'_',num2str(a),'_gcode_TEST.txt'];
fid=fopen(filename,'w');

fprintf(fid,'G28 Z\n');
fprintf(fid,'G91 \n');
fprintf(fid,'G1 Z%6.3f\n',z_offset);

C_R1=[0,h1+dis
    w/2-h2/tand(a),0
    w/2+h2/tand(a),h2+L*sind(a)+w2*tand(a)
    0,h1+h3-tand(a)*w2
    -w,0
    0,-(h1+h3-tand(a)*w2)
    w/2+h2/tand(a),-(h2+L*sind(a)+w2*tand(a))
    w/2-h2/tand(a),0
    0,-h1
    -w-dis,0
    0,h1+h2+L*sind(a)+w2*tand(a)
    dis,0
    0,-w2*tand(a)
    w2,0
    0,h3
    2*(L*cosd(a)),0
    0,-h3
    w2,0
    0,w2*tand(a)];
C_R1(:,3)=1;
C_R1(3,3)=2;
C_R1(7,3)=2;
C_R2=-C_R1(end:-1:1,:);

C_A(1,:)=[0,0,1];
for i=2:length(C_R1)+1
    C_A(i,:)=C_A(i-1,:)+C_R1(i-1,:);
end
plot(C_A(:,1),C_A(:,2))
axis equal

ms = 40*60;
fms = 100*60;
SlowLayer = 0.9*60;
dz = 0.4*0.68;


for Li=1:2:Layer
    for i=1:length(C_R1)
        if i>1 & C_R1(i,3)~=C_R1(i-1,3)
            if C_R1(i,3)==2
                if mod(Li,SlowLayer)==0
                    ms = 40*0.9*60;
                    %fprintf(fid,'ms,&msBeam*&SlowLayer\n');
                else
                    ms = 40*60; 
                    %fprintf(fid,'ms,&msBeam\n');
                end
            else
                ms = 40*60;
                %fprintf(fid,'ms,&ms\n');
            end
        end
        fprintf(fid,'G1 F%6.3f X%6.3f Y%6.3f\n',ms,C_R1(i,1),C_R1(i,2));
    end
    fprintf(fid,'G1 Z%6.3f\n', dz);
    for i=1:length(C_R2)
        if i>1 & C_R2(i,3)~=C_R2(i-1,3)
            if C_R2(i,3)==-2
                if mod(Li+1,SlowLayer)==0
                    ms = 40*60*0.9;
                    %fprintf(fid,'ms,&msBeam*&SlowLayer\n');
                else
                    ms = 40*60;
                    %fprintf(fid,'ms,&msBeam\n');
                end
            else
                ms = 40*60;
                %fprintf(fid,'ms,&ms\n');
            end
        end
        fprintf(fid,'G1 F%6.3f X%6.3f Y%6.3f\n',ms,C_R2(i,1),C_R2(i,2));
    end
    fprintf(fid,'G1 Z%6.3f\n', dz);
end
%fprintf(fid,'END\n');
fclose(fid);




