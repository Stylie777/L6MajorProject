# L6MajorProject

This repository locates all technical work related to my L6 Major Project for my Digital Technology Solutions Apprenticeship. 

## Kanban Board

The Kanban board for the project can be seen on Trello [here](kanban-baord).

## The Tool

This tool is designed a Proof of Concept for a testing suite to validate LLVM's IR tests. The tool will clone the latest version of the [llvm-project](llvm-project) and compare the content's of LLVM's tests to the expected results.

As this is a Proof of Concept, there is currently limitations to the tools capabilities:
- The tool currently only support the VHCADD Instruction (Section C.2.4.356 of the [Arm Cortex-M Reference Manual](ARM-Cortex-M-ARM))
- Only the earlyclobber contraints are checked, realted to register allocation

## Using the Tool
### Installing Requirments

There are extra Python modules that are required to run the tool, these are listed in `src/requirements.txt`. To install them using Python's `pip` module, run the following command in your terminal (Note: these commands are for Bash on MacOS and Linux):
```sh
pip install src/requirements.txt
```

### Running the tool

From the top level directory of the reporitory, run the following command:
```sh
python3 src/main.py
```

This will run the tool and handle everything for the user, the results for each instruction will be outputted to your terminal, reflecting the following:
- For instructions that are valid
```sh
<instruction> is a valid Arm Assembley Instruction
```
- For instructions that are not valid
```sh
<instruction> is not a valid Arm Assembley instruction
```
`<instruction>` will be replaced by the instruction that is being validated.

## Running the Tests

Each of the module files within the `src/` diretory has a related test file as part of this project. Currently the following python files have tests written:
- `validate_instruction.py`

To run the tests, use the following command line:
```sh
python3 src/test_{Python File Name}.py
```
`{Python File Name}` should be replaced by one of the supported files that are listed above. For example, to test `validate_instruction.py` the command line would be: 
```sh
python3 src/test_validate_instruction.py
```

## Version History

### v0.1 - Inital Release
- Support for checking the earlyclobber contraint for the VHCADD instruction

<!-- Hyperlinks -->
[kanban-board]:https://trello.com/invite/b/673475fd26c9e89a0131ecd5/ATTI6e3c1073f393a4ab48e90d6a4f9179025704A135/l6majorproject
[llvm-project]:https://github.com/llvm/llvm-project
[ARM-Cortex-M-ARM]:https://developer.arm.com/documentation/ddi0553/by/?lang=en