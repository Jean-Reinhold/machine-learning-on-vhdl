import json
import click
import logging
import numpy as np
from typing import List
from .generate_vhdl import generate_vhdl

logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "--weights-file", required=True, help="Path to JSON file containing MLP weights."
)
@click.option(
    "--biases-file", required=True, help="Path to JSON file containing MLP biases."
)
@click.option(
    "--output-file", default="mlp_generated.vhd", help="Output VHDL filename."
)
@click.option(
    "--input-size",
    type=int,
    default=None,
    help="Number of inputs. If omitted, derived from weights.",
)
def mlp_cli(weights_file: str, biases_file: str, output_file: str, input_size: int):
    weights, biases = load_weights_and_biases(
        weights_file=weights_file, biases_file=biases_file
    )

    generate_vhdl(weights, biases, input_size=input_size, output_file=output_file)
    logger.info("MLP VHDL generation complete.")


def load_weights_and_biases(
    weights_file: str, biases_file: str
) -> (List[np.ndarray], List[np.ndarray]):
    logger.debug("Loading weights from %s", weights_file)
    with open(weights_file, "r") as wf:
        raw_weights = json.load(wf)  # Should be a list of 2D arrays

    weights: List[np.ndarray] = []
    for i, layer in enumerate(raw_weights):
        arr = np.array(layer)
        assert (
            arr.ndim == 2
        ), f"weights_file layer {i} must be 2D. Got shape {arr.shape}."
        weights.append(arr)

    logger.debug("Loading biases from %s", biases_file)
    with open(biases_file, "r") as bf:
        raw_biases = json.load(bf)  # Should be a list of 1D arrays

    biases: List[np.ndarray] = []
    for i, bvec in enumerate(raw_biases):
        arr = np.array(bvec)
        assert (
            arr.ndim == 1
        ), f"biases_file layer {i} must be 1D. Got shape {arr.shape}."
        biases.append(arr)

    return weights, biases
