# L6MajorProject

This repository locates all technical work related to my L6 Major Project for my Digital Technology Solutions Apprenticeship. 

## The Tool

This tool is designed a Proof of Concept for a testing suite to validate LLVM's IR tests. The tool will clone the latest version of the [llvm-project](llvm-project) and compare the content's of LLVM's tests to the expected results.

As this is a Proof of Concept, there is currently limitations to the tools capabilities:
- The tool currently only support the following instructions from the [Arm Cortex-M Reference Manual](ARM-Cortex-M-ARM)

| Instruction | Section |
| :----------- | :-------: |
| VCADD | C2.4.312 |
| VCADD (Floating Point) | C2.4.313 |
| VCMUL (Floating Point) | C2.4.321 |
| VHCADD | C2.4.356 |
| VQDMUL | C2.4.440 |
| VREV64 | C2.4.453 |

- Only the following elements are verfified:
    - Earlyclobber contraints
    - Register Allocation is within the expected range
    - Rotate value is within the expected parameters if used

## Using the Tool
### Installing Requirments

There are extra Python modules that are required to run the tool, these are listed in `src/requirements.txt`. To install them using Python's `pip` module, run the following command in your terminal (Note: these commands are for Bash on MacOS and Linux):
```sh
pip install -r src/requirements.txt
```

### Running the tool

From the top level directory of the reporitory, run the following command:
```sh
pytest src/test_llvm.py
```

> The tool uses the Pytest suite

This will run the tool and handle everything for the user, the results for each instruction will be outputted to your terminal. Any failures will be highlighted by Pytest. Running with the `-v` option will expand the information available.

## Running the Tests

Each of the module files within the `src/` diretory has a related test file as part of this project. Currently the following python files have tests written:
- `validate_instruction.py`
- `llvm_ir_reader.py`

To run the tests, use the following command line:
```sh
python3 -m unittest discover tests/ "test_*"
```
> Running with `-v` will detail each test being run, rather than just a summary

All the unittest modules in this project support being run in isolation, this can be done by passing the file into python, for example:
```sh
python3 tests/test_validate_instruction.py
```

These tests are also run within CI when new commits are added to the main branch.

## Version History

### v0.1 - Inital Release
- Support for checking the earlyclobber contraint for the VHCADD instruction

### v0.2 - Support for Pytest
- Updated the logic to utilise Python's Pytest module.

### v0.3 - Expanded support for extra instructions
- The following instructions are now supported by the tool
    - VCADD (Both Integer and Floating Point variants)
    - VREV64
    - VCMUL (Floating Point)
    - VQDMULL
<!-- Hyperlinks -->
[llvm-project]:https://github.com/llvm/llvm-project
[ARM-Cortex-M-ARM]:https://developer.arm.com/documentation/ddi0553/by/?lang=en