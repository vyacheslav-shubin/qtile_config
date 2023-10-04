import os
import re

from dbus_next.constants import MessageType

from libqtile.log_utils import logger
from libqtile.utils import add_signal_receiver
from libqtile.widget import base
from libqtile.lazy import lazy
import subprocess
from qtile_extras.popup.toolkit import (PopupGridLayout, PopupText, PopupImage)

controls = [
    PopupImage(
        row=0, col=0,
        filename="/usr/share/icons/hicolor/64x64/apps/firefox.png",
        mouse_callbacks={"Button1": lazy.spawn("firefox")}
    ),
    PopupImage(
        row=0, col=1,
        filename="/var/lib/swcatalog/icons/ubuntu-jammy-universe/64x64/telegram-desktop_telegram.png",
        mouse_callbacks={"Button1": lazy.spawn("/home/vyacheslav/data/apps/Telegram/Telegram")}
    ),
   PopupImage(
       row=0, col=2,
       filename="/usr/share/icons/Yaru-prussiangreen/32x32@2x/apps/nautilus.png",
       mouse_callbacks={"Button1": lazy.spawn("nautilus -w")}
   ),
   PopupImage(
       row=0, col=3,
       filename="/usr/share/icons/hicolor/64x64/apps/clementine.png",
       mouse_callbacks={"Button1": lazy.spawn("clementine")}
   ),
    PopupImage(
        row=1, col=0,
        filename="/var/lib/swcatalog/icons/ubuntu-jammy-universe/64x64/freecad-common_freecad.png",
        mouse_callbacks={"Button1": lazy.spawn("/home/vyacheslav/data/apps/FreeCAD_0.21.1-Linux-x86_64.AppImage")}
    )
]

#def _show_power_menu(qtile):
#    layout.show(x=0, y=1350)

class Launcher(base._TextBox):
    defaults = []

    def _configure(self, qtile, bar):
        base._TextBox._configure(self, qtile, bar)
        pass

    def on_mouse_click(self, qtile):
        r=2
        c=4
        layout = PopupGridLayout(
            qtile, width=c*64, height=r*64,
            rows=r, cols=c,
            hide_on_mouse_leave=True,
            controls=controls, background="00000060",initial_focus=None,    )

        layout.show(x=0, y=1405-r*64)
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
