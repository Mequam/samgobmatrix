# Python Project 1 - Matrix Operations

the following repository is my python project 1 for skillstorm and
an upgrade to the samgob dice language

what follows is a quick description for running the code, and a rough explanation of
the arcitecture for those curious to poke around and do some analysis

---

## Quick Start

quick start scripts for windows and linux for running the code can be found at

[https://github.com/Mequam/samgobMatrixQucikStart.git](https://github.com/Mequam/samgobMatrixQucikStart.git)

simply clone the above repo and run the setup script for you respective platform


---

## Download and Enviornment Setup

the following commands can setup the program from a git and python install

#### Linux

```bash
git clone https://github.com/Mequam/samgobmatrix.git
cd samgobmatrix
git submodule update --init --recursive
python -m venv .venv
source .venv/bin/activate
python -m pip install -r ./requirements.txt
```

#### Windows

```powershell
git clone https://github.com/Mequam/samgobmatrix.git
cd samgobmatrix
git submodule update --init --recursive
python -m venv .venv
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted
./.venv\\Scripts\\activate
python -m pip install -r ./requirements.txt
```

---

## Running the Program

fist make sure you are using an environment where the requirements for
the program are installed, this should have been set up in the above
setup commands, to use the environment you can use the following commands

#### Linux
```bash
source .venv/bin/activate
```

#### Windows
```powershell
./.venv/Scripts/activate
```

make sure in a windows envioronment that your system is configured to run scripts,
if you get an error complaining about script excecution configuration, double check
the excecution policy for your powershell, as a quick fix you can run

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted
```

which will let the current user run anything, including the activate script,
there is probably a better way around that problem, but I am nowhere near a powershell
expert and thats what worked for me :)


#### Start Command

once in the enviornment you can run the program with the following command

```bash
python main.py
```

---

## Unit Tests

the matrix component of the program is packaged with several unit tests to verify the integrity
of the code, you can run these unit tests with the following command in the root directory of the code base
to ensure everything is operational

```bash
python -m unittest -v
```

---

## Using The Program

once started you will be placed into a shell where you can run several commands

unrecognized commands will be treated as queries of the samgob language, and the program
will try and parse them out

at all times you can get a list of valid commands using the help command, these commands can
be further quried with help to get a list of subcommands that can be run in the system

a help sequence could look like the following

```
()> help
valid commands are 
 'samgob'
 'plot'
 'memory'
 'exit'
()> help plot
valid commands are 
 'heatmap'
()> help plot heatmap
usage: heatmap [-h]

options:
  -h, --help  show this help message and exit
()> command or query
```

commands will often have a default command that is run automatically for you
if you do not specify which command you are running, the samgob command for 
example is run as the default command for the entier system to perform parsing,
so if you don't want to specify samgob <arguments> you could just plop down <arguments>
and the program will happilly parse them out

## Built In Commands

the program comes with 4 default commands

1. samgob (default)
2. plot
3. memory
4. exit


---

## Samgob (Samon Goblin) Language

the samgob language is a turing complete dice rolling language designed to be run in a 
terminal enviornment for those who like rolling lots of dice and rng, the particular
variaty of samgob installed in this program has been edited to include matrix support!

the spec for the language can be viewed in dice\_set.lang and is a good starting point for
all of the different things that can be performed with it

### Arithmatic

samgob has 3 primary arithmatic constructs,

numbers,
matricies
sets

each of these can be controled and filtered in order to generate dice rolls

#### numbers

starting with numbers, you can perform basic arithmatic operations

```
1+1
2+5
3*7/8
[1+1]*2
1+1*2
3.1415*2
```

#### sets

sets are collections of numbers that can be created using set operators
and condenced down to numbers using a set compressor operators.

this is easier with an example

```
3D6
```

above D is a set operator that takes in a set (when numbers are treated as sets they are sets ranging from 1 to
the given number, in this case [1,2,3,4,5,6]) and randomly selects n elements from that set, n in this case bieng
3

so a possible return value from this set operator would be [2,4,6]

there are two other set operators currently supported in the language, T for top and B for bottom

these operators take the n top or bottom numbers from a given input set, so for example if I wanted
to roll 2 20 sided dice and take the higher number I could do so using the following operation

```
1T2D20
```

if I instead wanted to take the top 3 rolls of a set of 4 6 sided dice I could do so with the
following query

```
3T4D6
```

sets can then be compressed down into single numbers using set compressors, of which there are currently two,
the unary set compressor s and the standard set compresor d

d takes n values randomly from a set, sums them, and returns the result

so
```
3d6
```

will generate the set 1,2,3,4,5,6 then randomly select 3 values from it, sum them together and return the result

the s unary set operator takes a single set on the right and returns the sum of that set

```
s3D6
```

would be an equvilent way of performing the above 3d6 query

finally sets can be generated with the range syntax

{5-8}

will generate the set

5,6,7,8


#### Matricies

this version of samgob contains matrix support!

matricies are represented using a ,: notation where every :
indicates a new row in the matrix.

using this format the identity matrix could be represented as follows


```
1,0:0,1
```
equates to

1 0
0 1

as another example the rotation matrix by 90 degrees could be represented as

```
0,-1:1,0
```

0 -1
1  0

the numbers stored inside of the matricies are themselfs fully parsable samgob arithmatic,
so you can throw dice queries to your hearts content inside of the matricies to generate
random matricies on the cli

```
1d10,2d20,3d10:s3T5D6,3d6,4d6
```

under the hood these matricies are using the matrix classs found in DAKMatrix,
the ~ operator exposes underlying python functions of a matrix so you can compute
inverses determinents and transposes

```
x=1,2:3,4
x~transpose
x~inv
x~det
```

will compute the transpose inverse and determinent of the matrix x

matricies can be added subtracted and multiplied! the langauge can get a bit unhappy with
order of operations though, so it can be helpful to place the matricies in parenthasese while performing this operation :)

```
x=[1,2:3,4]+[5,6:7,8]
x*[1,2:3,4]
x*x~transpose
x*x~det
x*2
```


#### Variables

samgob fully supports variables! simply place any arithmatic to the right of an equal sign and
the program will remember that value for the future

```
x=3d6,2d6:4d6,5d6
x=2*x
```

### Control Flow

samgob contains fully funcitoning for loops, if statements, while loops and else clauses
since samgob is designed for concise terminal syntax the loop syntax is a little different from
other langauges

One major differnece is what I like to call "infinit scoping", once a loop is opened in samgob
EVERY following statement is concidered in that loop, closing the loop is optional! This allows
for the language to be very concice in a cli enviornment and your queries to take less space!

every loop structure in samgob begins with a : followed by some kind of indicator for the amount
the loop needs to run and can optionally end in an S, the S is a seperator indicator and is used for formating
the output for that loop, all output in that loop is deliminated with the value to the right of the S, leave that
value blank to indicate a new line deliminator

all samgob loops can be closed with a ::


#### For Loops

for loops in samgob start with a : and are followed by any arithmatic evaluating to a number

```
:6 3d6
```

will roll 6 3 sided dice

```
:100S :6 3d6
```

will generate 100 of those rolls, and seperate each of the inner command
with a newline character

```
:100S :6 3d6 :: :1S 1d20
```
this satement loops 3d6 6 times, then performs that 100 times, and rolls a 20 sided dice
after rolling the 6 3d6 dice, basically the :: is closing the :6, not the :100S

the :1S is added to append a newline and make the output easier to read :D

```
:100S :2S, :4 1d{0-1}
```

this will generate 2 columns of 4 binary bits 100 times

#### If Statments

samgob uses for loops for if statement evaluation, a for loop who evaluates to 0 initially
is concidered a false if statement

the ==, >, < operators all evaluate to 0 or 1, and that value can be fed into a for loop

```
:1d20>10 x=1
```
will set x to 1 only if 1d20 is bigger than 10

you can use an else clause to detect if the loop did not run

```
:1d20>10 x=1 :e x=0
```

use an outer loop to repeat and display the results more easily

```
:10 :1d20>10 x=1 x :e x=0 x
```

note the use of the blank variable for displaying its value

#### While Loops

you can use :w in order to repeat while a statment is true

```
:w1d20>2 1 :: 0
```

will run while 1d20 > 10 and print 0 when done

---

## CLI Commands

### samgob

this command parses out the samgob programing language, it takes a samgob query
and returns the result as text on the screen

### Plot Command

this command is for displaying matricies in matplot lib, it takes a **sambob query** stores the resulting value in a variable
named tmp, and then displays the matrix on the screen using a heatmap

since the command takes a full samgob query, feel free to play around with the results

```
plot 1d20,1d20,1d20:1d20,1d20,1d20:1d20,1d20,1d20
```

plots a random 3d matrix to get you started

### Memory Command

this command is for interacting with and saving variables to the disk

```bash
memory save <variablename>
```

you can additionally change the name

will save a variable that is currently in samgob to the system

```bash
memory load [--varname [VARNAME]]
```

will load a variable into memory if specified, if not specified will load
EVERY variable into memory

```bash
memory show
```

will show all queries stored in the memory file since loading actually runs the query in samgob,
you could write queries that reload with random dice

all memory commands include an optional --filepath flag that can be edited to change the file used to store the
program variable memory


---

## Arcitecture Overview

there are three primary custom modules in the program

the command module, which contains a simple command class that can be chained
together in the form of a command tree. This command class further contains several
very useful utilities to convert arbitrary python functions into commands

the matrix module, which contains a simple matrix class for matrix operations
that really is just a wrapper around numpy

and the samgob module, which contains the language parsing logic

samgob itself is parsed using the goblang toolkit which is a custom framework
for parsing arbitrary langauges, the file used for this is dice\_set.lang
and can be located in the samgob folder. I am fairly certain that this parsing is
responsible for most of the startup lag in the program, a future update could see
storing the "parse mesh" so that it doesn't need to be re computed each time the program
starts up

each command set can be located in the subcommands folder, and uses the command module
in order to create itself. These commands are then chained together in main.py, with a
single unified reference to a dice parser from samgob, so everything is talking to
the same samgob implementation and variable set.
