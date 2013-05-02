% cd C:\ani\code-sand-box
% c:\Octave\3.2.4_gcc-4.4.0\bin\octave.exe costfunc.m

addpath('C:\ani\code-sand-box')

x=1:100
y=x.*2
z=x\y

save reg.txt z -ascii 

plot(z)


[W,s,v] = svd((repmat(sum(x.*x,1),size(x,1),1).*x)*x'); 

% https://d396qusza40orc.cloudfront.net/ml/docs%2Fslides%2FLecture1.pdf
% https://class.coursera.org/ml-003/lecture/index
% https://class.coursera.org/ml-003/wiki/view?page=CourseFAQ
% https://share.coursera.org/wiki/index.php/ML:Main
% http://calypso.inesc-id.pt/docs/OctTutV1b.pdf
% http://spark-public.s3.amazonaws.com/ml/exercises/ex1_003.zip
% https://class.coursera.org/ml-003/assignment/view?assignment_id=2