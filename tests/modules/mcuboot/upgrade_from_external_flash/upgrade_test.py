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
            logger.debug("#: " + line)
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


@pytest.mark.build_specification('mcuboot.upgrade_from_external_flash')
@pytest.mark.usefixtures('skip_if_not_executable')
def test_upgrade_revert_confirm(dut: DeviceAbstract, build_manager: BuildManager):
    assert wait_for_message(dut.iter_stdout, "0.0.0")

    logger.info('Build second image with new MCUboot image version')
    new_build_dir = str(build_manager.build_config.build_dir) + '_second_image'
    build_manager.build_config.build_dir = new_build_dir
    build_manager.build_config.cmake_extra_args.append('-DCONFIG_MCUBOOT_IMAGE_VERSION="1.1.1+1"')
    build_manager.build()

    logger.info('Upload APP image with mcumgr')
    app_update_bin = str((Path(new_build_dir) / 'zephyr' / 'app_update.bin').resolve())
    connection_str = f"--conntype serial --connstring={dut.connection.portstr}"
    run_command(f"mcumgr -t 60 {connection_str} image upload {app_update_bin}")
    output = run_command(f"mcumgr -t 60 {connection_str} image list", log_output=True)
    hashes = re.findall(r"hash:\s(.*)\n", output)
    assert len(hashes) == 2

    logger.info('Test uploaded APP image')
    run_command(f"mcumgr -t 60 {connection_str} image test {hashes[1]}")
    run_command(f"mcumgr -t 60 {connection_str} reset")
    assert wait_for_message(dut.iter_stdout, "1.1.1")

    logger.info('Revert images')
    run_command(f"mcumgr -t 60 {connection_str} reset")
    assert wait_for_message(dut.iter_stdout, "0.0.0")

    logger.info('Test and confirm APP image')
    run_command(f"mcumgr -t 60 {connection_str} image test {hashes[1]}")
    run_command(f"mcumgr -t 60 {connection_str} reset")
    assert wait_for_message(dut.iter_stdout, "1.1.1")
    run_command(f"mcumgr -t 60 {connection_str} image confirm {hashes[1]}")
    run_command(f"mcumgr -t 60 {connection_str} reset")
    assert wait_for_message(dut.iter_stdout, "1.1.1")


@pytest.mark.build_specification('mcuboot.upgrade_from_external_flash_with_netcore')
@pytest.mark.usefixtures('skip_if_not_executable')
def test_upgrade_with_netcore(dut: DeviceAbstract, build_manager: BuildManager):
    assert wait_for_message(dut.iter_stdout, "0.0.0")

    logger.info('Build second image with new MCUboot image version')
    new_build_dir = str(build_manager.build_config.build_dir) + '_second_image'
    build_manager.build_config.build_dir = new_build_dir
    build_manager.build_config.cmake_extra_args.append('-DCONFIG_MCUBOOT_IMAGE_VERSION="1.1.2+1"')
    build_manager.build()

    logger.info('Upload APP and NETCORE images with mcumgr')
    app_update_bin = str((Path(new_build_dir) / 'zephyr' / 'app_update.bin').resolve())
    net_core_app_update = str((Path(new_build_dir) / 'zephyr' / 'net_core_app_update.bin').resolve())
    connection_str = f"--conntype serial --connstring={dut.connection.portstr}"
    run_command(f"mcumgr -t 60 {connection_str} image upload {app_update_bin} -e -n 0")
    run_command(f"mcumgr -t 60 {connection_str} image upload {net_core_app_update} -e -n 1")
    output = run_command(f"mcumgr -t 60 {connection_str} image list", log_output=True)
    hashes = re.findall(r"hash:\s(.*)\n", output)
    assert len(hashes) == 3

    logger.info('Test uploaded APP and NETCORE images')
    run_command(f"mcumgr -t 60 {connection_str} image test {hashes[1]}")
    run_command(f"mcumgr -t 60 {connection_str} image test {hashes[2]}")
    run_command(f"mcumgr -t 60 {connection_str} reset")
    assert wait_for_message(dut.iter_stdout, "1.1.2")
