# -*- coding: utf-8 -*-
import pytest

from ioex.calcex import Figure, UnitMismatchError
yaml = pytest.importorskip('yaml')


@pytest.mark.parametrize(('yaml_dumper'), [yaml.Dumper, yaml.SafeDumper])
@pytest.mark.parametrize(('figure'), [
    Figure(),
    Figure(123.4),
    Figure([1, 2]),
    Figure(None, u'm/s²'),
    Figure(123.4, u'm/s²'),
    Figure(1234, u'米/s²'),
])
def test_to_yaml(figure, yaml_dumper):
    class TestDumper(yaml_dumper):
        pass
    TestDumper.add_representer(
        type(figure),
        lambda d, f: figure.to_yaml(d, f, '!test-figure'))
    figure_yaml = yaml.dump(figure, Dumper=TestDumper)
    class TestLoader(yaml.SafeLoader):
        pass
    TestLoader.add_constructor(
        '!test-figure',
        lambda loader, node: loader.construct_mapping(node),
        )
    figure_attr = yaml.load(figure_yaml, Loader=TestLoader)
    assert set(['value', 'unit']) == set(figure_attr.keys())
    assert figure.value == figure_attr['value']
    assert figure.unit == figure_attr['unit']


@pytest.mark.parametrize(('yaml_dumper'), [yaml.Dumper, yaml.SafeDumper])
@pytest.mark.parametrize(('figure'), [
    Figure(123.4, u'm/s²'),
])
def test_register_yaml_representer(figure, yaml_dumper):
    class TestDumper(yaml_dumper):
        pass
    figure.register_yaml_representer(TestDumper)
    figure_yaml = yaml.dump(figure, Dumper=TestDumper)
    class TestLoader(yaml.SafeLoader):
        pass
    TestLoader.add_constructor(
        '!figure',
        lambda loader, node: loader.construct_mapping(node),
        )
    figure_attr = yaml.load(figure_yaml, Loader=TestLoader)
    assert set(['value', 'unit']) == set(figure_attr.keys())
    assert figure.value == figure_attr['value']
    assert figure.unit == figure_attr['unit']
