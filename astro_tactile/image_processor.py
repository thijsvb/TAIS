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
        temp_data = self.get_input()
        for proc in self.queue:
            temp_data = proc.apply(temp_data)
        self.output_data = temp_data
        return self.output_data

class Process:
    def __init__(self, type, vars=None):
        procs = {
            "equal_hist": self.__equal_hist,
            "gamma_corr": self.__gamma_corr,
            "log_corr": self.__log_corr,
            "chop": self.__chop,
            "denoise": self.__denoise,
            "destar": self.__destar}

        def_vars = {
            "equal_hist": 256,
            "gamma_corr": 1,
            "log_corr": 1,
            "chop": [None, None],
            "denoise": 0.1,
            "destar": 1}

        self.type = type
        self.__proc_fun = procs[type]
        if vars is None:
            vars = def_vars[type]
        self.__vars = vars

    def set_type(self, type):
        self.__init__(type)

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

    def __equal_hist(self, data, nbins):
        return exposure.equalize_hist(data, nbins)

    def __gamma_corr(self, data, gamma):
        return exposure.adjust_gamma(data, gamma)

    def __log_corr(self, data, gain):
        return exposure.adjust_log(data, gain)

    def __chop(self, data, vars):
        floor, ceil = vars
        if not floor is None:
            mask = data < floor
            data[mask] = floor
        if not ceil is None:
            mask = data > ceil
            data[mask] = ceil
        return data

    def __denoise(self, data, weight):
        return restoration.denoise_tv_chambolle(data, weight)

    def __destar(self, data, radius):
        selem = morphology.disk(radius)
        res = morphology.white_tophat(data, selem)
        return data - res

# class EqualHist(Process):
#     #equalize histogram
#     def __init__(self, nbins=None):
#         super().__init__(self.equal_hist, nbins)
#
#     def equal_hist(self, data, nbins):
#         if nbins is None:
#             return exposure.equalize_hist(data)
#         else:
#             return exposure.equalize_hist(data, nbins)
#
# class GammaCorr(Process):
#     # gamma correction
#     def __init__(self, gamma):
#         super().__init__(self.gamma_corr, gamma)
#
#     def gamma_corr(self, data, gamma):
#         return exposure.adjust_gamma(data, gamma)
#
# class LogCorr(Process):
#     # log correction
#     def __init__(self, gain):
#         super().__init__(self.log_corr, gain)
#
#     def log_corr(self, data, gain):
#         return exposure.adjust_log(data, gain)
#
# class Chop(Process):
#     # chop
#     def __init__(self, floor=None, ceil=None):
#         super().__init__(self.chop, [floor, ceil])
#
#     def chop(self, data, vars):
#         floor, ceil = vars
#         if not floor is None:
#             mask = data < floor
#             data[mask] = floor
#         if not ceil is None:
#             mask = data > ceil
#             data[mask] = ceil
#         return data
#
# class Denoise(Process):
#     # denoise
#     def __init__(self, weight):
#         super().__init__(self.denoise, weight)
#
#     def denoise(self, data, weight):
#         return restoration.denoise_tv_chambolle(data, weight)
#
# class Destar(Process):
#     # tophat filter star removal
#     def __init__(self, radius):
#         super().__init__(self.destar, radius)
#
#     def destar(self, data, radius):
#         selem = morphology.disk(radius)
#         res = morphology.white_tophat(data, selem)
#         return data - res
