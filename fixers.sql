use fixers;
SELECT * from systemissues;
insert into systemissues
values('HI1','No bootable device found','1. Switch off the system.
2. Disconnect all power cables to the servers power supply units.
3. Remove the system cover.
4. Reseat all the cables of hard drive backplane at both ends.
5. Reseat all the drives.
6. Replace the system cover.
7. Connect the power cables to the servers power supply units.
8. Power on the system
9. To enter UEFI, Press F2.
10. Verify that all installed drives are detected in controller BIOS, if not detected refer to the Troubleshooting Hard drive issues
section.
11. Ensure that in BIOS the RAID setting is set to RAID mode for SATA drives.
12. Save the setting, and reboot the server.
13. If the issue persists, contact Technical Support for assistance.
');
insert into systemissues values('HI2','USB device not connected.','1. Disconnect the device and reconnect them. \n2. If the problem persists, connect
 the keyboard and/or mouse to another USB port on the system. \n3. Turn off all attached USB devices, and disconnect them from the system and restart the sy
stem. \n5. Reconnect and turn on each USB device one at a time. \n6.If the problem persists, get help from the support center.');
select * from systemissues;