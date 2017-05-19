class AttributeDescriptor(object):

    def __init__(self, name):
        self._name = name

    def __get__(self, instance, owner):
        return getattr(instance, self._name)

    def __set__(self, instance, value):
        setattr(instance, self._name, value)
