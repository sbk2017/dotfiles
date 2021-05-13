#!/usr/bin/env python3

import rofi_menu
import os


class MountMenu(rofi_menu.Menu):
    prompt = 'Mount'
    dirs = {
        'Home': '/mnt/nasbox/home',
        'Movies': '/mnt/Movies'
    }
    mount = '(<span bgcolor="#339933" color="white"> <b>mount</b> </span>)'
    items = []
    for k, v in dirs.items():
        if os.path.ismount(v):
            items.append(rofi_menu.ShellItem(f'{k} at {v} mounted  (<span bgcolor="#b30000" color="black"><b>unmount</b> </span>)',
                f'umount {v}'))
        else:
            items.append(rofi_menu.ShellItem(f'{k:<10}{v:<30} {mount:>25}', f'mount {v}'))

if __name__ == "__main__":
    rofi_menu.run(MountMenu())
