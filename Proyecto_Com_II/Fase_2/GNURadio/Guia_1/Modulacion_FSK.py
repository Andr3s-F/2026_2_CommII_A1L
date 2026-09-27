#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Modulacion_FSK
# Description: FSK conceptual: envolvente compleja, PSD y frecuencia instantanea
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
import math
from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import sip
import threading



class Modulacion_FSK(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Modulacion_FSK", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Modulacion_FSK")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "Modulacion_FSK")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 100
        self.samp_rate = samp_rate = 1e6
        self.symbol_rate = symbol_rate = samp_rate/sps
        self.fsk_deviation = fsk_deviation = 20000

        ##################################################
        # Blocks
        ##################################################

        self._fsk_deviation_range = qtgui.Range(5000, 100000, 1000, 20000, 200)
        self._fsk_deviation_win = qtgui.RangeWidget(self._fsk_deviation_range, self.set_fsk_deviation, "Desviación FSK (Hz)", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._fsk_deviation_win)
        self.tx_time = qtgui.time_sink_c(
            1600, #size
            samp_rate, #samp_rate
            "Envolvente compleja FSK", #name
            1, #number of inputs
            None # parent
        )
        self.tx_time.set_update_time(0.10)
        self.tx_time.set_y_axis(-1.2, 1.2)

        self.tx_time.set_y_label('Amplitude', "")

        self.tx_time.enable_tags(True)
        self.tx_time.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.tx_time.enable_autoscale(False)
        self.tx_time.enable_grid(True)
        self.tx_time.enable_axis_labels(True)
        self.tx_time.enable_control_panel(False)
        self.tx_time.enable_stem_plot(False)


        labels = ['FSK I/Q', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.tx_time.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.tx_time.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.tx_time.set_line_label(i, labels[i])
            self.tx_time.set_line_width(i, widths[i])
            self.tx_time.set_line_color(i, colors[i])
            self.tx_time.set_line_style(i, styles[i])
            self.tx_time.set_line_marker(i, markers[i])
            self.tx_time.set_line_alpha(i, alphas[i])

        self._tx_time_win = sip.wrapinstance(self.tx_time.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._tx_time_win)
        self.throttle = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.symbol_repeat = blocks.repeat(gr.sizeof_float*1, sps)
        self.spectrum = qtgui.freq_sink_c(
            2048, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "PSD FSK", #name
            1,
            None # parent
        )
        self.spectrum.set_update_time(0.10)
        self.spectrum.set_y_axis((-140), 10)
        self.spectrum.set_y_label('Relative Gain', 'dB')
        self.spectrum.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.spectrum.enable_autoscale(False)
        self.spectrum.enable_grid(True)
        self.spectrum.set_fft_average(1.0)
        self.spectrum.enable_axis_labels(True)
        self.spectrum.enable_control_panel(False)
        self.spectrum.set_fft_window_normalized(False)



        labels = ['FSK', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.spectrum.set_line_label(i, "Data {0}".format(i))
            else:
                self.spectrum.set_line_label(i, labels[i])
            self.spectrum.set_line_width(i, widths[i])
            self.spectrum.set_line_color(i, colors[i])
            self.spectrum.set_line_alpha(i, alphas[i])

        self._spectrum_win = sip.wrapinstance(self.spectrum.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._spectrum_win)
        self.nrz_mapper = digital.chunks_to_symbols_bf([-1.0, 1.0], 1)
        self.fsk_modulator = analog.frequency_modulator_fc((2*math.pi*fsk_deviation/samp_rate))
        self.fsk_demod = analog.quadrature_demod_cf((samp_rate/(2*math.pi*fsk_deviation)))
        self.freq_inst = qtgui.time_sink_f(
            1600, #size
            samp_rate, #samp_rate
            "Frecuencia instantánea", #name
            1, #number of inputs
            None # parent
        )
        self.freq_inst.set_update_time(0.10)
        self.freq_inst.set_y_axis(-1.5, 1.5)

        self.freq_inst.set_y_label('Amplitude', "")

        self.freq_inst.enable_tags(True)
        self.freq_inst.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.freq_inst.enable_autoscale(False)
        self.freq_inst.enable_grid(True)
        self.freq_inst.enable_axis_labels(True)
        self.freq_inst.enable_control_panel(False)
        self.freq_inst.enable_stem_plot(False)


        labels = ['Frecuencia instantánea normalizada', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.freq_inst.set_line_label(i, "Data {0}".format(i))
            else:
                self.freq_inst.set_line_label(i, labels[i])
            self.freq_inst.set_line_width(i, widths[i])
            self.freq_inst.set_line_color(i, colors[i])
            self.freq_inst.set_line_style(i, styles[i])
            self.freq_inst.set_line_marker(i, markers[i])
            self.freq_inst.set_line_alpha(i, alphas[i])

        self._freq_inst_win = sip.wrapinstance(self.freq_inst.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._freq_inst_win)
        self.bit_source = blocks.vector_source_b([0,1,0,0,1,1,0,1,1,1,0,0,1,0,1,0], True, 1, [])


        ##################################################
        # Connections
        ##################################################
        self.connect((self.bit_source, 0), (self.nrz_mapper, 0))
        self.connect((self.fsk_demod, 0), (self.freq_inst, 0))
        self.connect((self.fsk_modulator, 0), (self.throttle, 0))
        self.connect((self.nrz_mapper, 0), (self.symbol_repeat, 0))
        self.connect((self.symbol_repeat, 0), (self.fsk_modulator, 0))
        self.connect((self.throttle, 0), (self.fsk_demod, 0))
        self.connect((self.throttle, 0), (self.spectrum, 0))
        self.connect((self.throttle, 0), (self.tx_time, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "Modulacion_FSK")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_symbol_rate(self.samp_rate/self.sps)
        self.symbol_repeat.set_interpolation(self.sps)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_symbol_rate(self.samp_rate/self.sps)
        self.freq_inst.set_samp_rate(self.samp_rate)
        self.fsk_demod.set_gain((self.samp_rate/(2*math.pi*self.fsk_deviation)))
        self.fsk_modulator.set_sensitivity((2*math.pi*self.fsk_deviation/self.samp_rate))
        self.spectrum.set_frequency_range(0, self.samp_rate)
        self.throttle.set_sample_rate(self.samp_rate)
        self.tx_time.set_samp_rate(self.samp_rate)

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate

    def get_fsk_deviation(self):
        return self.fsk_deviation

    def set_fsk_deviation(self, fsk_deviation):
        self.fsk_deviation = fsk_deviation
        self.fsk_demod.set_gain((self.samp_rate/(2*math.pi*self.fsk_deviation)))
        self.fsk_modulator.set_sensitivity((2*math.pi*self.fsk_deviation/self.samp_rate))




def main(top_block_cls=Modulacion_FSK, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
