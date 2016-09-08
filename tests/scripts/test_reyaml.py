# -*- coding: utf-8 -*-
import pytest

pytest.importorskip('yaml')
import os
import subprocess

script_path = os.path.realpath(os.path.join(__file__, '..', '..', '..', 'scripts', 'reyaml'))

@pytest.mark.parametrize(('stdin', 'params', 'expected_stdout'), [
    ['a: b\n', [], 'a: b\n'],
    ['{a: b}\n', [], 'a: b\n'],
    ['[a, b, c]\n', [], '- a\n- b\n- c\n'],
    ])
def test_params(stdin, params, expected_stdout):
    p = subprocess.Popen(
            [script_path],
            stdin = subprocess.PIPE,
            stdout = subprocess.PIPE,
            )
    stdout, stderr = p.communicate(stdin)
    assert expected_stdout == stdout

def test_file_input(tmpdir):
    input_file = tmpdir.join('in')
    input_file.write('a: b')
    assert 'a: b\n' == subprocess.check_output(
            [script_path, '-i', input_file.strpath],
            )

def test_file_output(tmpdir):
    output_file = tmpdir.join('out')
    p = subprocess.Popen(
            [script_path, '-o', output_file.strpath],
            stdin = subprocess.PIPE,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            )
    stdout, stderr = p.communicate('a: b')
    assert stdout == ''
    assert stderr == ''
    assert 'a: b\n' == output_file.read()

def test_file_input_output(tmpdir):
    input_file = tmpdir.join('in')
    input_file.write('c: d')
    output_file = tmpdir.join('out')
    p = subprocess.Popen(
            [script_path, '-i', input_file.strpath, '-o', output_file.strpath],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            )
    stdout, stderr = p.communicate()
    assert stdout == ''
    assert stderr == ''
    assert 'c: d\n' == output_file.read()

def test_file_input_output_same(tmpdir):
    io_file = tmpdir.join('io')
    io_file.write('{b: 3}')
    p = subprocess.Popen(
            [script_path, '-i', io_file.strpath, '-o', io_file.strpath],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            )
    stdout, stderr = p.communicate()
    assert stdout == ''
    assert stderr == ''
    assert 'b: 3\n' == io_file.read()
