# smarTaxi 🚕

In today's world owning a personal car or calling a taxi cab just for one person can be very inefficient and time consuming. 
We believe that the possibility of sharing a cab with other people can have a positive effect on the environment as well as 
on your pocket. The goal of this project was to explore several algorithms which could help in creating an 
application for shared taxi rides and to compare their performance with each other.

To run progam You have to execute `Environment.ipynb` (correct plots rendering available [here](https://nbviewer.org/github/valart/smarTaxi/blob/main/Environment.ipynb)), which runs whole *virtual* environment. Before the start of 
simulation 10 taxi cabs and 2 persons are generated at random locations in the area.

Also, in the project exists Policy class (`policy.py`), which is an abstract class. It is responsible for selecting clients in a certain period of time. The 
program has the ability to extend this class by changing the behavior of the algorithm. The list of heuristic functions (policies) tested during the project:

1. Dummy — assigning random people
2. Queue — first appears - first assigned
3. Nearest Neighbour — picking up and dropping off people with closest locations
4. Discounted Nearest Neighbour — the longer the client waits in line, the more priority he/she has
5. Nearest Neighbour with riding distances — the human who is the nearest and whose destination is the nearest, is most important
6. Discounted Nearest Neighbour with riding distances — same as nearest Neighbour with riding distances, but also taking into account waiting time as in Discounted Nearest Neighbour
7. Weighted Nearest Neighbour with riding distances — same as nearest Neighbour with riding distances, but all distances are weighted with reciprocal exponential function that uses destination as variable 

Finally, after execution, You can see boxplots, which are representing different algorithms.

There is also possibility to see visualization in `.gif` format, if You execute code which is located in `ivan-dev` branch.
