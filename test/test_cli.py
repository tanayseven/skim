import os
from pathlib import Path
from tempfile import TemporaryDirectory

from click.testing import CliRunner

from skim.cli import command


def test_cli():

    with TemporaryDirectory() as temp_directory:
        temp_input_dir = Path(f'{temp_directory}/input/')
        temp_output_dir = Path(f'{temp_directory}/output/')
        os.makedirs(temp_input_dir)
        os.makedirs(temp_output_dir)
        with open(temp_input_dir / 'sample.txt', 'w') as f:
            f.write('This is a simple string to be written')
        runner = CliRunner()
        result = runner.invoke(command, [f'--input-dir={temp_input_dir}', f'--output-dir={temp_output_dir}', '--n=3'])
        print(result.output)
        with open(temp_output_dir / '2.txt') as f:
            prepared_content_2 = f.read()
        with open(temp_output_dir / '3.txt') as f:
            prepared_content_3 = f.read()
        assert prepared_content_2
        assert prepared_content_3

