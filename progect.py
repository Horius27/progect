import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel, QRadioButton, QMessageBox

class Quiz(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.setWindowTitle('Викторина')
        self.setGeometry(100, 100, 400, 300)

        self.questions = ['Вопрос 1: Что такое PyQt?',
                          'Вопрос 2: Какая версия Python используется в PyQt5?',
                          'Вопрос 3: Как создать главное окно в PyQt?',
                          'Вопрос 4: Как изменить название окна?']
        self.answers = [['Фреймворк для создания графических интерфейсов', 'Язык программирования', 'База данных'],
                        ['Python 2', 'Python 3', 'Python 3.5'],
                        ['Используя класс QDialog', 'Используя класс QMainWindow', 'Используя класс QWidget'],
                        ['setTitle', 'setWindowTitle', 'setWindowsTitle']]
        self.correct_answers = [0, 2, 1, 1]
        self.current_question = 0
        self.score = {'win': 0, 'lose': 0}

        self.question_label = QLabel(self.questions[self.current_question])
        self.radio_buttons = []
        for i in range(3):
            self.radio_buttons.append(QRadioButton(self.answers[self.current_question][i]))
        self.submit_button = QPushButton('Ответить')
        self.submit_button.clicked.connect(self.check_answer)

        layout = QVBoxLayout()
        layout.addWidget(self.question_label)
        for button in self.radio_buttons:
            layout.addWidget(button)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def check_answer(self):
        if any(button.isChecked() for button in self.radio_buttons):
            user_answer = next(i for i, button in enumerate(self.radio_buttons) if button.isChecked())
            if user_answer == self.correct_answers[self.current_question]:
                self.score['win'] += 1
            else:
                self.score['lose'] += 1
                self.parent.update_scores(self.score['win'], self.score['lose'])

            if self.current_question < 3:
                self.current_question += 1
                self.question_label.setText(self.questions[self.current_question])
                for button in self.radio_buttons:
                    button.setText(self.answers[self.current_question][self.radio_buttons.index(button)])
            else:
                if self.score['lose'] == 0:
                    self.parent.handle_victory()  # Вызываем метод родительского окна при успешном прохождении
                else:
                    QMessageBox.information(self, 'Результат', f'Вы набрали {self.score["win"]} балла')
                    self.parent.show_main_window()
                    self.parent.save_scores()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, выберите ответ.')
            self.score['lose'] += 1
            self.parent.update_scores(self.score['win'], self.score['lose'])

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Викторина')
        self.setGeometry(100, 100, 500, 200)

        self.vic_win = QWidget()
        self.vic_win.setWindowTitle('Викторина')
        self.vic_win.resize(500, 200)

        self.start_button = QPushButton('Start', self.vic_win)
        self.start_button.setGeometry(280, 220, 241, 121)
        self.start_button.setStyleSheet("background-color: green; color: lime; border-radius: 20px; font-size: 100px;")
        self.start_button.clicked.connect(self.start_quiz)

        self.list_vic_lable = QLabel('Правильных ответов:', self.vic_win)
        self.list_vic_lable.setGeometry(20, 30, 200, 20)
        self.list_vic = QLabel("0", self.vic_win)
        self.list_vic.setGeometry(240, 30, 20, 20)

        self.list_vics_lable = QLabel("Ошибок:", self.vic_win)
        self.list_vics_lable.setGeometry(20, 60, 100, 20)
        self.list_vics = QLabel("0", self.vic_win)
        self.list_vics.setGeometry(240, 60, 20, 20)

        self.layout_vic = QVBoxLayout(self.vic_win)
        self.layout_vic.addWidget(self.start_button)
        self.layout_vic.addWidget(self.list_vic_lable)
        self.layout_vic.addWidget(self.list_vic)
        self.layout_vic.addWidget(self.list_vics_lable)
        self.layout_vic.addWidget(self.list_vics)

        self.quiz = None

        self.setCentralWidget(self.vic_win)

        self.load_scores()

    def start_quiz(self):
        self.hide_main_window()
        self.quiz = Quiz(self)
        self.quiz.show()

    def update_scores(self, win, lose):
        self.list_vic.setText(str(win))
        self.list_vics.setText(str(lose))
        self.save_scores()

    def handle_victory(self):
        self.list_vic.setText(str(self.quiz.score['win'] + 1))
        QMessageBox.information(self, "Результат", f"Вы Выиграли!!!")
        self.show_main_window()
        self.save_scores()

    def hide_main_window(self):
        self.hide()

    def show_main_window(self):
        self.show()

    def save_scores(self):
        try:
            with open('data.json', 'r') as f:
                data = json.load(f)
                data['win'] += int(self.list_vic.text())
                data['lose'] += int(self.list_vics.text())
        except FileNotFoundError:
            data = {'win': int(self.list_vic.text()), 'lose': int(self.list_vics.text())}

        with open('data.json', 'w') as f:
            json.dump(data, f)

    def load_scores(self):
        try:
            with open('data.json', 'r') as f:
                data = json.load(f)
                self.list_vic.setText(str(data['win']))
                self.list_vics.setText(str(data['lose']))
        except FileNotFoundError:
            pass

if __name__ == '__main__':
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec_()