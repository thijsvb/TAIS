#image manipulation
from skimage import data, io, exposure, filters, restoration, morphology, transform

class ImageProcessor:
    def __init__(self):
        self.queue = []
        self.input_data = None
        self.output_data = None

    def get_input(self):
        return self.input_data.copy()

    def set_input(self, data):
        self.input_data = data
        return

    def add_process(self, proc, index=None):
        if index is None:
            self.queue.append(proc)
        else:
            self.queue.insert(index, proc)
        return

    def process(self):
        if self.input_data is None:
            print("Error: No data given.")
            return

        temp_data = self.get_input()
        for proc in self.queue:
            temp_data = proc.apply(temp_data)
        self.output_data = temp_data
        return self.output_data

class Process:
    def __init__(self, type, vars=None):
        self.__procs = {
            "equal_hist": self.__equal_hist,
            "gamma_corr": self.__gamma_corr,
            "log_corr": self.__log_corr,
            "chop": self.__chop,
            "denoise": self.__denoise,
            "destar": self.__destar}

        self.__def_vars = {
            "equal_hist": 256,
            "gamma_corr": 1,
            "log_corr": 1,
            "chop": [False, False, -500, 12500],
            "denoise": 0.1,
            "destar": 1}

        self.type = type
        self.__proc_fun = self.__procs[type]
        if vars is None:
            vars = self.__def_vars[type]
        self.__vars = vars

    def set_type(self, type):
        self.__init__(type, None)

    def set_vars(self, vars, index=None):
        if index is None:
            self.__vars = vars
        else:
            self.__vars[index] = vars
        return

    def get_vars(self, index=None):
        if index is None:
            return self.__vars
        else:
            return self.__vars[index]

    def apply(self, data):
        return self.__proc_fun(data, self.__vars)

    def __equal_hist(self, data, nbins):
        return exposure.equalize_hist(data, nbins)

    def __gamma_corr(self, data, gamma):
        return exposure.adjust_gamma(data, gamma)

    def __log_corr(self, data, gain):
        return exposure.adjust_log(data, gain)

    def __chop(self, data, vars):
        floor_on, ceil_on, floor, ceil = vars
        if floor_on:
            mask = data < floor
            data[mask] = floor
        if ceil_on:
            mask = data > ceil
            data[mask] = ceil
        return data

    def __denoise(self, data, weight):
        return restoration.denoise_tv_chambolle(data, weight)

    def __destar(self, data, radius):
        selem = morphology.disk(radius)
        res = morphology.white_tophat(data, selem)
        return data - res
