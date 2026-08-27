"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    """Bloque Acumulador y Calculador de Estadisticas"""

    def __init__(self):
        gr.sync_block.__init__(
            self,
            name='Acumulador y Estadistica',
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        self.acumulado = 0.0

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]

        # 1. Acumulador (Suma consecutiva de muestras)
        for i in range(len(in0)):
            self.acumulado += in0[i]
            out[i] = self.acumulado

        # 2. Medidas Estadísticas (Media, Varianza y Desviación Estándar)
        if len(in0) > 0:
            media = np.mean(in0)
            varianza = np.var(in0)
            desviacion = np.std(in0)
            #print(f"[ESTADISTICAS] Media: {media:.2f} | Varianza: {varianza:.2f} | Desv. Est: {desviacion:.2f}")

        return len(output_items[0])
