
import femm
import os
from myfemm.geo import Point
import numpy
import matplotlib.pyplot as plt

os.chdir('src/feladat3')
femm.openfemm()
femm.opendocument('feladat3.fem')

freqs = [100, 1000, 10**4, 25*10**3]

middle_circle_top = Point(0, 0)
middle_circle_bottom = Point(0, -4)

def get_current_densities(xcoords, ycoords):
    curr_densities = []
    for x, y in zip(xcoords, ycoords):
        pointvalues = femm.mo_getpointvalues(x, y)
        eddy_curr_dens = pointvalues[7]
        source_curr_dens = pointvalues[8]
        curr_density = eddy_curr_dens + source_curr_dens
        curr_densities.append(curr_density)
    return curr_densities


if __name__ == "__main__":
    for freq in freqs:
        femm.mi_probdef(freq, 'centimeters', 'planar', 1.e-8, 5, 30)
        femm.mi_analyze()
        femm.mi_loadsolution()

        resolution = 10000
        xcoords = numpy.linspace(middle_circle_top.x, middle_circle_bottom.x, resolution)
        ycoords = numpy.linspace(middle_circle_top.y, middle_circle_bottom.y, resolution)
        complex_curr_dens = get_current_densities(xcoords, ycoords)
        magnitudes = []
        real = []
        imag = []
        for curr_dens in complex_curr_dens:
            magnitudes.append(abs(curr_dens))
            real.append(curr_dens.real)
            imag.append(curr_dens.imag)
        
        plt.rcParams['axes.grid'] = True
        to_plot = {
            'Magnitude' : magnitudes,
            'Real' : real,
            'Imag' : imag
        }
        for (name, values), index in zip(to_plot.items(), [1, 2, 3]):
            ax = plt.subplot(3, 1, index)
            ax.set_title(name)
            ax.plot(ycoords, values, label = f'{freq} Hz')
            handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.5),
        fancybox=True, shadow=True, ncol=5)

    plt.tight_layout()
    plt.show()
    femm.closefemm()