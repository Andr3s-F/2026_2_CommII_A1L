"""
Bloque de desviacion estandar (una sola salida).
Usa la identidad sigma^2 = E[x^2] - (E[x])^2
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):
    """Desviacion estandar acumulada"""

    def __init__(self):
        gr.sync_block.__init__(
            self,
            name='Desviacion_Despues',
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        self.acum_anterior = 0.0
        self.acum_anterior1 = 0.0
        self.Ntotales = 0

    def work(self, input_items, output_items):
        x = input_items[0]
        y0 = output_items[0]   # Desviacion estandar

        N = len(x)
        if N > 0:
            self.Ntotales += N

            acumulado = self.acum_anterior + np.cumsum(x)
            self.acum_anterior = acumulado[-1]
            media = acumulado / self.Ntotales

            x2 = np.multiply(x, x)
            acumulado1 = self.acum_anterior1 + np.cumsum(x2)
            self.acum_anterior1 = acumulado1[-1]
            media_cuad = acumulado1 / self.Ntotales

            y0[:] = np.sqrt(np.maximum(media_cuad - media ** 2, 0.0))

        return len(x)