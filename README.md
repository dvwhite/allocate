# Allocate

![DAG of compatible appointments from 8:00 - 12:00](https://i.imgur.com/ZoeS66h.png)
###### This is a graph visualization of appointment IDs mapped to subsequent compatible appointments IDs using one of the tree mapping functions (`update_valid_choices`).

My intent when creating this project was to prototype a simple, lightweight interpreter scheduling optimization tool. The project originated when I worked as a hospital staff member charged with creating foreign language interpreter schedules. As I created the schedules every day for next business day, I found that I always had far more requests to be staffed than available staff to allocate to the requests, so creating a schedule always required a lot of thinking, iteration, and deep domain knowledge. I probably spent at least 1-2 hours of work per day on scheduling simply due to the sheer complexity of doing so by hand. 

While working at the medical center, I began studying computer science part time on the weekends. While taking these CS classes, I realized that I could put my knowledge of Python and scheduling algorithms to devise a system to automate manual interpreter scheduling. I sat down every weekend over the course of about a year or so, and wrote as much of this as I could. I made many mistakes, and learned from them as I went. This is my first open source project. Feedback is very much appreciated!

You'll like this project if you schedule a workforce with fixed shift start and end times and want to optimally allocate your available staffing resources to achieve a higher overall impact. You'll also like the project if you enjoy experimenting with changes to how you would normally schedule staff.

#### Project Goals
##### #1 - Adaptation
In this project, the primary goal is to give you the freedom to adapt the project to your specific needs. I have created the basic building blocks of a scheduling operation that meets my needs so that you can use as is, or find ways to improve upon it based on your unique needs.

##### #2 - Abstraction
Many of the abstractions you would expect for interpreter scheduling are defined in the project, so you don't need to bother creating them: patients, interpreters, appointments, schedules. The utils included in the project are also useful. For example, the Time class is a handy lightweight `datetime` wrapper that handles the time arithmetic.

##### #3 - Creativity
The project allows you to be creative and experiment with changes to how you would normally schedule staff without having to impact the real world. By using the scheduling heuristic simulations provided in this project, is then possible to dive deeper into your scheduling operation and surface later with valuable observations, which you could then implement in the workplace to better allocate your resources in the real world if you so choose. 

## Project Structure

A. Code
```
The modules that contain the project's logic, abstractions and configurations
```

B. Data
```
A csv format file of schedule data to read and modify that conforms to the header structure in CSVData.py
```

C. Tests
```
Unit test files
```

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

Data:
```
DemoData.csv
```

## Design & Formatting Decisions

#### Style
Code is formatted according to PEP8 style guidelines with the help of Pycharm IDE. I opted for a code documentation docstring format able to autogenerate reStructuredText documentation.

#### Organization
I wanted the config file to contain all of the user-defined information (staff names, shift times, assignment weights, staff per shift...) to keep the real world customizations seperate from the business model.  

#### File Structure
* Base classes and subclasses are grouped together whenever possible

## Scheduling Class Objects

### BruteForce
Using the `BruteForce` class, you can compute the power set of all possible assignments for one interpreter using the `gen_all_paths` method. It continues doing so for each interpreter in the `BruteForce.interpreters` list until there are either no more appointments or interpreters.

The computational time complexity of the `BruteForce` class method `gen_all_paths` seems to grow exponentially at somewhere near O(x^e). A moderately small number of nodes for `BruteForce` doesn't seem to take very long, but your mileage may vary. It is useful as a way to verify and benchmark other solutions.

### Greedy
Greedy algorithms that use either count or the total impact sum as the characteristic to locally optimize seem to rapidly generate viable solutions with only a marginal effectiveness loss using the model data. It can be fun to explore if this can work for you.

### MonteCarlo 
An alternative approach that involves randomized schedule creation. The schedules are randomly generated until to a given number of trials stored in the `Optimum` class has been reached. The `Optimum.max_repeated_result` property caps the number of times that the highest recorded trial impact has repeatedly remained the highest impact score of any randomly generated interpreter schedule assignment. This prevents lots of needless waiting if you think it has reached it's likely maximum.

Since tests performed on simulated schedule data have returned tree path counts in the tens of millions, almost reaching 100M, it seems unlikely that this method would return the optimal schedule anytime soon, however it did approach both the brute force and greedy heuristics' effectiveness, displaying only a marginal impact loss after only 100 or so trials at the time of writing. Again, your mileage may vary.

### Weighted Interval Scheduling Algorithm
The time complexity of the `BruteForce` class motivated me to develop a faster solution. The weighted interval scheduling algorithm has proven a partial solution to some of the problems with `BruteForce`. It can compute a solution in `O(nlogn)`, so is not as constrained by tree node size, or by the number of edges on each node. The key is that it uses memoization by computing the highest-weighted path choices before applying them to the data. The use of memoization renders it unable to work with 2d coordinates and their impact to commute times, which has presented a challenge when working with data that is not already sorted and constrained by physical location.   

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

### Overview, Data Flow and Demoing the Project
The project is simple to set up and use. A high level overview of the project
scripts is as follows:

1. You will need a csv file with data needing 
2. Adapt or use the predefined header labels in `csvconfig` to match the csv header structure
3. Open `csvconfig` and run it
4. A report will print to the interactive shell or IDE console that you can review to see which scheduling method(s) would produce an optimal scheduling result
5. As the report runs, it displays the schedules generated by the available scheduling functions one by one, from the most to least impactful. The schedule will print out for each report function individually and pauses until you hit the 'enter' key. This allows you to assign staff on your schedule if you so choose, or simply gain an understanding of the best method and how impactful it might be
6. Pressing 'enter' a final time will end the script

#### Data Flow and Program Execution
The file of csv data is parsed by the `csvconfig` and `csvprocessor` files. The `csvconfig` contains the business data such as the list of available staff, their assignments and shift start/end times. The `csvconfig` file builds a `Schedule` class object using the `csvprocessor` library. The `csvconfig` file then creates a `Optimum` class object using the `Schedule`, and runs a method called `compare_performance`, and loads it into the `ConsoleReport` class to display to the user by printing it to the console/shell. 

#### Setup and Run the Demo
1. Download the latest release
2. Run the 'csvconfig.py' script from within your text editor, shell or IDE
3. Review the comparison of scheduling methods to see the best method to
   schedule the available resources contained in 'csvconfig.py'
4. Experiment with making changes to 'csvconfig.py' and you'll see how it
   can impact the efficacy of a scheduling method. For instance, by altering
   a staff member's schedule, or by adding additional staff members, you
   will modify the resulting schedules generated by the `schedulers.py` script

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


## Acknowledgments

Many thanks to MIT OCW for the helpful, free online data science and programming videos that inspired this project:
* MIT 6.0002 Introduction to Computational Thinking and Data Science (Fall 2016) - [available here](https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-0002-introduction-to-computational-thinking-and-data-science-fall-2016/)
* MIT 6.046J Design and Analysis of Algorithms (Spring 2015) - [available here](https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-046j-design-and-analysis-of-algorithms-spring-2015/)
* The many online "textbook" implementations of the weighted interval scheduling algorithm, both iterative as well as recursive, that guided the project around a runtime roadblock
