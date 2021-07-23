"""Dispatcher module."""

import sys
import asyncio
import logging
import signal
import time
from typing import List

from monitor import Monitor


class Dispatcher:

    def __init__(self, monitors: List[Monitor]) -> None:
        self._monitors = monitors
        self._monitor_tasks: List[asyncio.Task] = []
        self._logger = logging.getLogger(self.__class__.__name__)
        self._stopping = False

    def run(self) -> None:
        asyncio.run(self.start())

    def add_monitor_task(self, monitor: Monitor) -> None:
        self._monitor_tasks.append(
            asyncio.create_task(self._run_monitor(monitor))
        )

    async def start(self) -> None:
        self._logger.info('Starting up')

        for monitor in self._monitors:
            self.add_monitor_task(monitor)

        if sys.platform.startswith('win'):
            signal.signal(signal.SIGTERM, self.stop)
            signal.signal(signal.SIGINT, self.stop)
        else:
            asyncio.get_event_loop().add_signal_handler(signal.SIGTERM, self.stop)
            asyncio.get_event_loop().add_signal_handler(signal.SIGINT, self.stop)

        await asyncio.gather(*self._monitor_tasks)

        #
        # Runs until all tasks are completed;
        # TODO: create dynamic addition of tasks
        #

        self.stop()

    def stop(self) -> None:
        if self._stopping:
            return

        self._stopping = True

        self._logger.info('Shutting down')
        for task, monitor in zip(self._monitor_tasks, self._monitors):
            task.cancel()
        self._monitor_tasks.clear()
        self._logger.info('Shutdown finished successfully')

    @staticmethod
    async def _run_monitor(monitor: Monitor) -> None:
        def _until_next(last: float) -> float:
            time_took = time.time() - last
            return max(monitor.check_every - time_took, 0)

        while True:
            time_start = time.time()

            try:
                await monitor.check()
            except asyncio.CancelledError:
                break
            except Exception:
                monitor.logger.exception('Error executing monitor check')

            await asyncio.sleep(_until_next(last=time_start))
