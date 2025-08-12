from ..core.base_session import BaseSession
from niffler_e_2_e_tests_python.models.config import Envs


def create_session(envs: Envs, use_colored: bool = True) -> BaseSession:
    """Фабрика для создания сессии с использованием настроек окружения

    Args:
        envs: Фикстура с настройками окружения
        use_colored: Использовать цветные шаблоны для логирования

    Returns:
        BaseSession: Настроенный экземпляр сессии
    """
    return BaseSession(
        base_url=envs.gateway_url,  # Используем URL из фикстуры envs
        use_colored_templates=use_colored
    )