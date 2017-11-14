import sys,os
import curses


class Console():

    # Initialize colors in curses
    stdscr = curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    def __init__(self, stdscr):
        self._stdscr = stdscr
        self._stdscr.clear()
        self._stdscr.refresh()
        self.draw_borders()
        self.draw_stats_column()
        self.draw_alerts_column()
        self.status_bar()
        self._stdscr.refresh()

    def draw_borders(self):
        '''Draw borders of the different columns'''
        self._height, self._width = self._stdscr.getmaxyx()
        self._stdscr.border()
        self._stdscr.vline(1, int(3 * self._height / 4), '|', int(self._width - 2))
        self._stdscr.vline(1, int(self._height / 4), '|', int(self._width - 2))
        self._stdscr.refresh()

    def draw_stats_column(self):
        '''initialize the http monitor'''
        self._stats_column = curses.newwin(int(self._height - 2), int(self._width / 4 - 1), 1, 1)
        _, t_x = self._stats_column.getmaxyx()
        self._stats_column.setscrreg(3, self._height - 5)
        self._stats_column.idlok(True)
        self._stats_column.scrollok(True)
        self._stats_column.attron(curses.color_pair(1))
        self._stats_column.attron(curses.A_BOLD)
        self._stats_column.addstr(0, int(t_x / 2 - 4), "Monitor")
        self._stats_column.hline(1, 0, '-', t_x)

        self._stats_column.attroff(curses.color_pair(1))
        self._stats_column.attroff(curses.A_BOLD)

        self._stats_column.noutrefresh()

    def draw_alerts_column(self):
        '''Initialize the Alerts column'''
        self._alert_column = curses.newwin(int(self._height - 2), int(self._width / 4 - 1), 1,
                                     int( self._width / 2 + 1))
        _, s_x = self._alert_column.getmaxyx()
        self._alert_column.attron(curses.color_pair(1))
        self._alert_column.attron(curses.A_BOLD)
        self._alert_column.addstr(0, int(s_x / 2 - 5), "Alerts")
        self._alert_column.hline(1, 0, '-', s_x)
        self._alert_column.attron(curses.color_pair(1))
        self._alert_column.attron(curses.A_BOLD)
        self._alert_column.noutrefresh()

    def status_bar(self):
        # Declaration of strings
        statusbarstr = "Press 'q' to exit | STATUS BAR "
        self._stdscr.attron(curses.color_pair(3))
        self._stdscr.addstr(self._height - 1, 0, statusbarstr)
        self._stdscr.addstr(self._height - 1, len(statusbarstr), " " * (self._width - len(statusbarstr) - 1))
        self._stdscr.attroff(curses.color_pair(3))



if __name__ == "__main__":
    stdscr = curses.initscr()
    c = Console(stdscr)
