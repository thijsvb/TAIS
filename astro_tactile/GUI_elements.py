import wx
from image_processor import *

class ProcessingUI:
    def __init__(self, tais, parent, img_proc=None):
        self.tais = tais
        self.parent_box = parent
        if img_proc is None:
            img_proc = ImageProcessor()
        self.processor = img_proc
        self.InitUI()

    def InitUI(self):
        self.parent_box.Clear(True)
        title = wx.StaticText(self.tais.main_panel, label="Processing")
        title.SetFont(self.tais.bold_font)
        title.SetHelpText("Image processing queue")
        self.parent_box.Add(title)

        for i, proc in enumerate(self.processor.queue):
            proc_box = ProcessUI(self.tais, self, proc, i)
            self.parent_box.Add((-1,10))

        add_btn = wx.Button(self.tais.main_panel, label='Add process')
        add_btn.Bind(wx.EVT_BUTTON, self.add_process_btm)
        self.parent_box.Add(add_btn, flag=wx.TOP, border=10)
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
        self.panel = wx.Panel(self.tais.main_panel, style=wx.SIMPLE_BORDER)
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

        cb = wx.ComboBox(self.panel, value=self.__types[self.__process.type], choices=list(self.__types.values()), style=wx.CB_READONLY)
        cb.Bind(wx.EVT_COMBOBOX, self.change_type)
        self.box.Add(cb, wx.RIGHT, border=10)



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
        self.__process.set_type(type)
        self.__processing_ui.InitUI()

    def remove(self, e):
        self.__processing_ui.processor.queue.pop(self.__queue_index)
        self.__processing_ui.InitUI()
