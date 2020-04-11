import asyncio
from contextlib import suppress


class PeriodicTimer:
    def __init__(self, func, time):
        self.func = func
        self.time = time
        self.is_started = False
        self._task = None

    async def start(self):
        if not self.is_started:
            self.is_started = True
            # Start task to call func periodically:
            self._task = asyncio.ensure_future(self._run())

    async def stop(self):
        if self.is_started:
            self.is_started = False
            # Stop task and await it stopped:
            self._task.cancel()
            with suppress(asyncio.CancelledError):
                await self._task

    async def _run(self):
        while True:
            await asyncio.sleep(self.time)
            await self.func()


class KarmaCooldownTimer(PeriodicTimer):
    def __init__(self, func, time, guild_id, member_id):
        super().__init__(func, time)
        self.guild_id = guild_id
        self.member_id = member_id

    async def start(self):
        if not self.is_started:
            self.is_started = True
            # Start task to call func periodically:
            self._task = asyncio.ensure_future(self._run_with(guild_id=self.guild_id, member_id=self.member_id))

    async def _run_with(self, guild_id, member_id):
        while True:
            await asyncio.sleep(self.time)
            await self.func(guild_id, member_id)
            break
        await self.stop()
