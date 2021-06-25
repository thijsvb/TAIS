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

APP_EXIT, OPEN_FILE = 1, 2

class TAIS(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(TAIS, self).__init__(*args, **kwargs)
        self.Maximize(True)

        self.loaded_fits = None

        self.font = wx.Font(wx.FontInfo())
        self.bold_font = wx.Font(wx.FontInfo().Bold())

        self.InitUI()
        # Test Data & Processing
        # imgproc = ImageProcessor()
        # imgproc.add_process(Process("equal_hist"))
        # imgproc.add_process(Process("gamma_corr", 3))
        # imgproc.add_process(Process("log_corr",3.0))
        # imgproc.add_process(Process("chop", [True, True, 0, 100]))
        # imgproc.add_process(Process("denoise", 0.1))
        # imgproc.add_process(Process("destar", 1))

        self.processing = ProcessingUI(self)
        self.image_preview = ImagePreviewUI(self)

    def InitUI(self):
        # Menu
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        qmi = wx.MenuItem(fileMenu, APP_EXIT, '&Quit\tCtrl+Q')
        fileMenu.Append(qmi)
        omi = wx.MenuItem(fileMenu, OPEN_FILE, "&Open\tCtrl+O")
        fileMenu.Append(omi)

        self.Bind(wx.EVT_MENU, self.OnQuit, id=APP_EXIT)
        self.Bind(wx.EVT_MENU, self.OnOpen, id=OPEN_FILE)

        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        # Layout
        self.main_panel = wx.Panel(self)
        self.main_panel.SetBackgroundColour("#e0e0ff")

        self.main_hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.img_panel = wx.Panel(self.main_panel)
        self.img_panel.SetLabel("Image Preview")
        self.img_vbox = wx.BoxSizer(wx.VERTICAL)
        st1 = wx.StaticText(self.img_panel, label="Image Preview")
        st1.SetFont(self.bold_font)
        self.img_vbox.Add(st1)
        self.img_panel.SetSizer(self.img_vbox)
        self.main_hbox.Add(self.img_panel, proportion=2, flag=wx.LEFT|wx.RIGHT, border=10)

        self.proc_panel = wx.Panel(self.main_panel)
        self.proc_panel.SetLabel("Processing queue")
        self.proc_vbox = wx.BoxSizer(wx.VERTICAL)
        self.proc_panel.SetSizer(self.proc_vbox)
        self.main_hbox.Add(self.proc_panel, proportion=1, flag=wx.LEFT|wx.RIGHT, border=10)

        self.mod_panel = wx.Panel(self.main_panel)
        self.mod_panel.SetLabel("Model settings")
        self.mod_vbox = wx.BoxSizer(wx.VERTICAL)
        st3 = wx.StaticText(self.mod_panel, label="Model settings")
        st3.SetFont(self.bold_font)
        self.mod_vbox.Add(st3)
        self.mod_panel.SetSizer(self.mod_vbox)
        self.main_hbox.Add(self.mod_panel, proportion=1, flag=wx.LEFT|wx.RIGHT, border=10)

        self.main_panel.SetSizer(self.main_hbox)

        self.SetTitle('Tactile Astronomical Imaging System')
        self.Centre()

    def OnQuit(self, e):
        self.Close()

    def OnOpen(self, e):
        with wx.FileDialog(self, "Open FITS file", wildcard="FITS files (*.fits)|*.fits",
                             style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            try:
                with fits.open(pathname) as file:
                    self.load_fits(file)
            except IOError:
                wx.LogError("Cannot open file " + pathname)

    def load_fits(self, fits_file):
        self.loaded_fits = fits_file
        data = fits_file[0].data
        self.processing.processor.set_input(data)
        self.image_preview.plots_panel.draw(data)

def main():
    app = wx.App()
    tais = TAIS(None)
    tais.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
