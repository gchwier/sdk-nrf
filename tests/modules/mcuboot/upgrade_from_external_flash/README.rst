

Overview
********

This application is based on `SMP Server Sample <https://docs.zephyrproject.org/latest/samples/subsys/mgmt/mcumgr/smp_svr/README.html>`_.
Added to test MCUBoot with external flash.
Required ``mcumgr``.

Available configurations for:

* nrf52840dk_nrf52840
* nrf5340dk_nrf5340_cpuapp
* nrf9160dk_nrf9160_ns

This test scenario will be later automated with `TwisterV2 <https://github.com/zephyrproject-rtos/twister>`_ framework.

Building and Testing - manual procedure
***************************************
Build application:

.. code-block:: console

   west build -p -b nrf9160dk_nrf9160_ns nrf/tests/modules/mcuboot/upgrade_from_external_flash -d build-91-upgrade

and flash the board:

.. code-block:: console

   west flash --erase -d build-91-upgrade

it should give output on the console:

.. code-block:: console

   *** Booting Zephyr OS build v3.2.99-ncs1-4-g8fb465f43f6a ***
   I: Starting bootloader
   I: Primary image: magic=unset, swap_type=0x1, copy_done=0x3, image_ok=0x3
   I: Secondary image: magic=unset, swap_type=0x1, copy_done=0x3, image_ok=0x3
   I: Boot source: none
   I: Swap type: none
   I: Bootloader chainload address offset: 0xc000
   I: Jumping to the first image slot
   
   uart:~$ *** Booting Zephyr OS build v3.2.99-ncs1-4-g8fb465f43f6a ***
   Version: 0.0.0+0, board: nrf9160dk_nrf9160

Build the same application, but with ``CONFIG_MCUBOOT_IMAGE_VERSION``  changed:

.. code-block:: console

   west build -p -b nrf9160dk_nrf9160_ns nrf/tests/modules/mcuboot/upgrade_from_external_flash -d build-91-upgrade1111 \
   -- -DCONFIG_MCUBOOT_IMAGE_VERSION=\"1.1.1+1\"

Assuming that te board uses the serial port ``ttyACM0`` upload the secondary app with ``mcumgr``:

.. code-block:: console

   mcumgr -t 60 --conntype serial --connstring=/dev/ttyACM0 image upload build-91-upgrade1111/zephyr/app_update.bin

To obtain a list of images use the following command:

.. code-block:: console

   mcumgr -t 60 --conntype serial --connstring=/dev/ttyACM0 image list
   Images:
   image=0 slot=0
      version: 0.0.0
      bootable: true
      flags: active confirmed
      hash: 14ef291ff3b63025b1f3413a56db5bff4adf28380831a7ddd47a209f0e2f2380
   image=0 slot=1
      version: 1.1.1.1
      bootable: true
      flags:
      hash: 64b3aaf5f3e7125edb14c8db47c7d8014a6c0e8fd3c90ec01dcabe50d56592ca
   Split status: N/A (0)

In order to instruct MCUboot to swap the images we need to test the image first, making sure it boots:

.. code-block:: console

   mcumgr -t 60 --conntype serial --connstring=/dev/ttyACM0 \
   image test 64b3aaf5f3e7125edb14c8db47c7d8014a6c0e8fd3c90ec01dcabe50d56592ca
   ...
   image=0 slot=1
      version: 1.1.1.1
      bootable: true
      flags: pending

One can now run the newly uploaded image by performing a soft reset of the board:

.. code-block:: console

   mcumgr -t 60 --conntype serial --connstring=/dev/ttyACM0 reset

MCUboot will swap the images and boot the new application, showing this output to the console:

.. code-block:: console

   *** Booting Zephyr OS build v3.2.99-ncs1-4-g8fb465f43f6a ***
   I: Starting bootloader
   I: Primary image: magic=unset, swap_type=0x1, copy_done=0x3, image_ok=0x3
   I: Secondary image: magic=good, swap_type=0x2, copy_done=0x3, image_ok=0x3
   I: Boot source: none
   I: Swap type: test
   I: Starting swap using move algorithm.
   I: Bootloader chainload address offset: 0xc000
   I: Jumping to the first image slot
   
   uart:~$ *** Booting Zephyr OS build v3.2.99-ncs1-4-g8fb465f43f6a ***
   Version: 1.1.1+1, board: nrf9160dk_nrf9160

One can now confirm te new image with ``mcumgr``
or reset the board once again and MCUboot should revert the images, showing this output to the console:

.. code-block:: console

   *** Booting Zephyr OS build v3.2.99-ncs1-4-g8fb465f43f6a ***
   I: Starting bootloader
   I: Primary image: magic=good, swap_type=0x2, copy_done=0x1, image_ok=0x3
   I: Secondary image: magic=unset, swap_type=0x1, copy_done=0x3, image_ok=0x3
   I: Boot source: none
   I: Swap type: revert
   I: Starting swap using move algorithm.
   I: Secondary image: magic=unset, swap_type=0x1, copy_done=0x3, image_ok=0x3
   I: Bootloader chainload address offset: 0xc000
   I: Jumping to the first image slot
   
   uart:~$ *** Booting Zephyr OS build v3.2.99-ncs1-4-g8fb465f43f6a ***
   Version: 0.0.0+0, board: nrf9160dk_nrf9160

Version of MCUBoot image should be verified after every reset.
