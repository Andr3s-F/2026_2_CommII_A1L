#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Aplicacion Practica - Canal AWGN
# Author: lizaness
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import aplicacion_ruido_epy_block_0 as epy_block_0  # embedded python block
import sip



class aplicacion_ruido(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Aplicacion Practica - Canal AWGN", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Aplicacion Practica - Canal AWGN")
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

        self.settings = Qt.QSettings("GNU Radio", "aplicacion_ruido")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self.amp_ruido = amp_ruido = 0.5

        ##################################################
        # Blocks
        ##################################################

        self._amp_ruido_range = qtgui.Range(0, 2, 0.05, 0.5, 200)
        self._amp_ruido_win = qtgui.RangeWidget(self._amp_ruido_range, self.set_amp_ruido, "Nivel de Ruido (Sigma)", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._amp_ruido_win)
        self.qtgui_number_sink_0_4 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.qtgui_number_sink_0_4.set_update_time(0.10)
        self.qtgui_number_sink_0_4.set_title("Desviacion Estandar")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0_4.set_min(i, -1)
            self.qtgui_number_sink_0_4.set_max(i, 1)
            self.qtgui_number_sink_0_4.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_4.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_4.set_label(i, labels[i])
            self.qtgui_number_sink_0_4.set_unit(i, units[i])
            self.qtgui_number_sink_0_4.set_factor(i, factor[i])

        self.qtgui_number_sink_0_4.enable_autoscale(False)
        self._qtgui_number_sink_0_4_win = sip.wrapinstance(self.qtgui_number_sink_0_4.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_number_sink_0_4_win)
        self.qtgui_number_sink_0_3 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.qtgui_number_sink_0_3.set_update_time(0.10)
        self.qtgui_number_sink_0_3.set_title("Potencia Promedio")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0_3.set_min(i, -1)
            self.qtgui_number_sink_0_3.set_max(i, 1)
            self.qtgui_number_sink_0_3.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_3.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_3.set_label(i, labels[i])
            self.qtgui_number_sink_0_3.set_unit(i, units[i])
            self.qtgui_number_sink_0_3.set_factor(i, factor[i])

        self.qtgui_number_sink_0_3.enable_autoscale(False)
        self._qtgui_number_sink_0_3_win = sip.wrapinstance(self.qtgui_number_sink_0_3.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_number_sink_0_3_win)
        self.qtgui_number_sink_0_2 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.qtgui_number_sink_0_2.set_update_time(0.10)
        self.qtgui_number_sink_0_2.set_title("RMS")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0_2.set_min(i, -1)
            self.qtgui_number_sink_0_2.set_max(i, 1)
            self.qtgui_number_sink_0_2.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_2.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_2.set_label(i, labels[i])
            self.qtgui_number_sink_0_2.set_unit(i, units[i])
            self.qtgui_number_sink_0_2.set_factor(i, factor[i])

        self.qtgui_number_sink_0_2.enable_autoscale(False)
        self._qtgui_number_sink_0_2_win = sip.wrapinstance(self.qtgui_number_sink_0_2.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_number_sink_0_2_win)
        self.qtgui_number_sink_0_1 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.qtgui_number_sink_0_1.set_update_time(0.10)
        self.qtgui_number_sink_0_1.set_title("Media Cuadratica")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0_1.set_min(i, -1)
            self.qtgui_number_sink_0_1.set_max(i, 1)
            self.qtgui_number_sink_0_1.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_1.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_1.set_label(i, labels[i])
            self.qtgui_number_sink_0_1.set_unit(i, units[i])
            self.qtgui_number_sink_0_1.set_factor(i, factor[i])

        self.qtgui_number_sink_0_1.enable_autoscale(False)
        self._qtgui_number_sink_0_1_win = sip.wrapinstance(self.qtgui_number_sink_0_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_number_sink_0_1_win)
        self.qtgui_number_sink_0_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.qtgui_number_sink_0_0.set_update_time(0.10)
        self.qtgui_number_sink_0_0.set_title("Media")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0_0.set_min(i, -1)
            self.qtgui_number_sink_0_0.set_max(i, 1)
            self.qtgui_number_sink_0_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_0.set_label(i, labels[i])
            self.qtgui_number_sink_0_0.set_unit(i, units[i])
            self.qtgui_number_sink_0_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0_0.enable_autoscale(False)
        self._qtgui_number_sink_0_0_win = sip.wrapinstance(self.qtgui_number_sink_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_number_sink_0_0_win)
        self.qtgui_histogram_sink_x_0 = qtgui.histogram_sink_f(
            1024,
            100,
            (-3),
            3,
            "",
            1,
            None # parent
        )

        self.qtgui_histogram_sink_x_0.set_update_time(0.10)
        self.qtgui_histogram_sink_x_0.enable_autoscale(True)
        self.qtgui_histogram_sink_x_0.enable_accumulate(False)
        self.qtgui_histogram_sink_x_0.enable_grid(False)
        self.qtgui_histogram_sink_x_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers= [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_histogram_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_histogram_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_histogram_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_histogram_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_histogram_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_histogram_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_histogram_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_histogram_sink_x_0_win = sip.wrapinstance(self.qtgui_histogram_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_histogram_sink_x_0_win)
        self.epy_block_0 = epy_block_0.blk()
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_float*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 1000, 1, 0, 0)
        self.analog_noise_source_x_0 = analog.noise_source_f(analog.GR_GAUSSIAN, amp_ruido, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.epy_block_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.qtgui_histogram_sink_x_0, 0))
        self.connect((self.epy_block_0, 0), (self.qtgui_number_sink_0_0, 0))
        self.connect((self.epy_block_0, 1), (self.qtgui_number_sink_0_1, 0))
        self.connect((self.epy_block_0, 2), (self.qtgui_number_sink_0_2, 0))
        self.connect((self.epy_block_0, 3), (self.qtgui_number_sink_0_3, 0))
        self.connect((self.epy_block_0, 4), (self.qtgui_number_sink_0_4, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "aplicacion_ruido")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)

    def get_amp_ruido(self):
        return self.amp_ruido

    def set_amp_ruido(self, amp_ruido):
        self.amp_ruido = amp_ruido
        self.analog_noise_source_x_0.set_amplitude(self.amp_ruido)




def main(top_block_cls=aplicacion_ruido, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

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
