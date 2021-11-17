from cline.base_tasks import EagerTask


class HelpTask(EagerTask):
    def invoke(self) -> int:
        self._config.render_help()
        return 0
