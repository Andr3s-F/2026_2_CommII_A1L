"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    """Bloque Acumulador Continuo y Calculador de Estadisticas"""

    def __init__(self):
        gr.sync_block.__init__(
            self,
            name='e_Acum',  
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        self.acumulado = 0.0 
    def work(self, input_items, output_items):
        x = input_items[0]    
        y0 = output_items[0]  

        if len(x) > 0:
            
            y0[:] = self.acumulado + np.cumsum(x)
            self.acumulado = y0[-1]  

            
            media = np.mean(x)
            varianza = np.var(x)
            desviacion = np.std(x)

        return len(y0)  
