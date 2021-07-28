import land_window_4
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from test_public_resource import *

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    pub_res_init()
    Public_Resource.Portrait_sequence_init()

    land_window = land_window_4.Land_Window()
    land_window.show()
    sys.exit(app.exec_())


