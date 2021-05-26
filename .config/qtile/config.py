# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List  # noqa: F401
import os
from datetime import datetime
from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
import mywidget
from colors import color

mod = "mod4"

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    os.system(f'sh {home}')


keys = [
    # Switch between windows
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(),  desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key(
        [mod, "control"], "Left",
        lazy.spawn("amixer -q set Master 5%+"),
        desc="Grow window to the left"
    ),
    Key(
        [mod, "control"], "Right",
         lazy.spawn("amixer -q set Master 5%-"),
        desc="Grow window to the right"
    ),
    Key(
        [mod, "control"], "Down",
        lazy.layout.shrink(),
        desc="Grow window down"
    ),
    Key(
        [mod, "control"], "Up",
        lazy.layout.grow(),
        desc="Grow window up"
    ),
    Key(
        [mod], "m",
        lazy.layout.maximize(),
        desc="Reset all window sizes"
    ),
    Key(
        [mod, "control"], "m",
        lazy.layout.normalize(),
        desc="Reset all window sizes"
    ),

    # Keybinding for programs
    Key(
        [mod], "Return",
        lazy.spawn('urxvt'),
        desc="Launch terminal"
    ),
    Key(
        [mod], "d",
        lazy.spawn('rofi -show drun -show-icons -modi drun'),
        desc="Applications menu"
    ),
    Key(
        [mod, 'shift'], "p",
        lazy.spawn('rofi -modi "clipboard:greenclip print" -show clipboard -run-command "{cmd}"'),
        desc="Applications menu"
    ),
    Key(
        [mod], "p",
        lazy.spawn(
            'urxvt -name "myranger" -fn "xft:SauceCodePro Nerd Font Mono:size=10" -e sh -c "ranger"'),
        desc="Launch terminal"
    ),
    Key(
        [mod], "f",
        lazy.spawn('firefox'),
        desc="Launch firefox"
    ),
    Key(
        [mod], "c",
        lazy.spawn('urxvt -name "qalc" -geometry 30x15 -e qalc'),
        desc="Launch firefox"
    ),
    Key(
        [mod, 'shift'], "n",
        lazy.spawn('urxvt -e newsboat -ru ~/.config/rss/rss.txt'),
        desc="News boat launch"
    ),
    Key([], "Print",
        # lazy.spawn(f'gnome-screenshot -a -f {ScreenshotDir + datetime.strftime(datetime.now(), "%Y-%m-%d-%H%M%S")}.png'),
        lazy.spawn('scrotmenu'),
        desc="Launch terminal"),
    # Key([mod], "Return", lazy.spawn('urxvt'), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.spawn('rofi -show p -modi p:rofi-power-menu'), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),
]

groups = [
    Group('1'),
    Group('2'),
    Group('3'),
    Group('4'),
    Group('5'),
    Group('6'),
    Group('7'),
    Group('8'),
    Group('9')
]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])

layouts = [
    layout.MonadTall(
                border_focus=color.color4,
                border_width=3,
                margin=10,
               ),
    # layout.Columns(border_focus_stack='#d75f5f'),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix()
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='FirCode',
    fontsize=12,
    padding=3,
    background=color.background,
    foreground=color.color12,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(visible_groups=['1', '2', '3', '4', '5']),
                widget.Prompt(),
                widget.WindowName(
                                  format='{name}',
                                  max_chars=30),
                widget.Systray(),
                widget.Clock(
                             font='Exo SemiBold Regular',
                             fontsize=14,
                             format='%d-%b %I:%M %p', 
                             foreground=color.foreground,
                             padding=30,
                             ),
                widget.Spacer(),
                # crypto prices block
                widget.Sep(),
                widget.TextBox(text='BTC'),
                mywidget.Crypto(symbol='BTCUSDT', update_interval=10, 
                                mouse_callbacks={
                                                'Button1': lambda: qtile.cmd_spawn('chartbtc')
                                                },
                                ),
                widget.TextBox(text='ETH'),
                mywidget.Crypto(symbol='ETHUSDT', update_interval=10),
                widget.TextBox(text='BNB'),
                mywidget.Crypto(symbol='BNBUSDT', update_interval=10),
                widget.Sep(),
                mywidget.Icon(icon='disk'),
                mywidget.Disk(
                              update_interval=120,
                              foreground=color.color11),
                mywidget.Icon(icon='disk1'),
                mywidget.Disk(
                              update_interval=120,
                              foreground=color.color11, 
                              partition='/mnt/Data',
                              ),
                mywidget.Icon(icon='mem'),
                widget.Memory(
                              foreground=color.color11,
                              format='{MemUsed:,.0f}M ',
                              update_interval=10,
                              fontsize=12,
                             ),
                mywidget.VPN(
                            update_interval=30
                            ),
                mywidget.Icon(icon='keyboard'),
                widget.KeyboardLayout(
                                      foreground=color.color11,
                                      configured_keyboards=['us', 'ara'],
                                      padding=2,
                                      ),
                mywidget.Icon(icon='speaker'),
                widget.Volume(
                                step=5,
                                padding=0,
                                margin=0,
                                volume_app="pavucontrol",
                                fmt=" {0} ",
                                foreground=color.color11,
                             ),
                widget.Sep(),
                widget.Systray(),
                # widget.QuickExit(default_text='(LogOut)'),
                widget.Sep(),
            ],
            24,
        ),
    ),
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(visible_groups=['6', '7', '8', '9']),
                widget.Prompt(),
                widget.WindowName(),
                widget.Systray(),
                widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
                widget.QuickExit(),
            ],
            24,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(wm_class='DearPyGui'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
    Match(title='qalc'),  # terminal calculator
    Match(title='myranger'),  # ranger
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
