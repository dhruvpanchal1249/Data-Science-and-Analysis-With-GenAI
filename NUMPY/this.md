# ***NUMPY commands and definition***
myarray=np.array([[2,22,45,65,1]])
myarray[0, 1]   
this command is to view the element of 2nd row and 1nd column and to create a array of 2*2 matrix

myarray.shape -> this command is to view the shape of the array

myarray.dtype -> this command is to view the data type of the array 

myarray[0,1]=45 
myarray -> this command is used to change the element valua the index passsed in the [] here 22 is changed with 45 

listarray.dtype --> used to find the data type of the array 

listarray.size --> used to find the size of the array

listarray.shape --> used to find the dimensions of the array 

zeros=np.zeros((3,6))
zeros -> this command is used to create a array of size 3*6 with all the values as 0

rng= np.arange(0,10)
rng -> this command is used to create a array of size 10 with values from 0 to 9 

lspace=np.linspace(1,4,4)
lspace -> this command is used to create a array of size 4 with values from 1 to 4 in which the values are lineally equally spaced 

emp=np.empty((4,6))
emp ->this command is used to create a array of size 4*6 with random values 

arr=np.arange(99)
arr
arr.reshape(3,33) ->this command is used to reshape the array into 3*33 matrix from a 1*99 matrix


x=[[1,2,3],[77,78,79],[41,42,43]]
arr=np.array(x)
arr
arr.sum(axis=0) -> this command is used to find the sum of the array along the columns
arr.sum(axis=1) -> this command is used to find the sum of the array along the rows
arr.argmax(axis=0) -> this command is used to find the index of the largest value in the array
arr.argmax(axis=1) -> this command is used to find the index of the largest value in the array
arr.argmin(axis=0) -> this command is used to find the index of the smallest value in the array
arr.argmin(axis=1) -> this command is used to find the index of the smallest value in the array

arr.T -> this command is used to transpose the array/matrix

arr.ndim -> this command is used to find the number of dimensions of the array

one=np.array([1,5,22,365,45,23])
one.argmax() -> this command is used to find the index of the largest value in the array
one.argmin() -> this command is used to find the index of the smallest value in the array

arr1 + arr2 -> this command is used to add the two arrays
arr1 - arr2 -> this command is used to subtract the two arrays
arr1 * arr2 -> this command is used to multiply the two arrays
arr1 / arr2 -> this command is used to divide the two arrays
arr1 ** 2 -> this command is used to square the elements of the array
arr1 ** 3 -> this command is used to cube the elements of the array

arr1.sum() -> this command is used to find the sum of the array
arr1.min() -> this command is used to find the minimum value in the array
arr1.max() -> this command is used to find the maximum value in the array
arr1.mean() -> this command is used to find the mean of the array
arr1.std() -> this command is used to find the standard deviation of the array
arr1.var() -> this command is used to find the variance of the array
