#!/usr/bin/env python
"""
Script to download from a URL to a local destination
"""
import argparse
import logging
import os

import wandb
from .components.wandb_utils.log_artifact import log_artifact

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="get_data")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    logger.info(f"Returning sample {args.sample}")
    logger.info(f"Uploading {args.artifact_name} to Weights & Biases")
    log_artifact(
        args.artifact_name,
        args.artifact_type,
        args.artifact_description,
        os.path.join("data", args.sample),
        run,
    )


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Download data")

    parser.add_argument(
        "--sample", type=str, help="Name of the sample to download", required=True
    )

    parser.add_argument(
        "--artifact_name", type=str, help="Name for the output artifact", required=True
    )

    parser.add_argument(
        "--artifact_type", type=str, help="Output artifact type", required=True
    )

    parser.add_argument(
        "--artifact_description",
        type=str,
        help="A brief description of this artifact",
        required=True,
    )

    args = parser.parse_args()

    go(args)
