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
