#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import os

import pandas as pd
import wandb

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    logging.info("Strating basic cleaning")
    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    artifact_local_path = run.use_artifact(args.input_artifact).file()

    try:
        df = pd.read_csv(artifact_local_path, index_col="id")
        min_price = args.min_price
        max_price = args.max_price
        idx = df["price"].between(min_price, max_price)
        df = df[idx].copy()
        logger.info(
            "Dataset price outliers removal outside range: %s-%s",
            args.min_price,
            args.max_price,
        )
        df["last_review"] = pd.to_datetime(df["last_review"])

        idx = df["longitude"].between(-74.25, -73.50) & df["latitude"].between(
            40.5, 41.2
        )
        df = df[idx].copy()

    except Exception as error:
        logging.error("Failed to read and clean dataset: {error}".format(error=error))

    else:
        df.to_csv("clean_sample.csv", index=False)

        artifact = wandb.Artifact(
            args.output_artifact,
            type=args.output_type,
            description=args.output_description,
        )

        artifact.add_file(args.output_artifact)
        run.log_artifact(artifact)

        artifact.wait()
        logger.info("Cleaned dataset uploaded to wandb")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")

    parser.add_argument(
        "--input_artifact", type=str, help="Input artifact name", required=True
    )

    parser.add_argument(
        "--output_artifact", type=str, help="Output artifact name", required=True
    )

    parser.add_argument("--output_type", type=str, help="Output type", required=True)

    parser.add_argument(
        "--output_description", type=str, help="Output description", required=True
    )

    parser.add_argument("--min_price", type=int, help="Min price limit", required=True)

    parser.add_argument("--max_price", type=int, help="Max price limit", required=True)

    args = parser.parse_args()

    go(args)
