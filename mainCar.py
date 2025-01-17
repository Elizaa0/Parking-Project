import datetime
from PyQt5 import QtWidgets, QtCore, QtGui, uic
from detect import detect_license_plate


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi("front.ui", self)

        self.ENTRYBUTTON.clicked.connect(self.handle_entry)
        self.EXITBUTTON.clicked.connect(self.handle_exit)
        self.loadImageButton.clicked.connect(self.load_image)

        self.slots = [False] * 5
        self.car_numbers = [None] * 5
        self.entry_times = {}
        self.parking_buttons = [
            self.findChild(QtWidgets.QPushButton, f"s{i + 1}") for i in range(5)
        ]
        self.update_slot_buttons()
        self.current_pixmap = None

    def load_image(self):

        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Wybierz obraz", "", "Obrazy (*.png *.jpg *.jpeg)"
        )
        if file_path:
            pixmap = QtGui.QPixmap(file_path)
            self.current_pixmap = pixmap
            self.display_image()
            license_plate = detect_license_plate(file_path)
            if license_plate:
                self.comboBoxRejestracja.clear()
                self.comboBoxRejestracja.addItem(license_plate)
                self.label_2.setText(f"Rozpoznano: {license_plate}")
            else:
                self.comboBoxRejestracja.clear()
                self.comboBoxRejestracja.addItem("-")
                self.label_2.setText("Nie rozpoznano tablicy.")

    def display_image(self):
        if self.current_pixmap:
            self.imagePreview.setPixmap(
                self.current_pixmap.scaled(
                    self.imagePreview.size(),
                    QtCore.Qt.KeepAspectRatio,
                    QtCore.Qt.SmoothTransformation,
                )
            )

    def resizeEvent(self, event):
        super(Ui, self).resizeEvent(event)
        self.display_image()

    def handle_entry(self):
        rejestracja = self.comboBoxRejestracja.currentText()
        if rejestracja and rejestracja != "-":
            try:
                slot = self.slots.index(False)
                self.slots[slot] = True
                self.car_numbers[slot] = rejestracja
                entry_time = datetime.datetime.now()
                self.entry_times[rejestracja] = entry_time
                self.label_2.setText(
                    f"Zarejestrowano wjazd: {rejestracja} (Miejsce: {slot + 1})"
                )
                self.labelEntryTime.setText(
                    f"Godzina wjazdu: {entry_time.strftime('%H:%M:%S')}"
                )
                self.update_slot_buttons()
                self.update_combobox_items()
            except ValueError:
                self.label_2.setText("Brak dostępnych miejsc.")

    def handle_exit(self):
        rejestracja = self.comboBoxRejestracja.currentText()
        if rejestracja and rejestracja in self.entry_times:
            slot = self.car_numbers.index(rejestracja)
            self.slots[slot] = False
            self.car_numbers[slot] = None
            entry_time = self.entry_times.pop(rejestracja)
            exit_time = datetime.datetime.now()
            duration = (exit_time - entry_time).total_seconds()
            cost = int(duration)  # 1 zł za sekundę
            self.label_2.setText(
                f"Wyjazd: {rejestracja} (Koszt: {cost} zł)"
            )
            self.labelCost.setText(f"Koszt: {cost} zł")
            self.labelEntryTime.setText("Godzina wjazdu: -")
            self.labelExitTime.setText(
                f"Godzina wyjazdu: {exit_time.strftime('%H:%M:%S')}"
            )
            self.update_slot_buttons()
            self.update_combobox_items()

    def update_slot_buttons(self):
        for i, button in enumerate(self.parking_buttons):
            if self.slots[i]:
                button.setStyleSheet("background-color: red; color: white;")
                button.setText(self.car_numbers[i])
            else:
                button.setStyleSheet("background-color: green; color: black;")
                button.setText(f"M{i + 1}")

    def update_combobox_items(self):
        self.comboBoxRejestracja.clear()
        for car_number in self.car_numbers:
            if car_number:
                self.comboBoxRejestracja.addItem(car_number)


def main():
    app = QtWidgets.QApplication([])
    window = Ui()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
