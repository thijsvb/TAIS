#!/usr/bin/env python

#Imports:
#Numpy
import numpy as np
#Fits opening
from astropy.io import fits
#image processor class
from image_processor import *
#GUI
import wx

APP_EXIT = 1

class TAIS(wx.Frame, wx.Accessible):
    def __init__(self, *args, **kwargs):
        super(TAIS, self).__init__(*args, **kwargs)
        self.InitUI()

    def InitUI(self):
        # Menu
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        qmi = wx.MenuItem(fileMenu, APP_EXIT, '&Quit\tCtrl+Q')
        fileMenu.Append(qmi)

        self.Bind(wx.EVT_MENU, self.OnQuit, id=APP_EXIT)

        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        # Layout
        main_panel = wx.Panel(self)
        main_panel.SetBackgroundColour("#e0e0ff")

        main_hbox = wx.BoxSizer(wx.HORIZONTAL)

        img_vbox = wx.BoxSizer(wx.VERTICAL)
        st1 = wx.StaticText(main_panel, label="Image Preview")
        img_vbox.Add(st1)
        main_hbox.Add(img_vbox, proportion=2, flag=wx.LEFT|wx.RIGHT, border=10)

        proc_vbox = wx.BoxSizer(wx.VERTICAL)
        st2 = wx.StaticText(main_panel, label="Processing")
        proc_vbox.Add(st2)
        main_hbox.Add(proc_vbox, proportion=1, flag=wx.LEFT|wx.RIGHT, border=10)

        mod_vbox = wx.BoxSizer(wx.VERTICAL)
        st3 = wx.StaticText(main_panel, label="Model")
        mod_vbox.Add(st3)
        main_hbox.Add(mod_vbox, proportion=1, flag=wx.LEFT|wx.RIGHT, border=10)

        main_panel.SetSizer(main_hbox)

        self.SetTitle('Tactile Astronomical Imaging System')
        self.Centre()

    def OnQuit(self, e):
        self.Close()

def main():
    app = wx.App()
    tais = TAIS(None)
    tais.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
