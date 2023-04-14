from .parametrica import ParametricaSingletone
from .parametrica.io import YAMLFileConfigIO, VirtualYAMLFileConfigIO
from .parametrica.types import Field, Fieldset
from .parametrica.rules import InRange, Min


class Log(Fieldset):
    level = Field[int](default=3).label("Уровень логирования").rule(InRange(0, 10)).hint('0..10')
    retention_days = Field[int](7).label("Срок хранения старых логов в днях ").rule(Min(1)).hint('(1+)')


class ServerSettings(Fieldset):
    port = Field[int](default=6060).label('Порт сервера').rule(InRange(0, 65535)).hint('0..65535')



class Config(ParametricaSingletone):
    server =Field[ServerSettings]().label('Настройки локального сервера')
    log = Field[Log]().label("Настройки логирования")


class DevConfig(ParametricaSingletone):
    debug_mode = Field[bool](default=False).hint('Режим разработчика.')


Config(YAMLFileConfigIO('settings.yaml'))
DevConfig(VirtualYAMLFileConfigIO('dev.env'))
