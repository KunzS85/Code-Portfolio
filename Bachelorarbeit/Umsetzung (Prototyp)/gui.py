import json

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QTableWidgetItem
import operator
import numpy as np
import copy
import business_logic_control as blc
import file_reader as fr


class NlpWorker(QObject):
    """
    This class is responsible for the NLP Process. It enables the execution of the calculation in the background
    and communicates with the GUI using PyQt Signals.
    """

    data_processed = pyqtSignal(dict)
    finished = pyqtSignal()

    def __init__(self, model_name, selected_text):
        QtCore.QObject.__init__(self)
        self.model_name = model_name
        self.selected_text = selected_text

    def run(self):
        """

        """
        pred = blc.get_prediction(self.model_name, self.selected_text)
        self.data_processed.emit(pred)
        self.finished.emit()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.current_prediction = {}
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1300, 880)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1300, 880))
        MainWindow.setMaximumSize(QtCore.QSize(1300, 880))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("SnoBERT.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(0, 0, 1165, 883))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_4.setContentsMargins(0, 0, 4, 0)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_6.setContentsMargins(3, -1, 0, 3)
        self.verticalLayout_6.setSpacing(3)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(310, 28))
        self.label.setMaximumSize(QtCore.QSize(310, 28))
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.cb_modell = QtWidgets.QComboBox(self.horizontalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_modell.sizePolicy().hasHeightForWidth())
        self.cb_modell.setSizePolicy(sizePolicy)
        self.cb_modell.setMinimumSize(QtCore.QSize(310, 28))
        self.cb_modell.setMaximumSize(QtCore.QSize(310, 28))
        self.cb_modell.setObjectName("cb_modell")

        self.add_items_to_dropdown_model()
        self.cb_modell.currentTextChanged.connect(self.add_model_description)

        self.verticalLayout.addWidget(self.cb_modell)
        self.verticalLayout_4.addLayout(self.verticalLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(310, 28))
        self.label_3.setMaximumSize(QtCore.QSize(310, 28))
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.te_import = QtWidgets.QTextEdit(self.horizontalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.te_import.sizePolicy().hasHeightForWidth())
        self.te_import.setSizePolicy(sizePolicy)
        self.te_import.setMinimumSize(QtCore.QSize(250, 28))
        self.te_import.setMaximumSize(QtCore.QSize(250, 28))
        self.te_import.setObjectName("te_import")
        self.horizontalLayout_2.addWidget(self.te_import)
        self.b_import = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
        self.b_import.clicked.connect(self.press_import)
        self.b_import.setMinimumSize(QtCore.QSize(50, 28))
        self.b_import.setMaximumSize(QtCore.QSize(50, 28))
        self.b_import.setObjectName("b_import")
        self.horizontalLayout_2.addWidget(self.b_import)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(260, 28))
        self.label_2.setMaximumSize(QtCore.QSize(260, 28))
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.cb_resultat = QtWidgets.QComboBox(self.horizontalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_resultat.sizePolicy().hasHeightForWidth())
        self.cb_resultat.setSizePolicy(sizePolicy)
        self.cb_resultat.setMinimumSize(QtCore.QSize(260, 28))
        self.cb_resultat.setMaximumSize(QtCore.QSize(260, 28))
        self.cb_resultat.setObjectName("cb_resultat")

        self.add_items_to_dropdown_results()

        self.verticalLayout_2.addWidget(self.cb_resultat)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_7.setContentsMargins(-1, -1, -1, 5)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        spacerItem = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem)
        self.b_refresh = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
        self.b_refresh.clicked.connect(self.press_refresh)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_refresh.sizePolicy().hasHeightForWidth())
        self.b_refresh.setSizePolicy(sizePolicy)
        self.b_refresh.setMinimumSize(QtCore.QSize(50, 30))
        self.b_refresh.setMaximumSize(QtCore.QSize(50, 30))
        self.b_refresh.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("change.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_refresh.setIcon(icon1)
        self.b_refresh.setFlat(True)
        self.b_refresh.setObjectName("b_refresh")
        self.verticalLayout_7.addWidget(self.b_refresh)
        self.horizontalLayout.addLayout(self.verticalLayout_7)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.horizontalLayout_3.addLayout(self.verticalLayout_4)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_5.setSpacing(2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_4 = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QtCore.QSize(310, 28))
        self.label_4.setMaximumSize(QtCore.QSize(310, 28))
        self.label_4.setObjectName("label_4")
        self.verticalLayout_5.addWidget(self.label_4)
        self.te_modell_desc = QtWidgets.QTextEdit(self.horizontalLayoutWidget_4,)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.te_modell_desc.sizePolicy().hasHeightForWidth())
        self.te_modell_desc.setSizePolicy(sizePolicy)
        self.te_modell_desc.setMinimumSize(QtCore.QSize(312, 155))
        self.te_modell_desc.setMaximumSize(QtCore.QSize(312, 155))
        self.te_modell_desc.setReadOnly(True)
        self.te_modell_desc.setObjectName("te_modell_desc")
        self.verticalLayout_5.addWidget(self.te_modell_desc)
        self.horizontalLayout_3.addLayout(self.verticalLayout_5)
        self.verticalLayout_6.addLayout(self.horizontalLayout_3)
        self.te_text = QtWidgets.QTextEdit(self.horizontalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.te_text.sizePolicy().hasHeightForWidth())
        self.te_text.setSizePolicy(sizePolicy)
        self.te_text.setMinimumSize(QtCore.QSize(630, 650))
        self.te_text.setMaximumSize(QtCore.QSize(630, 650))
        self.te_text.setObjectName("te_text")
        self.te_text.setAcceptDrops(False)
        self.verticalLayout_6.addWidget(self.te_text)
        self.b_start = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
        self.b_start.clicked.connect(self.press_start)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_start.sizePolicy().hasHeightForWidth())
        self.b_start.setSizePolicy(sizePolicy)
        self.b_start.setMinimumSize(QtCore.QSize(630, 30))
        self.b_start.setMaximumSize(QtCore.QSize(630, 30))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.b_start.setFont(font)
        self.b_start.setStyleSheet("background-color: rgb(136, 202, 100);\n"
"color: rgb(255, 255, 255);")
        self.b_start.setObjectName("b_start")
        self.verticalLayout_6.addWidget(self.b_start)
        self.horizontalLayout_4.addLayout(self.verticalLayout_6)
        self.tv_result = QtWidgets.QTableWidget(self.horizontalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tv_result.sizePolicy().hasHeightForWidth())
        self.tv_result.setSizePolicy(sizePolicy)
        self.tv_result.setMinimumSize(QtCore.QSize(655, 864))
        self.tv_result.setMaximumSize(QtCore.QSize(655, 864))
        self.tv_result.setObjectName("tv_result")
        self.tv_result.verticalHeader().hide()
        self.horizontalLayout_4.addWidget(self.tv_result)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SNOMAST 2.0"))
        self.label.setText(_translate("MainWindow", "Modell Auswahl"))
        self.label_3.setText(_translate("MainWindow", "Datei importieren (Drag\'n\'Drop .pdf, .txt)"))
        self.b_import.setText(_translate("MainWindow", "IMP"))
        self.label_2.setText(_translate("MainWindow", "Anzahl Resultate"))
        self.label_4.setText(_translate("MainWindow", "Beschreibung des Modells"))
        self.b_start.setText(_translate("MainWindow", "START"))

    def get_model_infos(self) -> dict:
        """
        This method gets the info from the business logic about the models that can be used.
        :return: A dictionary with keys consisting of the model names and the value is a
        dictionary with "name" and "description" as keys.
        """
        model_infos = blc.get_models_names()
        return model_infos

    def add_items_to_dropdown_model(self) -> None:
        """
        This method fills the dropdown, which represents the selection of available models
        """
        item_list = [""]
        for k, v in self.get_model_infos().items():
            item_list.append(k)
        self.cb_modell.addItems(item_list)

    def add_model_description(self, model_name: str) -> None:
        """
        This method fills the description text field with the model description of the model that is currently
        displayed in the model dropdown
        :param model_name: The currently displayed name is automatically passed from the dropdown to the method
        when something changes in the dropdown
        """
        model_infos = self.get_model_infos()
        if (self.cb_modell.currentText() == ""):
            self.te_modell_desc.setPlainText("Kein Modell ausgewählt")
        else:
            self.te_modell_desc.setPlainText(model_infos[model_name]["description"])

    def add_items_to_dropdown_results(self) -> None:
        """
        This method fills the result dropdown with a list of integers between 0-51 in 10 steps
        """
        self.cb_resultat.addItems([str(x) for x in range(10, 51, 10)])

    def press_start(self) -> None:
        """
        This method checks first  whether text was marked or not,
        if text was marked, this text is processed and the marked area in the text is colored. If no text was marked,
        the first 3000 characters are captured and processed.
        If no model is selected, the first model in the list of the model dropdown is selected, otherwise the
        selected model is used. The text and the model name is sent to the background task
        The prediction is executed in the background and the results are automatically passed
        to the on_data_ready method.
        during the calculation the start button is colored red and switched off
        """
        self.b_start.setEnabled(False)

        self.b_start.setStyleSheet("background-color: rgb(139, 37, 0);" "color: rgb(255, 255, 255);")

        cursor = self.te_text.textCursor()
        if cursor.hasSelection():
            text = cursor.selectedText()
            color = list(np.random.choice(range(256), size=3))
            fmt = cursor.charFormat()
            fmt.setBackground(QBrush(QColor(color[0] + (0.5 * (255 - color[0])),
                                            color[1] + (0.5 * (255 - color[1])),
                                            color[2] + (0.5 * (255 - color[2])))))
            cursor.mergeCharFormat(fmt)
        else:
            text = self.te_text.toPlainText()

        if not text:
            self.te_text.setText("Ich kann ohne Text nicht arbeiten ;-)")
            return

        tokens = len(text.split())
        if tokens > 400:
            selected_text = text[:3000]
        else:
            selected_text = text
        #print(len(selected_text.split()))
        active_model = self.cb_modell.currentText()
        if (active_model == ""):
            values_view = self.get_model_infos().values()
            value_iterator = iter(values_view)
            first_value = next(value_iterator)
            name = first_value["name"]
            self.cb_modell.setCurrentText(name)
            model_name = name
        else:
            model_name = active_model

        self.thread = QThread()
        self.nlp_task = NlpWorker(model_name, selected_text)
        self.nlp_task.moveToThread(self.thread)
        self.thread.started.connect(self.nlp_task.run)
        self.nlp_task.data_processed.connect(self.on_data_ready)
        self.nlp_task.finished.connect(self.thread.quit)

        self.thread.start()


    def on_data_ready(self, prediction):
        """
        This method is executed only after the completion of the background task.
        The Start button is switched on again and set to green. The result of the calculation is saved in the GUI and
        the method for filling the table is called up.
        """
        self.b_start.setDisabled(False)
        self.b_start.setStyleSheet("background-color: rgb(136, 202, 100);" "color: rgb(255, 255, 255);")
        self.current_prediction.clear()
        self.current_prediction = copy.deepcopy(prediction)
        self.press_refresh()

    def press_import(self) -> None:
        """
        This method reads the string in the import text field. Checks its extension for the desired file formats.
        If it is a suitable file format, the text is passed to the filereader and its result is displayed in the
        display window. otherwise the user is informed that this cannot be executed.
        """
        pt = self.te_import.toPlainText()
        url = pt[8:]
        file_form = url[len(url) - 4:]
        if file_form == ".txt":
            import_text = fr.read_txt(url)
        elif file_form == ".pdf":
            import_text = fr.read_pdf(url)
        else:
            import_text = "Wenn die Anforderungen an ein File nicht eingehalten werden, kann ich nicht Arbeiten ;-)"

        self.te_text.setText(import_text)

    def press_refresh(self) -> None:
        """
        This method checks if the GUI currently has a prediction to use, if not, nothing happens. If there is a
        prediction, it is passed to the method for filling the table with the number of results to be displayed.
        """
        if not self.current_prediction:
            return
        quantity = int(self.cb_resultat.currentText())
        self.fill_table_view(quantity, self.current_prediction)

    def fill_table_view(self, quantity: int, predictions: dict) -> None:
        """
        This method first sorts the results based on the size of the prediction. This sorting is now the basis for
        filling the table. Only the n highest results are displayed in the table, where n represents the number of
        desired results from the dropdown.
        :param quantity: An integer representing the number of results to be displayed.
        :param predictions: dictionary which contains the results of the last execution
        """
        self.tv_result.clear()
        d = {}

        for k, v in predictions.items():
            d[k] = v["probability"]
        #print("enter sorting")
        sorted_d = dict(sorted(d.items(), key=operator.itemgetter(1), reverse=True))
        order = [k for k, v in sorted_d.items()]
        #print(f"leave sorting {order}")
        horHeaders = ["Wahrscheinlichkeit", "Konzept ID", "Konzeptnamen", "Konzept ID | Konzeptnamen"]
        self.tv_result.setColumnCount(len(horHeaders))
        self.tv_result.setHorizontalHeaderLabels(horHeaders)
        self.tv_result.setRowCount(quantity)
        count = 0
        for n in order[:quantity]:
            p = str(predictions[n]["probability"])
            prob = QTableWidgetItem(p)
            i = predictions[n]["code"]
            k_id = QTableWidgetItem(i)
            k = predictions[n]["name"]
            kn = QTableWidgetItem(k)
            ik = f"{predictions[n]['code']} | {predictions[n]['name']}"
            k_id_kn = QTableWidgetItem(ik)
            items = [prob, k_id, kn, k_id_kn]
            for m in range(len(items)):
                self.tv_result.setItem(count, m, items[m])
            count += 1

        self.tv_result.resizeColumnsToContents()
        self.tv_result.resizeRowsToContents()


def start_gui():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
