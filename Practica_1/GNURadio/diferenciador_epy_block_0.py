"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    """Bloque Diferenciador Discreto: y[n] = x[n] - x[n-1]"""

    def __init__(self):
        gr.sync_block.__init__(
            self,
            name='e_Diff',        
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        self.x_anterior = 0.0     
    def work(self, input_items, output_items):
        x = input_items[0]       
        y0 = output_items[0]     

        if len(x) > 0:
           
            x_extendido = np.insert(x, 0, self.x_anterior)
            
            y0[:] = np.diff(x_extendido)
            
            self.x_anterior = x[-1]

        return len(y0)