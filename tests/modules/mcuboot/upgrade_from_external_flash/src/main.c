/*
 * Copyright (c) 2023 Nordic Semiconductor ASA.
 *
 * SPDX-License-Identifier: LicenseRef-Nordic-5-Clause
 */

#include <zephyr/kernel.h>


void main(void)
{
	printk("Version: %s, board: %s\n", CONFIG_MCUBOOT_IMAGE_VERSION, CONFIG_BOARD);
}
