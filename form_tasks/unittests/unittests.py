import ast
import asyncio
import pathlib
import threading
import docker
import aiohttp
import pytest

from docker.models.containers import Container


def get_cur_dir():
    """Для обхода проблемы с путями pytest"""
    return pathlib.Path(__file__).parent.resolve()


async def logs(cont, name):
    """Исходная функция"""
    conn = aiohttp.UnixConnector(path="/var/run/docker.sock")
    async with aiohttp.ClientSession(connector=conn) as session:
        async with session.get(f"http://xx/containers/{cont}/logs?follow=1&stdout=1") as resp:
            async for line in resp.content:
                # лучше не делать логи с помощью принтов
                # из-за отсутствия decode() возникли огромные проблемы, пришлось юзать костыли)
                print(name, line)


class TestLogs:
    container_name = 'test_container'
    logger_name = 'test'

    @pytest.fixture(scope='function')
    def container(self):
        client = docker.from_env()  # тут можно конфигурацию сменить
        _name: str = None
        _cont: Container = None

        def _container(name) -> Container:
            nonlocal _name, _cont
            _name = name
            image = client.images.build(path=f'{get_cur_dir()}/docker_container', tag=name)
            _cont = client.containers.run(image=name, detach=True, name=name, stdout=True, stderr=True)
            return _cont

        yield _container
        _cont.kill()
        _cont.remove()

    def run_logs_in_another_thead(self, cont: str, name: str) -> threading.Thread:
        """Запускаем логгер в отдельном потоке"""
        def _logs(*args):
            asyncio.run(logs(*args))

        return threading.Thread(target=_logs, args=(cont, name), daemon=True)

    def decode_captured_logs(self, captured_logs: str) -> list:
        logs_captured = []
        for line in captured_logs.splitlines():
            splitted = line.rsplit(maxsplit=1)
            name = splitted[0]
            log = splitted[1]
            # этих костылей можно было избежать, если бы в исходной функции был бы decode()
            # используем безопасный eval, для того чтобы преобразовать байтовый литерал и отсекаем перенос строки
            log = ast.literal_eval(log)[0:-1]
            log_decoded = log.decode()  # декодирование байтов
            log_filtered = ''.join(c for c in log_decoded if c.isprintable())  # удаляем управляющие символы
            logs_captured.append((name, log_filtered))
        return logs_captured

    @pytest.mark.asyncio
    async def test_logs(self, container, capsys):
        container = container(self.container_name)
        thread = self.run_logs_in_another_thead(self.container_name, self.logger_name)
        thread.start()

        logs_captured_raw = capsys.readouterr().out
        decoded_captured_logs = self.decode_captured_logs(logs_captured_raw)
        container_logs = container.logs(stdout=True, stderr=True).decode('utf-8').strip().splitlines()
        assert len(decoded_captured_logs) == len(container_logs)
        for i in range(len(decoded_captured_logs)):
            assert self.logger_name == decoded_captured_logs[1]
            assert container_logs[i] == decoded_captured_logs[1]
