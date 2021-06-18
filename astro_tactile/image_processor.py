#image manipulation
from skimage import data, io, exposure, filters, restoration, morphology, transform

class ImageProcessor:
    def __init__(self):
        self.__queue = []
        self.input_data = None
        self.output_data = None

    def get_input(self):
        return self.input_data.copy()

    def set_input(self, data):
        self.input_data = data
        return

    def add_process(self, proc, index=None):
        if index is None:
            self.__queue.append(proc)
        else:
            self.__queue.insert(index, proc)
        return

    def process(self):
        temp_data = self.get_input()
        for proc in self.__queue:
            temp_data = proc.apply(temp_data)
        self.output_data = temp_data
        return self.output_data

class Process:
    def __init__(self, proc_fun, vars):
        self.__proc_fun = proc_fun
        self.__vars = vars

    def set_vars(self, vars, index=None):
        if index is None:
            self.__vars = vars
        else:
            self.__vars[index] = vars
        return

    def get_vars(self):
        return self.__vars.copy()

    def apply(self, data):
        return self.__proc_fun(data, self.__vars)

class EqualHist(Process):
    #equalize histogram
    def __init__(self, nbins=None):
        super().__init__(self.equal_hist, nbins)

    def equal_hist(self, data, nbins):
        if nbins is None:
            return exposure.equalize_hist(data)
        else:
            return exposure.equalize_hist(data, nbins)

# gamma correction
def gamma_corr(data, gamma):
    return exposure.adjust_gamma(data, gamma)

# log correction
def log_corr(data, gain):
    return exposure.adjust_log(data, gain)

# chop
def chop(data, floor = None, ceil = None):
    if not floor is None:
        mask = data < floor
        data[mask] = floor
    if not ceil is None:
        mask = data > ceil
        data[mask] = ceil
    return data

# denoise
def denoise(data, weight):
    return restoration.denoise_tv_chambolle(data, weight)


# tophat filter star removal
def destar(data, radius):
    selem = morphology.disk(radius)
    res = morphology.white_tophat(data, selem)
    return data - res
