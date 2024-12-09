import sys
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QMessageBox,
    QLineEdit,
    QSpinBox,
    QSlider
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from learning_model import learn_immune_network  # Код обучения


class DropArea(QWidget):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.setAcceptDrops(True)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.label = QLabel("Перетащите лог-файл сюда")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            QLabel {
                border: 2px dashed lightgray;
                font-size: 16px;
            }
        """)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        self.main_window.add_dropped_files(files)


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.setParent(parent)
        plt.tight_layout()


class LearningThread(QThread):
    update_graph_signal = pyqtSignal(int, float)  # Передача данных для графика (поколение, точность)
    learning_complete_signal = pyqtSignal(str)  # Завершение обучения

    def __init__(self, individual_size, population_size, clone_count, mutation_rate, target_accuracy, log_file,
                 model_name):
        super().__init__()
        self.individual_size = individual_size
        self.population_size = population_size
        self.clone_count = clone_count
        self.mutation_rate = mutation_rate
        self.target_accuracy = target_accuracy
        self.log_file = log_file
        self.model_name = model_name

    def run(self):
        try:
            final_generation = 0
            final_accuracy = 0.0
            for gen, acc in learn_immune_network(
                    self.individual_size, self.population_size, self.clone_count,
                    self.mutation_rate, self.target_accuracy, self.log_file, self.model_name
            ):
                final_generation, final_accuracy = gen, acc
                self.update_graph_signal.emit(gen, acc)  # Отправляем данные для обновления графика

            # Отправляем финальный сигнал завершения
            self.learning_complete_signal.emit(f"Модель сохранена как {self.model_name}.pkl")
        except Exception as e:
            self.learning_complete_signal.emit(f"Ошибка: {str(e)}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.generations = []
        self.accuracies = []
        self.dropped_files = []
        self.learning_thread = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Обучение иммунной сети обнаружению dos/ddos атак в трафике")
        self.setGeometry(100, 100, 1500, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # Область для drag-and-drop
        self.drop_area = DropArea(self)
        self.drop_area.setMinimumHeight(250)
        left_layout.addWidget(self.drop_area, stretch=3)

        # Список файлов
        self.file_list_widget = QListWidget()
        self.file_list_widget.setMaximumHeight(150)
        left_layout.addWidget(self.file_list_widget, stretch=1)

        # Поля для параметров
        self.param_layout = QVBoxLayout()

        def create_slider_spinbox(label, min_val, max_val, step):
            layout = QHBoxLayout()
            label_widget = QLabel(label)
            slider = QSlider(Qt.Horizontal)
            slider.setRange(min_val, max_val)
            slider.setTickInterval(step)
            slider.setFixedWidth(200)
            spinbox = QSpinBox()
            spinbox.setRange(min_val, max_val)
            spinbox.setSingleStep(step)
            spinbox.setFixedWidth(60)

            slider.valueChanged.connect(spinbox.setValue)
            spinbox.valueChanged.connect(slider.setValue)

            slider.setValue(min_val)
            spinbox.setValue(min_val)

            layout.addWidget(label_widget)
            layout.addWidget(slider)
            layout.addWidget(spinbox)

            return layout, slider, spinbox

        # Слайдеры и спинбоксы для параметров
        layout, self.individual_size_slider, self.individual_size_spinbox = create_slider_spinbox(
            "Количество признаков", 1, 10, 1)
        self.param_layout.addLayout(layout)

        layout, self.population_size_slider, self.population_size_spinbox = create_slider_spinbox("Размер популяции",
                                                                                                  10, 1000, 10)
        self.param_layout.addLayout(layout)

        layout, self.clone_count_slider, self.clone_count_spinbox = create_slider_spinbox("Количество клонов", 1, 500,
                                                                                          1)
        self.param_layout.addLayout(layout)

        layout, self.mutation_rate_slider, self.mutation_rate_spinbox = create_slider_spinbox("Вероятность мутации (%)",
                                                                                              0, 100, 1)
        self.param_layout.addLayout(layout)

        layout, self.target_accuracy_slider, self.target_accuracy_spinbox = create_slider_spinbox(
            "Целевая точность (%)", 0, 100, 1)
        self.param_layout.addLayout(layout)

        left_layout.addLayout(self.param_layout)

        # Поле для названия модели
        self.model_name_input = QLineEdit()
        self.model_name_input.setPlaceholderText("Введите название модели (без пробелов)")
        left_layout.addWidget(QLabel("Название модели:"))
        left_layout.addWidget(self.model_name_input)

        # Кнопка запуска
        self.start_button = QPushButton("Начать обучение")
        self.start_button.setEnabled(False)
        self.start_button.clicked.connect(self.start_learning)
        left_layout.addWidget(self.start_button)

        # График и панель инструментов
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.toolbar = NavigationToolbar(self.canvas, self)
        right_layout.addWidget(self.toolbar)
        right_layout.addWidget(self.canvas)

        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 2)
        central_widget.setLayout(main_layout)

    def add_dropped_files(self, files):
        for file in files:
            if file not in self.dropped_files and file.endswith('.log'):
                self.dropped_files.append(file)
                self.file_list_widget.addItem(file)
        self.update_start_button_state()

    def update_start_button_state(self):
        self.start_button.setEnabled(bool(self.dropped_files))

    def update_graph(self, generation, accuracy):
        # Сохраняем последние значения
        self.generations.append(generation)  # Добавляем новое поколение
        self.accuracies.append(accuracy)

        # Рисуем график
        self.canvas.ax.clear()
        self.canvas.ax.plot(self.generations, self.accuracies, marker='o', label="Средняя точность")
        self.canvas.ax.set_xlabel("Поколение")
        self.canvas.ax.set_ylabel("Точность")
        self.canvas.ax.legend()
        self.canvas.draw()

    def on_learning_complete(self, message):
        self.learning_thread = None
        QMessageBox.information(self, "Обучение завершено", message)
        # Отрисовать финальный график с последними данными
        if hasattr(self, "final_generation") and hasattr(self, "final_accuracy"):
            self.update_graph(self.final_generation, self.final_accuracy)

    def start_learning(self):
        if self.learning_thread is not None and self.learning_thread.isRunning():
            QMessageBox.warning(self, "Ошибка", "Обучение уже запущено!")
            return

        log_file = self.dropped_files[0]
        model_name = self.model_name_input.text().strip()
        if not model_name or " " in model_name:
            QMessageBox.warning(self, "Ошибка", "Название модели не может быть пустым или содержать пробелы.")
            return

        individual_size = self.individual_size_spinbox.value()
        population_size = self.population_size_spinbox.value()
        clone_count = self.clone_count_spinbox.value()
        mutation_rate = self.mutation_rate_spinbox.value() / 100
        target_accuracy = self.target_accuracy_spinbox.value() / 100

        self.learning_thread = LearningThread(
            individual_size, population_size, clone_count, mutation_rate, target_accuracy, log_file, model_name
        )
        self.learning_thread.update_graph_signal.connect(self.update_graph)
        self.learning_thread.learning_complete_signal.connect(self.on_learning_complete)
        self.learning_thread.start()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()