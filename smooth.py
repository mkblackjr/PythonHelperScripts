# smooth.py

def smooth(x,N,**kwargs):
	smooth_x = []

	# # Error checking for the inputs

	# N not a positive integer, return error message
	if(type(N) is not int) | (N <= 0):
		raise ValueError("N must be a positive integer.\n")
	
	center_weight = kwargs.get('center_weight',1/(N*(N!=1)-1))
	
	# Set parameters for NO smoothing
	if (N == 1):
		center_weight = 1
		n_range = 1
		h = 0
		av = [1]


	elif (center_weight <= 0) | (center_weight > 1) | + \
		(type(center_weight) is not float):
		raise ValueError("center_weight must be a positive value between " + \
			"0 and 1.\nYou may need to adjust N to account " + \
			"for this error.\n")
	
	# Case where no errors have arisen
	else:
		N = N*(N<=len(x))+len(x)*(N>len(x))
		n_range = int((N/2))+1
		h = int((N)/2)
		b1 = center_weight
		dividend = 0

		# Calculate the weighting values based on the high weight value
		# - calculation worked out using discrete summation
		for i in range(h):
			dividend += (i+1)
		if (N%2==1):
			b2 = (1/2 - (h + 1/2)*b1)*h/dividend + b1
		else:
			b2 = (1/2 - h*b1)*h/(dividend-1/2*h) + b1

		av = [b2+(b1-b2)/h*(n_range-(m+1)) for m in range(n_range)]
		if av[-1] <= 0:
			raise ValueError("Lowest weighting value is " + str(av[-1]) + \
			 ".\nPlease reduce the center_weight value.\n")

	# Perform the smoothing algorithm
	for i in range(len(x)):
		y = 0

		# Inner loop iterates over surrounding data points, performs smoothing
		for j in range(N):
			index = i-h+j

			# Odd mesh - data spaced at regular intervals
			if(N%2 == 1):
				if index >= len(x):
					additive = x[len(x)-1-j]*av[abs(j-h)]
				elif(index < 0):
					additive = x[i+h+abs(i-h+j)]*av[abs(j-h)]
				else:
					additive = x[index]*av[abs(j-h)]
			
			# Even mesh - data requires interpolation			
			else:
				if index+1 >= len(x):
					additive = 1/2*(x[len(x)-j]*av[abs(j-h)]+
						x[len(x)-j+1]*av[abs(j-h)+1])
				elif(index < 0):
					additive = 1/2*(x[i-1+h+abs(i-h+j)]*av[abs(j-h)]+
						x[i+h+abs(i-h+j)]*av[abs(j-h)-1])
				else:
					if (j >= h):
						additive = 1/2*(x[index]*av[abs(j-h)]+
							x[index+1]*av[abs(j-h)+1])
					else:
						additive = 1/2*(x[index]*av[abs(j-h)]+
							x[index+1]*av[abs(j-h)-1])						
			
			# Accumulate the weighted values from each surrounding data point
			y += additive

		# Add smoothed data point to the array - will be same size as original
		smooth_x.append(y)

	return smooth_x