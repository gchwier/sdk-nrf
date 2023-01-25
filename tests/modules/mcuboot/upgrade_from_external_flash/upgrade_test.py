import logging
import pytest
import time
import re

from subprocess import check_output
from pathlib import Path
from twister2.builder.build_manager import BuildManager
from twister2.device.device_abstract import DeviceAbstract

logger = logging.getLogger(__name__)


def wait_for_message(iter_stdout, message, timeout=60):
    time_started = time.time()
    for line in iter_stdout:
        if line:
            logger.info("#: " + line)
        if message in line:
            return True
        if time.time() > time_started + timeout:
            return False


def run_command(command, log_output=False):
    logger.info(f"CMD: {command}")
    output = check_output(command, shell=True, text=True)
    if log_output:
        logger.info(output)
    return output


@pytest.mark.build_specification
def test_upgrade(dut: DeviceAbstract, build_manager: BuildManager):
    assert wait_for_message(dut.iter_stdout, "0.0.0")

    new_build_dir = str(build_manager.build_config.build_dir) + '_second_image'
    build_manager.build_config.build_dir = new_build_dir
    build_manager.build_config.extra_configs.append('CONFIG_MCUBOOT_IMAGE_VERSION="1.1.1+1"')
    build_manager.build()

    app_update_bin = str((Path(new_build_dir) / 'zephyr' / 'app_update.bin').resolve())
    connection_str = f"--conntype serial --connstring={dut.connection.portstr}"

    run_command(f"mcumgr -t 60 {connection_str} image upload {app_update_bin}")

    output = run_command(f"mcumgr -t 60 {connection_str} image list", log_output=True)
    hashes = re.findall(r"hash:\s(.*)\n", output)
    assert len(hashes) == 2

    run_command(f"mcumgr -t 60 {connection_str} image test {hashes[1]}")

    run_command(f"mcumgr -t 60 {connection_str} reset")

    # dut.connect()
    assert wait_for_message(dut.iter_stdout, "1.1.1")

    run_command(f"mcumgr -t 60 {connection_str} reset")

    assert wait_for_message(dut.iter_stdout, "0.0.0")
