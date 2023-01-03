/*
 * Copyright (c) 2023 Nordic Semiconductor ASA.
 *
 * SPDX-License-Identifier: LicenseRef-Nordic-5-Clause
 */

#include <zephyr/kernel.h>


#ifdef CONFIG_MCUMGR_CMD_OS_MGMT
#include <os_mgmt/os_mgmt.h>
#endif
#ifdef CONFIG_MCUMGR_CMD_IMG_MGMT
#include <img_mgmt/img_mgmt.h>
#endif
#ifdef CONFIG_MCUMGR_CMD_STAT_MGMT
#include <stat_mgmt/stat_mgmt.h>
#endif
#ifdef CONFIG_MCUMGR_CMD_SHELL_MGMT
#include <shell_mgmt/shell_mgmt.h>
#endif


void main(void)
{
	/* Register the built-in mcumgr command handlers. */

#ifdef CONFIG_MCUMGR_CMD_OS_MGMT
	os_mgmt_register_group();
#endif
#ifdef CONFIG_MCUMGR_CMD_IMG_MGMT
	img_mgmt_register_group();
#endif
#ifdef CONFIG_MCUMGR_CMD_STAT_MGMT
	stat_mgmt_register_group();
#endif
#ifdef CONFIG_MCUMGR_CMD_SHELL_MGMT
	shell_mgmt_register_group();
#endif

	printk("Version: %s, board: %s\n", CONFIG_MCUBOOT_IMAGE_VERSION, CONFIG_BOARD);
}
