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
#GUI elements class
from GUI_elements import *

APP_EXIT = 1

class TAIS(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(TAIS, self).__init__(size=(800, 600), *args, **kwargs)

        # self.font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        # self.bold_font = self.font.Bold()
        self.font = wx.Font(wx.FontInfo())
        self.bold_font = wx.Font(wx.FontInfo().Bold())

        self.InitUI()
        # Test Data & Processing
        imgproc = ImageProcessor()
        imgproc.add_process(Process("equal_hist"))
        imgproc.add_process(Process("gamma_corr", 3))
        imgproc.add_process(Process("log_corr",3))
        imgproc.add_process(Process("chop", [1, 100]))
        imgproc.add_process(Process("denoise", 0.1))
        imgproc.add_process(Process("destar", 1))
        self.processing = ProcessingUI(self, self.proc_vbox, imgproc)

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
        self.main_panel = wx.Panel(self)
        self.main_panel.SetBackgroundColour("#e0e0ff")

        self.main_hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.img_vbox = wx.BoxSizer(wx.VERTICAL)
        st1 = wx.StaticText(self.main_panel, label="Image Preview")
        st1.SetFont(self.bold_font)
        self.img_vbox.Add(st1)
        self.main_hbox.Add(self.img_vbox, proportion=2, flag=wx.LEFT|wx.RIGHT, border=10)

        self.proc_vbox = wx.BoxSizer(wx.VERTICAL)
        self.main_hbox.Add(self.proc_vbox, proportion=1, flag=wx.LEFT|wx.RIGHT, border=10)

        self.mod_vbox = wx.BoxSizer(wx.VERTICAL)
        st3 = wx.StaticText(self.main_panel, label="Model")
        st3.SetFont(self.bold_font)
        self.mod_vbox.Add(st3)
        self.main_hbox.Add(self.mod_vbox, proportion=1, flag=wx.LEFT|wx.RIGHT, border=10)

        self.main_panel.SetSizer(self.main_hbox)

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
