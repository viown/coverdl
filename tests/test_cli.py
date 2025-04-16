from click.testing import CliRunner
from coverdl.cli import coverdl

def test_version_output():
    runner = CliRunner()
    result = runner.invoke(coverdl, ['--version'])

    assert result.exit_code == 0
