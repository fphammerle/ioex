# -*- coding: utf-8 -*-
import pytest

from ioex.calcex import Figure
yaml = pytest.importorskip('yaml')


@pytest.mark.parametrize(('yaml_loader'), [yaml.Loader, yaml.SafeLoader])
@pytest.mark.parametrize(('figure_yaml', 'expected_figure'), [
    ['!fig {value: null, unit: null}', Figure()],
    ['!fig {value: 123.4, unit: null}', Figure(123.4)],
    ['!fig {value: [1, 2], unit: null}', Figure([1, 2])],
    ['!fig {value: null, unit: kg}', Figure(unit='kg')],
    ['!fig {value: 123.4, unit: km/h}', Figure(123.4, 'km/h')],
    ['!fig {value: [1, 2], unit: km/h}', Figure([1, 2], 'km/h')],
    ['!fig "?"', Figure()],
    ['!fig 123.4', Figure(123.4)],
    ['!fig 123.0', Figure(123.0)],
    ['!fig "? kg"', Figure(unit='kg')],
    ['!fig 123.4 km/h', Figure(123.4, 'km/h')],
    ['!fig 1234', Figure(1234)],
    ['!fig -123', Figure(-123)],
    [u'!fig 1234 米/s²', Figure(1234, u'米/s²')],
])
def test_register_yaml_constructor(figure_yaml, expected_figure, yaml_loader):
    class TestLoader(yaml_loader):
        pass
    Figure.register_yaml_constructor(TestLoader, tag='!fig')
    generated_figure = yaml.load(figure_yaml, Loader=TestLoader)
    assert expected_figure == generated_figure
    assert isinstance(generated_figure.value, type(expected_figure.value))


@pytest.mark.parametrize(('yaml_dumper'), [yaml.Dumper, yaml.SafeDumper])
@pytest.mark.parametrize(('figure', 'expected_text'), [
    [Figure(), '?'],
    [Figure(1234), '1234'],
    [Figure(-123), '-123'],
    [Figure(123.4), '123.4'],
    [Figure(-12.3), '-12.3'],
    [Figure(None, u'm/s²'), u'? m/s²'],
    [Figure(None, u'm/(s·s)'), u'? m/(s·s)'],
    [Figure(1234, u'米/s²'), u'1234 米/s²'],
    [Figure(123.4, u'm/s²'), u'123.4 m/s²'],
])
def test_to_yaml_scalar(figure, expected_text, yaml_dumper):
    class TestDumper(yaml_dumper):
        pass
    TestDumper.add_representer(
        type(figure),
        lambda d, f: figure.to_yaml(d, f, '!fig')
    )
    generated_yaml = yaml.dump(figure, Dumper=TestDumper)

    class TestLoader(yaml.SafeLoader):
        pass
    TestLoader.add_constructor(
        '!fig',
        lambda loader, node: loader.construct_scalar(node),
    )
    assert expected_text == yaml.load(generated_yaml, Loader=TestLoader)


@pytest.mark.parametrize(('yaml_dumper'), [yaml.Dumper, yaml.SafeDumper])
@pytest.mark.parametrize(('figure'), [
    Figure([1, 2]),
    Figure([1, 2], u'm/s²'),
    Figure({'x': 1, 'y': -2}, u'米/s²'),
])
def test_to_yaml_mapping(figure, yaml_dumper):
    class TestDumper(yaml_dumper):
        pass
    TestDumper.add_representer(
        type(figure),
        lambda d, f: figure.to_yaml(d, f, '!fig')
    )
    generated_yaml = yaml.dump(figure, Dumper=TestDumper)

    class TestLoader(yaml.SafeLoader):
        pass
    TestLoader.add_constructor(
        '!fig',
        lambda loader, node: loader.construct_mapping(node),
    )
    figure_attr = yaml.load(generated_yaml, Loader=TestLoader)
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
    figure.register_yaml_representer(TestDumper, tag='!test-fig')
    generated_yaml = yaml.dump(figure, Dumper=TestDumper)

    class TestLoader(yaml.SafeLoader):
        pass
    figure.register_yaml_constructor(TestLoader, tag='!test-fig')
    loaded_figure = yaml.load(generated_yaml, Loader=TestLoader)
    assert figure == loaded_figure
