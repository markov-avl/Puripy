from inspect import Parameter

from puripy.utils.metadata_utils import is_properties
from puripy.utils.reflection_utils import params_of

from .dependency import Dependency, ParameterDependency

_DependencyType = Dependency | ParameterDependency


class DependencyResolver:

    def get_dependencies(self, cls: type, factory: type = None) -> list[_DependencyType]:
        # property classes are always independent
        if is_properties(cls):
            return []

        # getting dependencies of `__init__`
        dependencies: list[_DependencyType] = [self.__to_parameter_dependency(p) for p in params_of(cls)]

        # if factory exists, it means that first parameter is a factory instance (`self`)
        if factory:
            dependencies[0].annotation = factory

        return dependencies

    @staticmethod
    def __to_parameter_dependency(parameter: Parameter) -> ParameterDependency:
        return ParameterDependency(
            annotation=parameter.annotation,
            name=parameter.name
        )
