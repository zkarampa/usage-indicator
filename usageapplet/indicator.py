import signal

import gi
import logging

from usageapplet.giffgaffClient import GiffgaffClient
from usageapplet.utils import kibibytes_to

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import AppIndicator3, Gtk, GLib


class DataUsageIndicator:
    def __init__(self, usage_applet):
        self.app = usage_applet
        self.indicator = AppIndicator3.Indicator.new(
            self.app.name,
            "gsm-3g-full",
            AppIndicator3.IndicatorCategory.COMMUNICATIONS
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())

        self.update_value()
        GLib.timeout_add_seconds(30, self.update_value)

    def build_menu(self):
        menu = Gtk.Menu()

        item = Gtk.MenuItem()
        item.set_label("Configuration")
        item.connect("activate", self.app.conf_win.cb_show, '')
        menu.append(item)

        item = Gtk.MenuItem()
        item.set_label("Exit")
        item.connect("activate", self.app.cb_exit)
        menu.append(item)

        menu.show_all()
        return menu

    def update_value(self):
        data = self.app.client.get_data_allowance()
        self.indicator.set_label(self.calculate_output(data["left"], data["max"]), "")
        return True

    def calculate_output(self, data_left, data_max):
        return "%.2f/%.2f GB" % (kibibytes_to(data_left), kibibytes_to(data_max))


class ConfigWindow(Gtk.Window):
    def __init__(self, root):
        super(ConfigWindow, self).__init__()
        self.app = root
        self.set_title(self.app.name + ' Config Window')

    def cb_show(self, w, data):
        self.show()


class UsageApplet(Gtk.Application):
    def __init__(self, app_name, username, password):
        super(UsageApplet, self).__init__()
        self.name = app_name
        self.client = GiffgaffClient(username, password)
        self.conf_win = ConfigWindow(self)
        self.indicator = DataUsageIndicator(self)

    def run(self):
        Gtk.main()

    def cb_exit(self):
        Gtk.main_quit()


def main():
    # logging.basicConfig(filename='myIndicator.log', level=logging.DEBUG)
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    username = ""
    password = ""
    app = UsageApplet('giffgaff data indicator', username, password)
    app.run()


if __name__ == "__main__":
    main()
