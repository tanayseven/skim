import os
from multiprocessing.pool import Pool
from pathlib import Path

import click

from skim.raw_file import write_tokens, load_raw_text

CPU_COUNT = os.cpu_count()


@click.command()
@click.option('--input-dir', help='Path to all *.txt files to prepare for input')
@click.option('--output-dir', help='Path to write files for output dirs')
@click.option('--n', help='The N for N-Grams to be prepared', default='2')
def command(input_dir, output_dir, n):
    input_dir, output_dir, n = Path(input_dir), Path(output_dir), int(n)
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    tokeniser = load_raw_text(input_dir)
    with Pool(CPU_COUNT) as processes:
        grouped_tokens = processes.map(tokeniser.group_tokens, [num for num in range(2, n+1)])
    for group in grouped_tokens:
        write_tokens(group, output_dir)


if __name__ == '__main__':
    command()
