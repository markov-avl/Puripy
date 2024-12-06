from inspect import Parameter

from puripy.context.property import PropertySourceReader
from puripy.utils.metadata_utils import is_properties
from puripy.utils.reflection_utils import params_of

from puripy.context.dependency.type import Dependency, ParameterDependency

_DependencyType = Dependency | ParameterDependency


class DependencyResolver:

    def get_dependencies(self, cls: type, factory: type = None) -> list[_DependencyType]:
        # getting dependencies of `__init__`
        dependencies: list[_DependencyType] = [self.__to_parameter_dependency(p) for p in params_of(cls)]

        # if factory exists, it means that first parameter is a factory instance (`self`)
        if factory:
            dependencies[0].type = factory

        # property classes are always indirectly dependent on PropertySourceParser
        if is_properties(cls):
            dependency = Dependency(is_direct=False, type=PropertySourceReader)
            dependencies.append(dependency)

        return dependencies

    @staticmethod
    def __to_parameter_dependency(parameter: Parameter) -> ParameterDependency:
        return ParameterDependency(
            is_direct=True,
            type=parameter.annotation,
            parameter_name=parameter.name
        )
