# Allocate

![DAG of compatible appointments from 8:00 - 12:00](https://i.imgur.com/ZoeS66h.png)
###### This is a graph visualization of appointment IDs mapped to subsequent compatible appointments IDs using one of the tree mapping functions (`update_valid_choices`).


My intent when creating this project was to prototype a simple, lightweight scheduling optimization tool. This is my first open source project. Feedback is very much appreciated!

You'll like this project if you schedule a workforce with fixed shift start and end times and want to allocate your available staffing resources to achieve a higher overall impact. You'll also like the project if, like me, you enjoy experimenting with changes to how you would normally schedule staff.

#### Big 3 Project Goals
##### #1 - Flexibility
As someone who manages staff allocation for a living, I understand that no two scheduling operations are identical. In this project, the primary goal is to give you the freedom to tailor it to your specific needs. I have created the basic building blocks of a scheduling operation that meets my needs and I know that someone else will eventually find ways to improve upon it based on their own unique needs.

##### #2 - Convenience
Many of the abstractions you would expect for as simple and straightforward of a staff scheduling operation as mine are defined in the project, so you don't need to bother creating them: patients, interpreters, appointments, schedules. 

##### #3 - Experimentation
The project simplifies the tasks associated with experimenting with and exploring the impact of scheduling variable changes and decisions without having to impact the real world. By experimenting in this way, is then possible to dive deeper into your scheduling operation and come out with valuable observations, which you could then implement in the workplace to better allocate your resources. 

## Project Structure

A. Code
```
[modules]
```

B. Data
```
[config]
A csv format file of schedule data to read and modify that conforms to the header structure in CSVData.py
```

C. Tests
```
Unit test files
...
```

## Design & Formatting Decisions

#### Style
Code is formatted according to PEP8 style guidelines with the help of Pycharm IDE. I opted for a code documentation docstring format able to autogenerate reStructuredText documentation.

#### Organization
I wanted the config file to contain all of the user-defined information (staff names, shift times, assignment weights, staff per shift...) to keep the real world customizations seperate from the business model.  

#### Future Plans
The static python config file could be replaced, augmented or simply modified by a or via a command line interface, or even a GUI (I've toyed with the idea of trying out electron but haven't had the time).

#### File Structure
* Base classes and subclasses are grouped together whenever possible

Main Business Logic:
```
location
--------
  + Point
  + Grid
  + Location
person
------
  + Person
  + Patient
  + Interpreter
schedule
--------
  + Appointment
  + Schedule
schedulers
----------
  + BruteForce
  + Greedy
  + MonteCarlo
  + WeightedInterval
  + Optimum
constants
---------
  + TIME_FORMAT
  + MAX_INT   
utils
-----
  + timer
  + typdef
  + enumerate_combinations
  + sum_lists_product
  + Time
```

Reports:
```
ConsoleReport
```

Configuration:
```
csvconfig
csvprocessor
```

## Scheduling Class Objects

### BruteForce
Using the `BruteForce` class, you can compute the power set of all possible assignments for one interpreter using the `gen_all_paths` method. It continues doing so for each interpreter in the `BruteForce.interpreters` list until there are either no more appointments or interpreters.

Brute force has its uses, even though it fails spectacularly after a given number of nodes (~80 at the time of writing this). This is because it tells you exactly how many schedule iterations need to be computed in order to determine which is the most highly weighted schedule possible, and can be used to verify the accuracy of alternative scheduling heuristics.

### Greedy
Greedy algorithms that use either count or the total impact sum as the characteristic to locally optimize seem to rapidly generate viable solutions with only a marginal effectiveness loss using the model data. It can be fun to explore if this can work for you.

### MonteCarlo 
An alternative approach that involves randomized schedule creation. The schedules are randomly generated until to a given number of trials stored in the `Optimum` class has been reached. The `Optimum.max_repeated_result` property caps the number of times that the highest recorded trial impact has repeatedly remained the highest impact score of any randomly generated interpreter schedule assignment. This prevents lots of needless waiting if you think it has reached it's likely maximum.

Since tests performed on simulated schedule data have returned tree path counts in the tens of millions, almost reaching 100M, it seems unlikely that this method would return the optimal schedule anytime soon, however it did approach both the brute force and greedy heuristics' effectiveness, displaying only a marginal impact loss after only 100 or so trials at the time of writing. Again, your mileage may vary.

### Weighted Interval Scheduling Algorithm
The time complexity of the `BruteForce` class motivated me to develop a faster solution. The weighted interval scheduling algorithm has proven a partial solution to some of the problems with `BruteForce`. It can compute a solution in `O(nlogn)`, so is not as constrained by tree node size, or by the number of edges on each node. The key is that it uses memoization by computing the highest-weighted path choices before applying them to the data. The use of memoization renders it unable to work with 2d coordinates and their impact to commute times, which has presented a challenge when working with data that is not already sorted and constrained by physical location.   

##### Complexity Constraints  
The computational time complexity of the `BruteForce` class method `gen_all_paths` seems to grow exponentially at somewhere near O(x^e). A moderately small number of nodes for `BruteForce` doesn't seem to take very long, but your mileage may vary by hardware. Going higher than that recommended number of nodes might require a lot more time to run than would seem reasonable in a work environment, thus why the research into using dynamic programming will be necessary for mainstream use.

## Getting Started

### Prerequisites

#### Files
To get up and running, you will need all project files. It is recommend to use the latest release.

#### Python Version
Python 3.6 or higher is required to run the code.

#### Dependencies
All library dependencies are default Python libraries or files from this project.

From the Python standard library:
```
random
datetime
collections
copy
sys
timeit
functools
operator
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


## Acknowledgments

Many thanks to MIT OCW for the helpful, free online data science and programming videos that inspired this project:
* MIT 6.0002 Introduction to Computational Thinking and Data Science (Fall 2016) - [available here](https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-0002-introduction-to-computational-thinking-and-data-science-fall-2016/)
* MIT 6.046J Design and Analysis of Algorithms (Spring 2015) - [available here](https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-046j-design-and-analysis-of-algorithms-spring-2015/)
* The many online "textbook" implementations of the weighted interval scheduling algorithm, both iterative as well as recursive, that served as the inspiration behind the WeightedInterval class
