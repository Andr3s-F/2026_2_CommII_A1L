#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Modulacion_FSK_AWGN
# Description: FSK con AWGN: comparación de envolvente compleja, PSD y frecuencia instantánea
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
import math
from gnuradio import blocks
from gnuradio import channels
from gnuradio.filter import firdes
from gnuradio import digital
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import sip
import threading



class Modulacion_FSK_AWGN(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Modulacion_FSK_AWGN", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Modulacion_FSK_AWGN")
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "Modulacion_FSK_AWGN")

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
        self.noise_voltage = noise_voltage = 0.1
        self.fsk_deviation = fsk_deviation = 20000

        ##################################################
        # Blocks
        ##################################################

        self._noise_voltage_range = qtgui.Range(0.0, 5.5, 0.001, 0.1, 200)
        self._noise_voltage_win = qtgui.RangeWidget(self._noise_voltage_range, self.set_noise_voltage, "Noise voltage", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._noise_voltage_win)
        self._fsk_deviation_range = qtgui.Range(5000, 100000, 1000, 20000, 200)
        self._fsk_deviation_win = qtgui.RangeWidget(self._fsk_deviation_range, self.set_fsk_deviation, "Desviación FSK (Hz)", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._fsk_deviation_win)
        self.throttle = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.symbol_repeat = blocks.repeat(gr.sizeof_float*1, sps)
        self.spectrum_compare = qtgui.freq_sink_c(
            2048, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "PSD FSK: ideal vs AWGN", #name
            2,
            None # parent
        )
        self.spectrum_compare.set_update_time(0.10)
        self.spectrum_compare.set_y_axis((-140), 10)
        self.spectrum_compare.set_y_label('Relative Gain', 'dB')
        self.spectrum_compare.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.spectrum_compare.enable_autoscale(False)
        self.spectrum_compare.enable_grid(True)
        self.spectrum_compare.set_fft_average(1.0)
        self.spectrum_compare.enable_axis_labels(True)
        self.spectrum_compare.enable_control_panel(False)
        self.spectrum_compare.set_fft_window_normalized(False)



        labels = ['Tx ideal', 'Rx + AWGN', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.spectrum_compare.set_line_label(i, "Data {0}".format(i))
            else:
                self.spectrum_compare.set_line_label(i, labels[i])
            self.spectrum_compare.set_line_width(i, widths[i])
            self.spectrum_compare.set_line_color(i, colors[i])
            self.spectrum_compare.set_line_alpha(i, alphas[i])

        self._spectrum_compare_win = sip.wrapinstance(self.spectrum_compare.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._spectrum_compare_win)
        self.rx_time = qtgui.time_sink_c(
            1600, #size
            samp_rate, #samp_rate
            "Envolvente compleja FSK: ideal vs AWGN", #name
            2, #number of inputs
            None # parent
        )
        self.rx_time.set_update_time(0.10)
        self.rx_time.set_y_axis(-8, 8)

        self.rx_time.set_y_label('Amplitude', "")

        self.rx_time.enable_tags(True)
        self.rx_time.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.rx_time.enable_autoscale(False)
        self.rx_time.enable_grid(True)
        self.rx_time.enable_axis_labels(True)
        self.rx_time.enable_control_panel(False)
        self.rx_time.enable_stem_plot(False)


        labels = ['Tx ideal', 'Rx + AWGN', '', '', '',
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


        for i in range(4):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.rx_time.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.rx_time.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.rx_time.set_line_label(i, labels[i])
            self.rx_time.set_line_width(i, widths[i])
            self.rx_time.set_line_color(i, colors[i])
            self.rx_time.set_line_style(i, styles[i])
            self.rx_time.set_line_marker(i, markers[i])
            self.rx_time.set_line_alpha(i, alphas[i])

        self._rx_time_win = sip.wrapinstance(self.rx_time.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._rx_time_win)
        self.nrz_mapper = digital.chunks_to_symbols_bf([-1.0, 1.0], 1)
        self.fsk_modulator = analog.frequency_modulator_fc((2*math.pi*fsk_deviation/samp_rate))
        self.fsk_demod_tx = analog.quadrature_demod_cf((samp_rate/(2*math.pi*fsk_deviation)))
        self.fsk_demod_rx = analog.quadrature_demod_cf((samp_rate/(2*math.pi*fsk_deviation)))
        self.freq_inst_compare = qtgui.time_sink_f(
            1600, #size
            samp_rate, #samp_rate
            "Frecuencia instantánea: ideal vs AWGN", #name
            2, #number of inputs
            None # parent
        )
        self.freq_inst_compare.set_update_time(0.10)
        self.freq_inst_compare.set_y_axis(-4, 4)

        self.freq_inst_compare.set_y_label('Amplitude', "")

        self.freq_inst_compare.enable_tags(True)
        self.freq_inst_compare.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.freq_inst_compare.enable_autoscale(False)
        self.freq_inst_compare.enable_grid(True)
        self.freq_inst_compare.enable_axis_labels(True)
        self.freq_inst_compare.enable_control_panel(False)
        self.freq_inst_compare.enable_stem_plot(False)


        labels = ['Tx ideal', 'Rx + AWGN', '', '', '',
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
                self.freq_inst_compare.set_line_label(i, "Data {0}".format(i))
            else:
                self.freq_inst_compare.set_line_label(i, labels[i])
            self.freq_inst_compare.set_line_width(i, widths[i])
            self.freq_inst_compare.set_line_color(i, colors[i])
            self.freq_inst_compare.set_line_style(i, styles[i])
            self.freq_inst_compare.set_line_marker(i, markers[i])
            self.freq_inst_compare.set_line_alpha(i, alphas[i])

        self._freq_inst_compare_win = sip.wrapinstance(self.freq_inst_compare.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._freq_inst_compare_win)
        self.channel_awgn = channels.channel_model(
            noise_voltage=noise_voltage,
            frequency_offset=0.0,
            epsilon=1.0,
            taps=[1.0 + 0.0j],
            noise_seed=0,
            block_tags=True)
        self.bit_source = blocks.vector_source_b([0,1,0,0,1,1,0,1,1,1,0,0,1,0,1,0], True, 1, [])


        ##################################################
        # Connections
        ##################################################
        self.connect((self.bit_source, 0), (self.nrz_mapper, 0))
        self.connect((self.channel_awgn, 0), (self.fsk_demod_rx, 0))
        self.connect((self.channel_awgn, 0), (self.rx_time, 1))
        self.connect((self.channel_awgn, 0), (self.spectrum_compare, 1))
        self.connect((self.fsk_demod_rx, 0), (self.freq_inst_compare, 1))
        self.connect((self.fsk_demod_tx, 0), (self.freq_inst_compare, 0))
        self.connect((self.fsk_modulator, 0), (self.throttle, 0))
        self.connect((self.nrz_mapper, 0), (self.symbol_repeat, 0))
        self.connect((self.symbol_repeat, 0), (self.fsk_modulator, 0))
        self.connect((self.throttle, 0), (self.channel_awgn, 0))
        self.connect((self.throttle, 0), (self.fsk_demod_tx, 0))
        self.connect((self.throttle, 0), (self.rx_time, 0))
        self.connect((self.throttle, 0), (self.spectrum_compare, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "Modulacion_FSK_AWGN")
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
        self.freq_inst_compare.set_samp_rate(self.samp_rate)
        self.fsk_demod_rx.set_gain((self.samp_rate/(2*math.pi*self.fsk_deviation)))
        self.fsk_demod_tx.set_gain((self.samp_rate/(2*math.pi*self.fsk_deviation)))
        self.fsk_modulator.set_sensitivity((2*math.pi*self.fsk_deviation/self.samp_rate))
        self.rx_time.set_samp_rate(self.samp_rate)
        self.spectrum_compare.set_frequency_range(0, self.samp_rate)
        self.throttle.set_sample_rate(self.samp_rate)

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate

    def get_noise_voltage(self):
        return self.noise_voltage

    def set_noise_voltage(self, noise_voltage):
        self.noise_voltage = noise_voltage
        self.channel_awgn.set_noise_voltage(self.noise_voltage)

    def get_fsk_deviation(self):
        return self.fsk_deviation

    def set_fsk_deviation(self, fsk_deviation):
        self.fsk_deviation = fsk_deviation
        self.fsk_demod_rx.set_gain((self.samp_rate/(2*math.pi*self.fsk_deviation)))
        self.fsk_demod_tx.set_gain((self.samp_rate/(2*math.pi*self.fsk_deviation)))
        self.fsk_modulator.set_sensitivity((2*math.pi*self.fsk_deviation/self.samp_rate))




def main(top_block_cls=Modulacion_FSK_AWGN, options=None):

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
