import subprocess

import pytest

import dualitee


def test_run(capfd):
    process = dualitee.run(['env', '--version'])

    stdout_sys, stderr_sys = capfd.readouterr()

    assert 'env' in process.stdout
    assert process.stderr == ''

    assert process.returncode == 0

    assert 'env' in stdout_sys
    assert stderr_sys == ''


def test_run_timeout():
    with pytest.raises(subprocess.TimeoutExpired):
        dualitee.run(['sleep', '9999'], timeout=0.001)


def test_run_shell(capfd):
    process = dualitee.run('env --version', shell=True)

    stdout_sys, stderr_sys = capfd.readouterr()

    assert 'env' in process.stdout
    assert process.stderr == ''

    assert process.returncode == 0

    assert 'env' in stdout_sys
    assert stderr_sys == ''


def test_run_bash(capfd):
    process = dualitee.run('echo $SHELL', shell=True, executable='bash')

    stdout_sys, stderr_sys = capfd.readouterr()

    assert 'bash' in process.stdout
    assert process.stderr == ''

    assert process.returncode == 0

    assert 'bash' in stdout_sys
    assert stderr_sys == ''


def test_run_env(capfd):
    process = dualitee.run('echo $VAR', env={'VAR': 'variable'}, shell=True)

    stdout_sys, stderr_sys = capfd.readouterr()

    assert process.stdout.rstrip() == 'variable'
    assert process.stderr == ''

    assert process.returncode == 0

    assert stdout_sys.rstrip() == 'variable'
    assert stderr_sys == ''


def test_run_stderr(capfd):
    process = dualitee.run('echo error >&2', shell=True)

    stdout_sys, stderr_sys = capfd.readouterr()

    assert process.stdout == ''
    assert process.stderr.rstrip() == 'error'

    assert process.returncode == 0

    assert stdout_sys == ''
    assert stderr_sys.rstrip() == 'error'


def test_run_check():
    with pytest.raises(subprocess.CalledProcessError):
        dualitee.run('exit 1', shell=True, check=True)
