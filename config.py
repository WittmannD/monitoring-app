import os
from yaml import load, CLoader, CDumper
from setting import CONFIG_PATH


class Config(dict):

    LOADER = CLoader
    DUMPER = CDumper

    def __init__(self, *arg, **kwargs) -> None:
        super(Config, self).__init__(*arg, **kwargs)
        self._load()

    def _load(self) -> None:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            cfg = load(f.read(), self.LOADER)

        self.update(cfg)
