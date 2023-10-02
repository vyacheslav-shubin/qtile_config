import os
import re

from dbus_next.constants import MessageType

from libqtile.log_utils import logger
from libqtile.utils import add_signal_receiver
from libqtile.widget import base
from libqtile.lazy import lazy
import subprocess


def show_power_menu(qtile, message):
    kbd_dbus_prev_cmd = "dbus-send --dest=ru.gentoo.KbddService /ru/gentoo/KbddService ru.gentoo.kbdd.prev_layout"
    kbd_dbus_next_cmd = "dbus-send --dest=ru.gentoo.KbddService /ru/gentoo/KbddService ru.gentoo.kbdd.next_layout"
    qtile.spawn(kbd_dbus_next_cmd)
    from qtile_extras.popup.toolkit import (PopupRelativeLayout, PopupImage, PopupText)
    text_message = PopupText(text=message, pos_x=0, pos_y=0, width=1, height=1, h_align="center")
    controls = [text_message]
    layout = PopupRelativeLayout(qtile, width=200, height=200, controls=controls, background="00000060",initial_focus=None,    )
    layout.show()
    #import os
    #os.system(kbd_dbus_next_cmd)


class KeyboardKbdd(base.ThreadPoolText):
    """Widget for changing keyboard layouts per window, using kbdd

    kbdd should be installed and running, you can get it from:
    https://github.com/qnikst/kbdd

    The widget also requires dbus-next_.

    .. _dbus-next: https://pypi.org/project/dbus-next/
    """

    defaults = [
        ("update_interval", 1, "Update interval in seconds."),
        (
            "configured_keyboards",
            ["us", "ru"],
            "your predefined list of keyboard layouts." "example: ['us', 'ir', 'es']",
        ),
        (
            "colours",
            None,
            "foreground colour for each layout"
            "either 'None' or a list of colours."
            "example: ['ffffff', 'E6F0AF']. ",
        ),
    ]

    def change_layout(self):
        #kbd_dbus_next_cmd = "dbus-send --dest=ru.gentoo.KbddService /ru/gentoo/KbddService ru.gentoo.kbdd.next_layout"
        if self.layout_index==0:
            nl = 1
        else:
            nl = 0
        kbd_dbus_next_cmd = "dbus-send --dest=ru.gentoo.KbddService /ru/gentoo/KbddService ru.gentoo.kbdd.set_layout uint32:" + str(nl)
        subprocess.call(kbd_dbus_next_cmd, shell=True)
        self._layout_changed(nl)
        self.update(self.poll())

    def __init__(self, **config):
        base.ThreadPoolText.__init__(self, "", **config)
        self.add_defaults(KeyboardKbdd.defaults)
        self.keyboard = self.configured_keyboards[0]
        self.layout_index=0
        self.is_kbdd_running = self._check_kbdd()
        if not self.is_kbdd_running:
            self.keyboard = "N/A"
        self.add_callbacks(
            {
                "Button1": self.change_layout,
                "Button2": self.change_layout,
            }
        )

    def _check_kbdd(self):
        try:
            running_list = self.call_process(["ps", "axw"])
        except FileNotFoundError:
            logger.error("'ps' is not installed. Cannot check if kbdd is running.")
            return False

        if re.search("kbdd", running_list):
            self.keyboard = self.configured_keyboards[0]
            return True

        logger.error("kbdd is not running.")
        return False

    async def _config_async(self):
        subscribed = await add_signal_receiver(
            self._signal_received,
            session_bus=True,
            signal_name="layoutChanged",
            dbus_interface="ru.gentoo.kbdd",
        )

        if not subscribed:
            logger.warning("Could not subscribe to kbdd signal.")

    def _signal_received(self, message):
        if message.message_type != MessageType.SIGNAL:
            return

        self._layout_changed(*message.body)
        logger.warning("Signal")

    def _layout_changed(self, layout_changed):
        """
        Handler for "layoutChanged" dbus signal.
        """
        if self.colours:
            self._set_colour(layout_changed)
        self.layout_index=layout_changed
        self.keyboard = self.configured_keyboards[layout_changed]

    def _set_colour(self, index):
        if isinstance(self.colours, list):
            try:
                self.layout.colour = self.colours[index]
            except IndexError:
                self._set_colour(index - 1)
        else:
            logger.error(
                'variable "colours" should be a list, to set a\
                            colour for all layouts, use "foreground".'
            )

    def poll(self):
        if not self.is_kbdd_running:
            if self._check_kbdd():
                self.is_kbdd_running = True
                return self.configured_keyboards[0]
        return self.keyboard
