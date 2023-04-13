/*
 * Copyright (c) 2023 Nordic Semiconductor ASA.
 *
 * SPDX-License-Identifier: LicenseRef-Nordic-5-Clause
 */

#include <zephyr/kernel.h>

int main(void)
{
	#ifdef CONFIG_SPI_NOR
	printk("SPI NOR Flash enabled\n");
	#endif

	#ifdef CONFIG_NORDIC_QSPI_NOR
	printk("QSPI NOR Flash enabled\n");
	#endif

	#ifdef CONFIG_BUILD_WITH_TFM
	printk("TFM enabled\n");
	#endif

	#ifdef CONFIG_BOARD_ENABLE_CPUNET
	printk("NETCORE enabled\n");
	#endif

	printk("Version: %s, board: %s\n", CONFIG_MCUBOOT_IMAGE_VERSION, CONFIG_BOARD);
	return 0;
}
