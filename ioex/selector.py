#!/usr/bin/env python

import os
import curses
import curses.textpad
import curses.wrapper
import locale
import pprint
import textwrap

KEY_ESC = 27
KEY_SDOWN = 336
KEY_SUP = 337

class Node(object):

    def __init__(self):
        self._parent = None
        self._children = []
        self._selected = False
        pass

    def child_count(self):
        return len(self._children)

    def find_root(self):
        if self._parent is None:
            return self
        else:
            return self._parent.find_root()

    def find_selected(self):
        selected_nodes = []
        if self.selected():
            selected_nodes.append(self)
        for child in self.get_children():
            selected_nodes = selected_nodes + child.find_selected()
        return selected_nodes

    def get_label(self, active_root):
        return ''

    def _clear_children(self):
        self._children = []

    def get_children(self):
        return self._children

    def _append_child(self, child):
        child._parent = self
        self._children.append(child)

    def get_header_height(self):
        return 0

    def select(self):
        self._selected = True

    def unselect(self):
        self._selected = False

    def toggle(self):
        if self.selected():
            self.unselect()
        else:
            self.select()

    def selected(self):
        return self._selected

class StaticNode(Node):

    def __init__(self, label):
        super(StaticNode, self).__init__()
        self.label = label

    def append_child(self, child):
        self._append_child(child)

    def get_label(self):
        return self.label

class SelectionPad(object):

    def __init__(self, parent_window):
        self._pad = curses.newpad(1, 1)
        self._pad.keypad(1)

    def refresh(self, pminrow, sminrow, smaxrow, smaxcol):
        # window.refresh([pminrow, pmincol, sminrow, smincol, smaxrow, smaxcol])
        #   pminrow and pmincol specify the upper left-hand corner of the rectangle to be displayed in the pad.
        #   sminrow, smincol, smaxrow, and smaxcol specify the edges of the rectangle to be displayed on the screen.
        #   The lower right-hand corner of the rectangle to be displayed in the pad is calculated from the screen coordinates, since the rectangles must be the same size.
        self._pad.refresh(pminrow, 0, sminrow, 0, smaxrow, smaxcol)

    def addstr(self, line_index, col_index, text, attr = 0):
        text_encoded = text.encode(locale.getpreferredencoding())
        try:
            self._pad.addstr(line_index, col_index, text_encoded, attr)
        except Exception, ex:
            raise Exception('pad(width=%d, height=%d).addstr(%d, %d, %s, %d) failed'
                    % (self.get_width(), self.get_height(), line_index, col_index, repr(text_encoded), attr))

    def clear(self):
        self._pad.clear()

    def get_height(self):
        return self._pad.getmaxyx()[0]

    def get_width(self):
        return self._pad.getmaxyx()[1]

    def getch(self):
        return self._pad.getch()

    def resize(self, nlines, ncols):
        try:
            self._pad.resize(nlines, ncols)
        except Exception, ex:
            raise Exception('pad(width=%d, height=%d).resize(%d, %d) failed'
                    % (self.get_width(), self.get_height(), nlines, ncols))

    def resize_height(self, nlines):
        self.resize(nlines, self.get_width())

    def resize_width(self, ncols):
        self.resize(self.get_height(), ncols)

def select(stdscr, active_root, multiple = False):

    curses.curs_set(0)
    pad = SelectionPad(stdscr)

    active_index = 0

    def get_screen_height():
        return stdscr.getmaxyx()[0]

    def get_active_node():
        return active_root.get_children()[active_index]

    def get_visible_pad_height():
        return get_screen_height() - active_root.get_header_height()

    def refresh():
        pad.clear()
        pad.resize_width(1)
        if len(active_root.get_children()) > 0:
            pad.resize_height(active_root.child_count())
            for child_index in range(len(active_root.get_children())):
                child = active_root.get_children()[child_index]
                label = child.get_label()
                # if the last line is the longest addstr() fails if
                # the width does not include one additional char.
                if len(label) > pad.get_width():
                    pad.resize_width(len(label) + 1)
                pad.addstr(
                    child_index,
                    0,
                    label,
                    (curses.A_UNDERLINE if child_index == active_index else 0)
                        | (curses.A_BOLD if child.selected() else 0)
                    )
            pad.refresh(
                max(
                    0,
                    min(
                        active_root.child_count() - get_visible_pad_height(),
                        active_index - int(get_visible_pad_height() / 2)
                        )
                    ),
                active_root.get_header_height(),
                get_screen_height() - 1,
                stdscr.getmaxyx()[1] - 1
                )

    while True:
        refresh()
        try:
            key = pad.getch()
        except KeyboardInterrupt:
            return None
        if key == curses.KEY_RESIZE:
            refresh()
        elif key in [curses.KEY_DOWN, KEY_SDOWN, ord('j'), ord('J')]:
            if multiple and key in [KEY_SDOWN, ord('J')]:
                get_active_node().toggle()
            active_index = min(active_root.child_count() - 1, active_index + 1)
        elif key in [curses.KEY_UP, KEY_SUP, ord('k'), ord('K')]:
            if multiple and key in [KEY_SUP, ord('K')]:
                get_active_node().toggle()
            active_index = max(0, active_index - 1)
        elif key == curses.KEY_NPAGE:
            active_index = min(active_root.child_count() - 1, active_index + int(get_visible_pad_height() / 2))
        elif key == curses.KEY_PPAGE:
            active_index = max(0, active_index - int(get_visible_pad_height() / 2))
        elif key in [ord(' ')]:
            if multiple:
                get_active_node().toggle()
            else:
                get_active_node().select()
                return active_root.find_root().find_selected()
        elif key in [ord('\n')]:
            get_active_node().select()
            return active_root.find_root().find_selected()
        elif key == KEY_ESC:
            return None
        else:
            raise Exception(key)

def select_string(stdscr, strings, multiple = False):
    root = StaticNode('root')
    for string in strings:
        root.append_child(StaticNode(string))
    selection = select(stdscr, root, multiple = multiple)
    if selection is None:
        return None
    else:
        return [n.get_label() for n in selection]
