# Simple Assembler and simulator
An assembler is made which converts assembly language to machine language.
And simulator runs the assembly program after assembler.

## Adding code
* Add the assembler code in the `Simple-Assembler` directory. Add the commands to execute the assembler in `Simple-Assembler/run`.
* Add the simulator code in the `SimpleSimulator` directory. Add the commands to execute the assembler in `SimpleSimulator/run`.
* Make sure that both the assembler and the simulator read from `stdin`.
* Make sure that both the assembler and the simulator write to `stdout`.

## //////////
* Go to the `automatedTesting` directory and execute the `run` file with appropiate options passed as arguments.
* Options available for automated testing:
	1. `--verbose`: Prints verbose output
	2. `--no-asm`: Does not evaluate the assembler
	3. `--no-sim`: Does not evaluate the simulator
