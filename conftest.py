from pathlib import Path
import sys, pytest

pytest_plugins = "pytester"
collect_ignore = [ 'template.py' ]


@pytest.fixture
def data(request):
    cwd = Path(request.fspath).parent
    return lambda f: (cwd / f).open()


@pytest.fixture
def ascript(request, pytester):
    dir = Path(request.fspath).parent
    def runner(inp):
        result = pytester.run(sys.executable, request.fspath, str(dir/inp))
        assert result.ret == 0
        assert not result.errlines
        return str(result.stdout) + '\n' # just assume trailing newline
    return runner
