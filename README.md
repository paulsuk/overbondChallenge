# overbondChallenge
Code for the overbond challenge

Running the code: 

	- The code must be run with Python 3.4 or later 
	
	- Run by using python bondAnalysis.py <input file name> <challenge number (1/2)>
	
	- Challenge number refers to the document found https://gist.github.com/kseyon/fdb3ede4fadc2559c74fcdbe32ccf613

Design: 

	- Object Oriented, and using Enum to identify bond type to allow for expanding the complexity of the problem. It also allows us to solve additional problems that are not explicitly stated in the specs.
	
		e.g we can calculate benchmarks or spread to curves of any type of bond (not just corporate bonds) compared to any sets of benchmarks (not just government bonds)
		
	- Avoiding using external libraries. No need for non-built in libraries which means code is more easily distributed
	
	- Restricting python version to 3.4 was a co ncious decision to be able to use the built in Enum class. This was a trade off of ease of distribution, and code functionality. In the end, I decided that downloading and install the most recent version of python3.6 is not a very difficult process 


Areas of improvement:

	- When looking for nearest neighbours, could use an implementation of binary search to reduce runtime complexity to O(log(n)) instead of current which is O(n). Did not implement for the sake of time
	
	- Write output to file (easy change)
	
	- Make parseInput more robust. Currently, the parsing method splits up the data into corporate and government bond types, which works in the context of this challenge, but added complexity in the data means rewrites are needed to the parser
	
	- Have an input arg that optionally runs tests
	
	- Make the interface more convenient by letting the user change the input file, and run the different challenges without having to rerun the script
