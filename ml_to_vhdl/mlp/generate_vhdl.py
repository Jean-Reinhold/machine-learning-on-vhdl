import logging
import numpy as np
from typing import List, IO

logger = logging.getLogger(__name__)


def write_vhdl_header(f: IO[str], input_size: int) -> None:
    logger.debug("Writing VHDL header for input size: %d", input_size)
    f.write("-- Auto-generated VHDL MLP\n")
    f.write("library IEEE;\n")
    f.write("use IEEE.STD_LOGIC_1164.ALL;\n")
    f.write("use IEEE.STD_LOGIC_ARITH.ALL;\n")
    f.write("use IEEE.STD_LOGIC_UNSIGNED.ALL;\n")
    f.write("\nentity MLP is\n")
    f.write(f"    Port (\n")
    f.write(f"        input_vec  : in  INTEGER_VECTOR({input_size - 1} downto 0);\n")
    f.write("        output_bit : out STD_LOGIC\n")
    f.write("    );\n")
    f.write("end MLP;\n\n")


def write_vhdl_constants(
    f: IO[str], weights: List[np.ndarray], biases: List[np.ndarray]
) -> None:
    for i, (w, b) in enumerate(zip(weights, biases)):
        logger.debug(
            "Writing constants for layer %d (weights shape: %s, bias length: %d)",
            i,
            w.shape,
            len(b),
        )
        rows = w.shape[0]
        cols = w.shape[1]
        f.write(
            f"    constant weights_layer_{i} : array(0 to {rows - 1}, 0 to {cols - 1}) of integer := (\n"
        )
        for row_index, row in enumerate(w):
            row_values = ", ".join(map(str, row))
            if row_index < rows - 1:
                f.write(f"        ({row_values}),\n")
            else:
                f.write(f"        ({row_values})\n")
        f.write("    );\n\n")
        bias_len = len(b)
        bias_values = ", ".join(map(str, b))
        f.write(
            f"    constant biases_layer_{i} : INTEGER_VECTOR({bias_len - 1} downto 0) := ({bias_values});\n\n"
        )


def write_vhdl_forward_pass(f: IO[str], weights: List[np.ndarray]) -> None:
    logger.debug("Writing forward pass logic.")
    f.write("    process(input_vec)\n")
    f.write("        variable sum_val : integer;\n")
    for i, w in enumerate(weights):
        cols = w.shape[1]
        f.write(
            f"        variable layer_{i}_output : INTEGER_VECTOR({cols - 1} downto 0);\n"
        )
    f.write("    begin\n\n")
    for i, w in enumerate(weights):
        logger.debug("Writing forward pass for layer %d", i)
        input_source = "input_vec" if i == 0 else f"layer_{i - 1}_output"
        rows = w.shape[0]
        cols = w.shape[1]
        f.write(f"        for j in 0 to {cols - 1} loop\n")
        f.write(f"            layer_{i}_output(j) := biases_layer_{i}(j);\n")
        f.write(f"            for k in 0 to {rows - 1} loop\n")
        f.write(
            f"                layer_{i}_output(j) := layer_{i}_output(j) + ({input_source}(k) * weights_layer_{i}(k, j));\n"
        )
        f.write("            end loop;\n")
        f.write("        end loop;\n\n")
    final_layer = len(weights) - 1
    f.write(f"        if layer_{final_layer}_output(0) > 0 then\n")
    f.write("            output_bit <= '1';\n")
    f.write("        else\n")
    f.write("            output_bit <= '0';\n")
    f.write("        end if;\n\n")
    f.write("    end process;\n")


def generate_vhdl(
    weights: List[np.ndarray],
    biases: List[np.ndarray],
    input_size: int,
    output_file: str = "mlp_generated.vhd",
) -> None:
    logger.debug("Generating VHDL file: %s", output_file)
    with open(output_file, "w") as f:
        write_vhdl_header(f, input_size)
        f.write("architecture Behavioral of MLP is\n")
        write_vhdl_constants(f, weights, biases)
        f.write("begin\n")
        write_vhdl_forward_pass(f, weights)
        f.write("end Behavioral;\n")
    logger.info("VHDL code successfully generated and saved to %s", output_file)
