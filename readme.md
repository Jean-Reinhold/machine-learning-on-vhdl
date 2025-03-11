# ML to VHDL: Offloading Models to FPGAs

This project demonstrates how to take trained machine-learning (ML) models (initially focusing on simple MLPs) and generate corresponding VHDL for FPGA-based inference. The primary goal is to measure inference speed and maintain a straightforward design that can be adapted for various types of ML architectures.


## Project Structure
```
.
├── pycache
│ └── config.cpython-312.pyc
├── config.py
├── main.py
├── ml_to_vhdl
│ ├── init.py
│ ├── pycache
│ │ └── init.cpython-312.pyc
│ └── mlp
│ ├── init.py
│ ├── pycache
│ │ ├── init.cpython-312.pyc
│ │ ├── cli.cpython-312.pyc
│ │ └── generate_vhdl.cpython-312.pyc
│ ├── cli.py
│ └── generate_vhdl.py
├── mlp_generated.vhd
└── samples
 └── mlp
 ├── biases.json
 └── weights.json
 ```

- config.py: Centralized logging configuration (and/or other global config) that each module can import.
- main.py: Top-level command-line entry point that dispatches to different subcommands (for instance, "mlp" vs "perceptron") using click.
- ml_to_vhdl/mlp/cli.py: Defines the CLI that loads MLP weights/biases (from JSON files), calls the VHDL-generation logic, and writes the resulting .vhd file.
- ml_to_vhdl/mlp/generate_vhdl.py: Contains the functions to build the VHDL source. It also includes code for writing constants, biases, and the forward pass.
- mlp_generated.vhd: The generated VHDL artifact. You typically won't commit it, but it’s helpful to see the output of the generation.
- samples/mlp/weights.json & samples/mlp/biases.json: Example JSON files storing MLP model parameters.

## Overview

1. Model Input: The user provides JSON files for weights and biases. For an MLP, each layer’s weight matrix is a 2D array, and each layer’s bias is a 1D array.
2. CLI: The mlp_cli command in mlp/cli.py reads these JSON files, converts them to NumPy arrays, and then calls generate_vhdl().
3. VHDL Generation: In generate_vhdl.py, the script:
 - Writes an entity (with a single integer vector as input and a single-bit output).
 - Declares constants for weights/biases.
 - Implements a forward pass.
 - Logs generation steps for debugging.
4. Result: A .vhd file (e.g., mlp_generated.vhd) is produced. You can then integrate it into your FPGA workflow to measure inference speed.

## Example Usage: MLP

1. Edit or Create your weights.json and biases.json in samples/mlp/. Ensure each layer of your MLP is represented properly:
 - weights.json = [ [ [1, -2], [3, 4] ], [ [2], [-1] ] ]
 - biases.json = [ [1, -1], [0] ]

2. Run:
```bash
 python3 main.py mlp --weights-file=samples/mlp/weights.json --biases-file=samples/mlp/biases.json --output-file=mlp_generated.vhd
````

 This command:
 - Reads JSON files
 - Generates the VHDL for your MLP
 - Outputs mlp_generated.vhd

3. Synthesize/Analyze:
 - In your FPGA toolchain (e.g., Quartus, Vivado), add the generated .vhd file, compile, and test resource usage or performance.

## Extending the Project

1. Add a New Model: Suppose you want to generate VHDL for a "perceptron" or "CNN".
 - Create a new folder under ml_to_vhdl (e.g., ml_to_vhdl/perceptron).
 - Add your CLI in ml_to_vhdl/perceptron/cli.py (similar to how MLP’s CLI is structured).
 - Implement your own generate_vhdl logic or reuse shared code.
 - Wire it up as a subcommand in main.py with a click.command().

2. Change the Activation: Currently, the generated VHDL simply checks if the final neuron is > 0 to output '1'. If you want a different activation or threshold, modify the final layer logic in generate_vhdl.py.

3. Switch Data Types: The examples assume integer arithmetic, but you could adapt code for fixed-point or even floating-point. You’d simply change the VHDL constant declarations and the forward pass math to accommodate new data types.

4. Improve Testing: You can add unit tests or integration tests that:
 - Provide known weights/biases.
 - Synthesize or simulate the .vhd in a test environment.
 - Compare its output to an expected result.

## Purpose

The goal is to measure how quickly and simply an ML model can be offloaded to an FPGA and tested. By generating straightforward VHDL, you can:
- Evaluate inference speed in hardware vs. a CPU.
- Evaluate resource usage (LUTs, DSP blocks, etc.).
- Gain insight into potential hardware accelerations for bigger or more complex models.

We keep the code modular, so that each model type (MLP, Perceptron, CNN, etc.) has its own CLI and generate_vhdl logic, letting you quickly adapt or extend for new architectures.