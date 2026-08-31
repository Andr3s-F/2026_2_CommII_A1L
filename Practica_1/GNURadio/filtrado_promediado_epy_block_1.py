import numpy as np
from gnuradio import gr


class blk(gr.sync_block):
    """Promediador movil de N muestras"""

    def __init__(self, N=16):
        gr.sync_block.__init__(
            self,
            name='Promediador_Movil',
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        self.N = int(N)
        # set_history pide N-1 muestras del bloque anterior,
        # para que la ventana no se corte entre llamadas a work().
        self.set_history(self.N)

    def work(self, input_items, output_items):
        x = input_items[0]
        y0 = output_items[0]
        ventana = np.ones(self.N) / self.N
        y0[:] = np.convolve(x, ventana, mode='valid')
        return len(y0)