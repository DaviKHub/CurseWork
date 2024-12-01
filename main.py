from customtkinter import *


class Application(CTk):

    def slider_event(self, value, label):
        self.slider_value = int(value)
        label.configure(text=f"{label.text.split(':')[0]}: {self.slider_value}")  # Обновляем текст в label
        return self.slider_value

    def start_learning_button(self):
        # learning_model.main()
        pass

    def testing_button(self):
        pass

    def learning_button(self):
        pass

    def __init__(self):
        set_appearance_mode("light")
        super().__init__()
        self.geometry("829x800")
        self.resizable(height=False, width=False)
        self.configure(background="#F5F5F5")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)  # Левая панель фиксированная
        self.grid_columnconfigure(1, weight=1)
        self.left_frame = CTkFrame(
            master=self,
            fg_color="#F5F5F5",
            width=326,
        )
        # Настройка главного окна (Application)
        self.grid_rowconfigure(0, weight=1)  # Позволяем растягиваться вертикально
        self.grid_columnconfigure(0, weight=0)  # Левая панель фиксированная
        self.grid_columnconfigure(1, weight=1)  # Правая панель растягивается

        # Левая панель (left_frame)
        self.left_frame.grid(row=0, column=0, sticky="ns")  # Растягивается только по высоте

        # Добавляем кнопки в left_frame
        self.left_frame.grid_rowconfigure(0, weight=0)  # Ряд для первой кнопки
        self.left_frame.grid_rowconfigure(1, weight=0)  # Ряд для второй кнопки
        self.left_frame.grid_rowconfigure(2, weight=1)  # Оставшееся пространство
        self.left_frame.grid_columnconfigure(0, weight=1)  # Центрируем содержимое горизонтально

        # Фрейм для кнопки "Обучить модель"
        self.learning_button_frame = CTkFrame(
            master=self.left_frame,
            fg_color="#EAEAEA",  # Цвет фона фрейма
            border_width=2,  # Толщина границы
            border_color="#000000",  # Цвет границы
            width=500,  # Ширина
            height=93  # Высота
        )
        self.learning_button = CTkButton(
            master=self.learning_button_frame,
            text="Обучить модель",
            fg_color="#2C2C2C",
            text_color="#F5F5F5",
            corner_radius=8,
            width=263,
            height=40,
            command=self.learning_button
        )
        self.learning_button.pack(anchor="center", pady=5)  # Центрируем кнопку внутри фрейма
        self.learning_button_frame.grid(row=0, column=0, pady=(30, 5), padx=10, sticky="ew")  # Выравнивание

        # Фрейм для кнопки "Протестировать модель"
        self.testing_button_frame = CTkFrame(
            master=self.left_frame,
            fg_color="#EAEAEA",
            width=326,
            height=93,
            border_width=2
        )
        self.testing_button = CTkButton(
            master=self.testing_button_frame,
            text="Протестировать модель",
            fg_color="#2C2C2C",
            text_color="#F5F5F5",
            corner_radius=8,
            width=263,
            height=40,
            command=self.testing_button
        )
        self.testing_button.pack(pady=5)  # Центрируем кнопку внутри фрейма
        self.testing_button_frame.grid(row=1, column=0, pady=(5, 10), padx=10, sticky="ew")  # Следующей строкой

        self.right_frame = CTkFrame(
            master=self,
            fg_color="#F5F5F5",
            width=326,
            height=93
        )
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        self.label1 = CTkLabel(
            master=self.right_frame,
            text="Выберете лог-файл",
            fg_color="#2C2C2C",
            height=40,
            width=425,
            corner_radius=8,
            text_color="#F5F5F5"
        )
        self.label1.grid(row=0, column=0)
        self.file_frame = CTkFrame(
            master=self.right_frame,
            fg_color="#DADADA",
            width=425,
            height=171,
            corner_radius=8,
            border_width=20,
            border_color="#DCDCDC"
        )
        self.file_label = CTkLabel(
            master=self.file_frame,
            text="Укажите путь к лог файлу или перетащите его сюда",
            width=425,
            height=171,
            text_color="#2C2C2C",
        )
        self.file_label.pack()
        self.file_frame.grid(row=1, column=0, sticky="nsew", pady=(30, 5))

        self.parameters_frame = CTkFrame(
            master=self.right_frame,
            border_width=2,
            fg_color="#DCDCDC",
        )
        self.parameters_label = CTkLabel(
            master=self.parameters_frame,
            text="Укажите параметры модели",
        )
        # 1
        self.population_slider = CTkSlider(
            master=self.parameters_frame,
            from_=10,
            to=1500,
            number_of_steps=1490,
            command=lambda value: self.slider_event(value, self.population_label)  # Передаём label
        )
        self.population_label = CTkLabel(
            master=self.parameters_frame,
            text=f"Размер популяции: 0"
        )
        # 2
        self.iteration_slider = CTkSlider(
            master=self.parameters_frame,
            from_=10,
            to=1500,
            number_of_steps=1490,
            command=lambda value: self.slider_event(value)  # Вызываем метод
        )
        self.iteration_label = CTkLabel(
            master=self.parameters_frame,
            text=f"Количество итераций: 0"
        )
        # 3
        self.count_clones_slider = CTkSlider(
            master=self.parameters_frame,
            from_=10,
            to=1500,
            number_of_steps=1490,
            command=lambda value: self.slider_event(value)  # Вызываем метод
        )
        self.count_clones_label = CTkLabel(
            master=self.parameters_frame,
            text=f"Количество клонов: 0"
        )
        # 4
        self.mutation_slider = CTkSlider(
            master=self.parameters_frame,
            from_=10,
            to=1500,
            number_of_steps=1490,
            command=lambda value: self.slider_event(value)  # Вызываем метод
        )
        self.mutation_label = CTkLabel(
            master=self.parameters_frame,
            text=f"Вероятность мутации: 0"
        )
        # 5
        self.accuracy_slider = CTkSlider(
            master=self.parameters_frame,
            from_=10,
            to=1500,
            number_of_steps=1490,
            command=lambda value: self.slider_event(value)  # Вызываем метод
        )
        self.accuracy_label = CTkLabel(
            master=self.parameters_frame,
            text=f"Минимальная точность: "
        )
        self.parameters_label.pack(anchor="center", pady=10)
        self.population_slider.pack(anchor="center", pady=(15, 0))
        self.population_label.pack(anchor="center")
        self.iteration_slider.pack(anchor="center", pady=(15, 0))
        self.iteration_label.pack(anchor="center")
        self.count_clones_slider.pack(anchor="center", pady=(15, 0))
        self.count_clones_label.pack(anchor="center")
        self.mutation_slider.pack(anchor="center", pady=(15, 0))
        self.mutation_label.pack(anchor="center")
        self.accuracy_slider.pack(anchor="center", pady=(15, 0))
        self.accuracy_label.pack(anchor="center")
        self.parameters_frame.grid(row=2, pady=20)

        self.start_learning_button = CTkButton(
            master=self.right_frame,
            text="Начать обучение",
            command=self.start_learning_button,
            fg_color="#2C2C2C",
            text_color="#F5F5F5",
            width=425,
            height=40,
        )
        self.start_learning_button.grid(row=3, pady=(20, 0))


if __name__ == "__main__":
    app = Application()
    app.mainloop()
