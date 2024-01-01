import os
import subprocess

# The decky plugin module is located at decky-loader/plugin
# For easy intellisense checkout the decky-loader code one directory up
# or add the `decky-loader/plugin` path to `python.analysis.extraPaths` in `.vscode/settings.json`
import decky_plugin

KDECONNECTD_UNIT_NAME = "decky-kde-connectd"


class Plugin:
    # A normal method. It can be called from JavaScript using call_plugin_function("method_1", argument1, argument2)
    async def add(self, left, right):
        return left + right

    async def list_avaliable(self):
        outputs = subprocess.run(["kdeconnect-cli", "-a"], capture_output=True)
        return

    # Asyncio-compatible long-running code, executed in a task when the plugin is loaded
    async def _main(self):
        decky_plugin.logger.info("Try to run kdeconnectd")
        outputs = subprocess.run(
            [
                "systemd-run",
                "--user",
                "--unit",
                KDECONNECTD_UNIT_NAME,
                "/usr/lib/kdeconnectd",
            ],
            check=False,
            capture_output=True,
            encoding="UTF-8",
        )
        if outputs.returncode != 0:
            decky_plugin.logger.error(f"fail to start systemd: {outputs.stderr}")
        return outputs.returncode == 0

    # Function called first during the unload process, utilize this to handle your plugin being removed
    async def _unload(self):
        decky_plugin.logger.info("Stopping kdeconnectd")
        outputs = subprocess.run(
            ["systemctl", "--user", "stop", KDECONNECTD_UNIT_NAME],
            check=False,
            capture_output=True,
        )
        if outputs.returncode != 0:
            decky_plugin.logger.error(f"fail to stop kdeconnectd: {outputs.stderr}")
        # TODO: reload systemd?
        return outputs.returncode == 0

    # Migrations that should be performed before entering `_main()`.
    async def _migration(self):
        pass
