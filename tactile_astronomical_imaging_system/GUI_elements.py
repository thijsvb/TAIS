import wx
from image_processor import *
import sys

class ProcessingUI:
    def __init__(self, tais, img_proc=None):
        self.tais = tais
        self.parent_box = tais.proc_vbox
        self.parent_panel = tais.proc_panel
        if img_proc is None:
            img_proc = ImageProcessor()
        self.processor = img_proc
        self.InitUI()

    def InitUI(self):
        self.parent_box.Clear(True)
        title = wx.StaticText(self.parent_panel, label="Processing queue")
        title.SetFont(self.tais.bold_font)
        title.SetHelpText("Image processing queue")
        self.parent_box.Add(title)

        for i, proc in enumerate(self.processor.queue):
            proc_box = ProcessUI(self.tais, self, proc, i)
            self.parent_box.Add((-1,10))

        add_btn = wx.Button(self.parent_panel, label='Add process')
        add_btn.Bind(wx.EVT_BUTTON, self.add_process_btm)
        self.parent_box.Add(add_btn)
        self.parent_box.Add((-1,10))

        app_btn = wx.Button(self.parent_panel, label = "Apply processing")
        app_btn.Bind(wx.EVT_BUTTON, self.apply_processing)
        self.parent_box.Add(app_btn)

        self.tais.main_panel.Layout()
        self.tais.main_hbox.Layout()

    def add_process_btm(self, e):
        self.add_process()

    def add_process(self, index=None):
        if index is None:
            self.processor.add_process(Process("equal_hist"))
        else:
            self.processor.add_process(Process("equal_hist"), index)
        self.InitUI()

    def apply_processing(self, e):
        data = self.processor.process()
        self.tais.image_preview.plots_panel.draw(data)

class ProcessUI:
    def __init__(self, tais, parent, proc, i):
        self.tais = tais
        self.__processing_ui = parent
        self.__process = proc
        self.__queue_index = i

        self.__types ={"equal_hist": "Equalize histogram",
                       "gamma_corr": "Gamma correction",
                       "log_corr": "Log correction",
                       "chop": "Chop",
                       "denoise": "Total-variation denoising",
                       "destar": "Remove forground stars"}

        self.InitUI()

    def InitUI(self):
        self.box = wx.BoxSizer(wx.HORIZONTAL)
        self.panel = wx.Panel(self.__processing_ui.parent_panel, style=wx.SIMPLE_BORDER)
        self.panel.SetBackgroundColour("#ffffff")
        self.panel.SetLabel("Process: "+self.__types[self.__process.type])
        self.__processing_ui.parent_box.Add(self.panel)

        arrow_box = wx.BoxSizer(wx.VERTICAL)
        up = wx.Button(self.panel, label='Move up')
        up.Bind(wx.EVT_BUTTON, self.move_up)
        arrow_box.Add(up)
        down = wx.Button(self.panel, label='Move down')
        down.Bind(wx.EVT_BUTTON, self.move_down)
        arrow_box.Add(down)
        self.box.Add(arrow_box, wx.RIGHT, border=10)

        cb_panel = wx.Panel(self.panel)
        cb_panel.SetLabel("Type")
        cb_box = wx.BoxSizer(wx.HORIZONTAL)
        cb = wx.ComboBox(cb_panel, value=self.__types[self.__process.type], choices=list(self.__types.values()), style=wx.CB_READONLY)
        cb.Bind(wx.EVT_COMBOBOX, self.change_type)
        cb_box.Add(cb, wx.RIGHT, border=10)
        cb_panel.SetSizer(cb_box)
        self.box.Add(cb_panel)

        maxval = int(2**31-1)
        if self.__process.type == "equal_hist":
            nbins_panel, nbins_box = self.__var_setup("Number of bins")
            nbins = wx.SpinCtrl(nbins_panel, initial=self.__process.get_vars(), min=1, max=maxval)
            nbins.Bind(wx.EVT_SPINCTRL, self.__set_spinctrl_var)
            nbins_box.Add(nbins)
            nbins_panel.SetSizer(nbins_box)
            self.box.Add(nbins_panel)

        elif self.__process.type == "gamma_corr":
            gamma_panel, gamma_box = self.__var_setup("Gamma")
            gamma = wx.SpinCtrlDouble(gamma_panel, initial=self.__process.get_vars(), min=-maxval, max=maxval)
            gamma.SetDigits(2)
            gamma.SetLabel("Gamma")
            gamma.Bind(wx.EVT_SPINCTRLDOUBLE, self.__set_spinctrldouble_var)
            gamma_box.Add(gamma)
            gamma_panel.SetSizer(gamma_box)
            self.box.Add(gamma_panel)

        elif self.__process.type == "log_corr":
            gain_panel, gain_box = self.__var_setup("Gain")
            gain = wx.SpinCtrlDouble(gain_panel, initial=self.__process.get_vars(), min=-maxval, max=maxval)
            gain.SetDigits(2)
            gain.SetLabel("Gain")
            gain.Bind(wx.EVT_SPINCTRLDOUBLE, self.__set_spinctrldouble_var)
            gain_box.Add(gain)
            gain_panel.SetSizer(gain_box)
            self.box.Add(gain_panel)

        elif self.__process.type == "chop":
            chop_panel, chop_box = self.__var_setup("Chop")
            floor_ceil_box = wx.BoxSizer(wx.VERTICAL)

            ceil_box = wx.BoxSizer(wx.HORIZONTAL)
            ceil_toggle = wx.CheckBox(chop_panel, label="Ceil:")
            ceil_toggle.SetValue(self.__process.get_vars(1))
            ceil_toggle.Bind(wx.EVT_CHECKBOX, self.__toggle_ceil)
            ceil_box.Add(ceil_toggle, wx.RIGHT, border=5)
            ceil_val = wx.SpinCtrl(chop_panel, initial=self.__process.get_vars(3), min=-maxval, max=maxval)
            ceil_val.Bind(wx.EVT_SPINCTRL, self.__set_ceil)
            ceil_box.Add(ceil_val)
            floor_ceil_box.Add(ceil_box)

            floor_box = wx.BoxSizer(wx.HORIZONTAL)
            floor_toggle = wx.CheckBox(chop_panel, label="Floor:")
            floor_toggle.SetValue(self.__process.get_vars(0))
            floor_toggle.Bind(wx.EVT_CHECKBOX, self.__toggle_floor)
            floor_box.Add(floor_toggle, wx.RIGHT, border=5)
            floor_val = wx.SpinCtrl(chop_panel, initial=self.__process.get_vars(2), min=-maxval, max=maxval)
            floor_val.Bind(wx.EVT_SPINCTRL, self.__set_floor)
            floor_box.Add(floor_val)
            floor_ceil_box.Add(floor_box)
            chop_box.Add(floor_ceil_box)

            chop_panel.SetSizer(chop_box)
            self.box.Add(chop_panel)

        elif self.__process.type == "denoise":
            weight_panel, weight_box = self.__var_setup("Weight")
            weight = wx.SpinCtrlDouble(weight_panel, initial=self.__process.get_vars(), min=0, max=maxval, inc=0.01)
            weight.SetDigits(2)
            weight.SetLabel("Weight")
            weight.Bind(wx.EVT_SPINCTRLDOUBLE, self.__set_spinctrldouble_var)
            weight_box.Add(weight)
            weight_panel.SetSizer(weight_box)
            self.box.Add(weight_panel)

        elif self.__process.type == "destar":
            radius_panel, radius_box = self.__var_setup("Radius")
            radius = wx.SpinCtrl(radius_panel, initial=self.__process.get_vars(), min=1, max=maxval)
            radius.Bind(wx.EVT_SPINCTRL, self.__set_spinctrl_var)
            radius_box.Add(radius)
            radius_panel.SetSizer(radius_box)
            self.box.Add(radius_panel)

        rem = wx.Button(self.panel, label="Remove")
        rem.Bind(wx.EVT_BUTTON, self.remove)
        self.box.Add(rem)

        self.panel.SetSizer(self.box)

    def swap(self, i, j):
        self.__processing_ui.processor.queue[j], self.__processing_ui.processor.queue[i] = self.__processing_ui.processor.queue[i], self.__processing_ui.processor.queue[j]

    def move_up(self, e):
        if self.__queue_index == 0:
            return
        i = self.__queue_index
        j = i-1
        self.swap(i, j)
        self.__processing_ui.InitUI()

    def move_down(self, e):
        if self.__queue_index == len(self.__processing_ui.processor.queue)-1:
            return
        i = self.__queue_index
        j = i+1
        self.swap(i, j)
        self.__processing_ui.InitUI()

    def change_type(self, e):
        type = list(self.__types.keys())[list(self.__types.values()).index(e.GetString())]
        self.__processing_ui.processor.queue.pop(self.__queue_index)
        self.__processing_ui.processor.add_process(Process(type), self.__queue_index)
        # self.__process.set_type(type)
        self.__processing_ui.InitUI()

    def remove(self, e):
        self.__processing_ui.processor.queue.pop(self.__queue_index)
        self.__processing_ui.InitUI()

    def __var_setup(self, name):
        var_panel = wx.Panel(self.panel)
        var_panel.SetLabel(name)
        var_box = wx.BoxSizer(wx.HORIZONTAL)
        st = wx.StaticText(var_panel, label=name+':')
        st.SetFont(self.tais.font)
        var_box.Add(st, wx.RIGHT, border=10)
        return (var_panel, var_box)

    def __set_spinctrl_var(self, e):
        self.__process.set_vars(e.GetPosition())

    def __set_spinctrldouble_var(self, e):
        self.__process.set_vars(e.GetValue())

    def __toggle_floor(self, e):
        self.__process.set_vars(e.IsChecked(), 0)

    def __set_floor(self, e):
        self.__process.set_vars(e.GetPosition(), 2)

    def __toggle_ceil(self, e):
        self.__process.set_vars(e.IsChecked(), 1)

    def __set_ceil(self, e):
        self.__process.set_vars(e.GetPosition(), 3)

class ImagePreviewUI:
    def __init__(self, tais):
        self.tais = tais
        self.parent_box = tais.img_vbox
        self.parent_panel = tais.img_panel
        self.InitUI()

    def InitUI(self):
        self.plots_panel = CanvasPanel(self.parent_panel)
        self.parent_box.Add(self.plots_panel, wx.EXPAND)
        self.parent_box.Add((-1,10))

        reset = wx.Button(self.parent_panel, label="Reset to input data")
        reset.Bind(wx.EVT_BUTTON, self.reset_plots)
        self.parent_box.Add(reset)

    def reset_plots(self, e):
        data = self.tais.processing.processor.input_data
        self.plots_panel.draw(data)

import matplotlib
matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx as NavigationToolbar
from matplotlib.figure import Figure

class CanvasPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.figure = Figure(figsize=(4,6))
        self.im_axes = self.figure.add_subplot(2, 1, 1)
        self.hg_axes = self.figure.add_subplot(2, 1, 2)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.toolbar = NavigationToolbar(self.canvas)
        self.toolbar.Realize()
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.EXPAND)
        self.sizer.Add(self.toolbar, 0, wx.LEFT | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()

    def draw(self, data):
        if data is None:
            return

        self.figure.clear()
        self.im_axes = self.figure.add_subplot(2, 1, 1)
        self.hg_axes = self.figure.add_subplot(2, 1, 2)
        ims = self.im_axes.imshow(data, cmap="Greys_r")
        self.figure.colorbar(ims, ax=self.im_axes)
        self.hg_axes.hist(data.flatten(), bins=256)
        self.canvas.draw()

from data_to_stl import *
from stl import mesh

class ModelUI:
    def __init__(self, tais):
        self.tais = tais
        self.parent_box = tais.mod_vbox
        self.parent_panel = tais.mod_panel

        self.InitUI()

    def InitUI(self):
        maxval = int(2**31-1)
        size_panel, size_box = self.__var_setup("Model size (x,y in mm)")
        self.xsize = wx.SpinCtrl(size_panel, initial=50, min=1, max=maxval)
        self.xsize.Bind(wx.EVT_SPINCTRL, self.set_sizex)
        size_box.Add(self.xsize)
        self.ysize = wx.SpinCtrl(size_panel, initial=50, min=1, max=maxval)
        self.ysize.Bind(wx.EVT_SPINCTRL, self.set_sizey)
        size_box.Add(self.ysize)
        size_panel.SetSizer(size_box)
        self.parent_box.Add(size_panel)

        self.size_prop = wx.CheckBox(self.parent_panel, label="Size proportional to data")
        self.size_prop.SetValue(True)
        self.size_prop.Bind(wx.EVT_CHECKBOX, self.set_sizex)
        self.parent_box.Add(self.size_prop)

        zheight_panel, zheight_box = self.__var_setup("Z height in mm")
        self.zheight = wx.SpinCtrlDouble(zheight_panel, initial=2, min=0.1, max=maxval, inc=0.1)
        self.zheight.SetDigits(1)
        self.zheight.SetLabel("Z height in mm")
        zheight_box.Add(self.zheight)
        zheight_panel.SetSizer(zheight_box)
        self.parent_box.Add(zheight_panel)

        bpheight_panel, bpheight_box = self.__var_setup("Baseplate height in mm")
        self.bpheight = wx.SpinCtrlDouble(bpheight_panel, initial=1, min=0.1, max=maxval, inc=0.1)
        self.bpheight.SetDigits(1)
        self.bpheight.SetLabel("Baseplate heigth in mm")
        bpheight_box.Add(self.bpheight)
        bpheight_panel.SetSizer(bpheight_box)
        self.parent_box.Add(bpheight_panel)

        make_btn = wx.Button(self.parent_panel, label="Make and save STL model")
        make_btn.Bind(wx.EVT_BUTTON, self.__make_model)
        self.parent_box.Add(make_btn)

    def __var_setup(self, name):
        var_panel = wx.Panel(self.parent_panel)
        var_panel.SetLabel(name)
        var_box = wx.BoxSizer(wx.HORIZONTAL)
        st = wx.StaticText(var_panel, label=name+':')
        st.SetFont(self.tais.font)
        var_box.Add(st, wx.RIGHT, border=10)
        return (var_panel, var_box)

    def set_sizex(self, e=None):
        if self.size_prop.IsChecked():
            if self.tais.loaded_fits is None:
                return
            datax, datay = self.tais.processing.processor.get_input().shape
            sizey = self.xsize.GetValue() * (datay/datax)
            sizey = round(sizey)
            self.ysize.SetValue(sizey)

    def set_sizey(self, e=None):
        if self.size_prop.IsChecked():
            if self.tais.loaded_fits is None:
                return
            datax, datay = self.tais.processing.processor.get_input().shape
            sizex = self.ysize.GetValue() * (datax/datay)
            sizex = round(sizex)
            self.xsize.SetValue(sizex)

    def __make_model(self, e):
        data = self.tais.processing.processor.output_data
        if data is None:
            return
        zsize = self.zheight.GetValue() + self.bpheight.GetValue()
        size = (self.xsize.GetValue(), self.ysize.GetValue(), zsize)
        mesh = data_to_stl(data, size, base_off=self.bpheight.GetValue())

        with wx.FileDialog(self.tais, "Save STL file", wildcard="STL files (*.stl)|*.stl",
                       style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # save the current contents in the file
            pathname = fileDialog.GetPath()
            try:
                mesh.save(pathname)
            except IOError:
                wx.LogError("Cannot save current data in file " + pathname)
