import gi
import signal
import logging
import datetime

from indicator.giffgaffClient import GiffgaffClient

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')

from gi.repository import AppIndicator3, Gtk, GLib


class MyIndicator:
    def __init__(self, root):
        self.app = root
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
        item.set_label("Main Window")
        item.connect("activate", self.app.main_win.cb_show, '')
        menu.append(item)

        item = Gtk.MenuItem()
        item.set_label("Configuration")
        item.connect("activate", self.app.conf_win.cb_show, '')
        menu.append(item)

        item = Gtk.MenuItem()
        item.set_label("Exit")
        item.connect("activate", cb_exit)
        menu.append(item)

        menu.show_all()
        return menu

    def update_value(self):
        self.indicator.set_label(get_allowance(self.app.giffgaff), "")
        return True


class MyConfigWin(Gtk.Window):
    def __init__(self, root):
        super(MyConfigWin, self).__init__()
        self.app = root
        self.set_title(self.app.name + ' Config Window')

    def cb_show(self, w, data):
        self.show()


class MyMainWin(Gtk.Window):
    def __init__(self, root):
        super(MyMainWin, self).__init__()
        self.app = root
        self.set_title(self.app.name)

    def cb_show(self, w, data):
        self.show()


class MyApp(Gtk.Application):

    scopes = "read"

    def __init__(self, app_name, username, password):
        super(MyApp, self).__init__()
        self.name = app_name
        self.giffgaff = GiffgaffClient(username, password, self.scopes)
        self.main_win = MyMainWin(self)
        self.conf_win = MyConfigWin(self)
        self.indicator = MyIndicator(self)


def get_allowance(giffgaff_cient):
    profile = giffgaff_cient.get_profile()
    data_left = profile.json()['current_goodybag']['data_left']
    data_max = profile.json()['current_goodybag']['data_max']
    data_left_amount = profile.json()['current_goodybag']['data_left_amount']
    data_max_amount = profile.json()['current_goodybag']['data_max_amount']

    logging.info("Time: %s", datetime.datetime.now())
    logging.info("data_left: %s, data_left_amount: %s", data_left, data_left_amount)

    result = calculate_output(data_left, data_max)
    logging.info("result: %s", result)
    return result


def calculate_output(data_left, data_max):
    return "%.2f/%.2f GB" % (human_readable(data_left), human_readable(data_max))


def human_readable(data):
    return float(data) / float(1024*1024)


def run():
    Gtk.main()


def cb_exit(_):
    Gtk.main_quit()


if __name__ == '__main__':
    logging.basicConfig(filename='myIndicator.log', level=logging.DEBUG)
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    username = ""
    password = ""

    app = MyApp('giffgaff data indicator', username,password)
    run()
