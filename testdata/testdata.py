#testing if libraries are working
from pylab import imshow,gray,jet,show
from numpy import loadtxt

#imshow library with density plot
data = loadtxt("circular.txt",float)
imshow(data)
jet()
#gray()
show()



