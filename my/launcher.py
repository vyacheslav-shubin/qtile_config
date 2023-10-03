import os
import re

from dbus_next.constants import MessageType

from libqtile.log_utils import logger
from libqtile.utils import add_signal_receiver
from libqtile.widget import base
from libqtile.lazy import lazy
import subprocess
from qtile_extras.popup.toolkit import (PopupRelativeLayout, PopupText, PopupImage)

controls = [
    PopupImage(
        filename="/usr/share/icons/Yaru-prussiangreen/32x32@2x/apps/nautilus.png",
        pos_x=0, pos_y=0,
        width=0.5, height=1,
        mouse_callbacks={
            "Button1": lazy.spawn("nautilus -w")
        }
    ),
    PopupImage(
        filename="/var/lib/swcatalog/icons/ubuntu-jammy-universe/64x64/telegram-desktop_telegram.png",
        pos_x=0.5, pos_y=0,
        width=0.5, height=1,
        mouse_callbacks={
            "Button1": lazy.spawn("/home/vyacheslav/data/apps/Telegram/Telegram")
        }

    ),

]

#def _show_power_menu(qtile):
#    layout.show(x=0, y=1350)

class Launcher(base._TextBox):
    defaults = []

    def _configure(self, qtile, bar):
        base._TextBox._configure(self, qtile, bar)
        pass

    def on_mouse_click(self, qtile):

        layout = PopupRelativeLayout(
                qtile, width=128, height=64,
                hide_on_mouse_leave=True,
                controls=controls, background="00000060",initial_focus=None,    )

        layout.show(x=0, y=1340)
        pass

    def __init__(self, **config):
        base._TextBox.__init__(self, "🚀", **config)
        self.layout = None
        self.add_defaults(Launcher.defaults)
        self.add_callbacks(
            {
                "Button1": lazy.function(self.on_mouse_click),
                "Button2": lazy.function(self.on_mouse_click),
            }
        )
