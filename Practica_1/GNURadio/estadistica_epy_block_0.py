"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    """Bloque de Promedios de Tiempo Estadísticos"""

    def __init__(self):
        gr.sync_block.__init__(
            self,
            name='Promedios_de_tiempos',
            in_sig=[np.float32],
            out_sig=[np.float32, np.float32, np.float32, np.float32, np.float32]
        )
        self.acum_anterior = 0.0
        self.Ntotales = 0
        self.acum_anterior1 = 0.0
        self.acum_anterior2 = 0.0

    def work(self, input_items, output_items):
        x = input_items[0]
        y0 = output_items[0]  # Media
        y1 = output_items[1]  # Media Cuadrática
        y2 = output_items[2]  # RMS
        y3 = output_items[3]  # Potencia Promedio
        y4 = output_items[4]  # Desviación Estándar

        N = len(x)
        if N > 0:
            self.Ntotales += N

            # 1. Media
            acumulado = self.acum_anterior + np.cumsum(x)
            self.acum_anterior = acumulado[-1]
            y0[:] = acumulado / self.Ntotales

            # 2. Media Cuadrática
            x2 = np.multiply(x, x)
            acumulado1 = self.acum_anterior1 + np.cumsum(x2)
            self.acum_anterior1 = acumulado1[-1]  # Corrección de variable en la guía
            y1[:] = acumulado1 / self.Ntotales

            # 3. Valor RMS
            y2[:] = np.sqrt(y1)

            # 4. Potencia Promedio
            y3[:] = np.multiply(y2, y2)

            # 5. Desviación Estándar
            x3 = np.multiply(x - y0, x - y0)
            acumulado2 = self.acum_anterior2 + np.cumsum(x3)
            self.acum_anterior2 = acumulado2[-1]
            y4[:] = np.sqrt(acumulado2 / self.Ntotales)

        return len(x)



