from cline.base_tasks import FlagTask


class VersionTask(FlagTask):
    def invoke(self) -> int:
        self.out.write(self._config.version or "unknown")
        self.out.write("\n")
        return 0

    @classmethod
    def cli_flag(cls) -> str:
        return "version"
