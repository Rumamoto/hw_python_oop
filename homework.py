class InfoMessage:
    def __init__(
            self, training_type,
            duration, distance,
            speed, calories) -> None:

        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f"Тип тренировки: {self.training_type};"
                f"Длительность: {self.duration:.3f} ч.;"
                f"Дистанция: {self.distance:.3f} км;"
                f"Ср. скорость: {self.speed:.3f} км/ч;"
                f"Потрачено ккал: {self.calories:.3f}.;")

    """Информационное сообщение о тренировке."""
    pass


class Training:
    LEN_STEP: float = 0.65  # расстояние, которое преодолевает за один шаг или гребок
    M_IN_KM: int = 1000  # константа перевода из метров в километры
    """Базовый класс тренировки."""

    def __init__(self, action: int,  # количество совершённых действий (число шагов при ходьбе и беге либо гребков — при плавании)
                 duration: float,  # длительность тренировки
                 weight: float,  # вес спортсмена
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    # расчёт дистанции, которую пользователь преодолел за тренировку
    def get_distance(self) -> float:
        return self.action * Training.LEN_STEP / Training.M_IN_KM
        """Получить дистанцию в км."""

    def get_mean_speed(self) -> float:
        return self.get_distance / self.duration
        """Получить среднюю скорость движения."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        return InfoMessage
        """Вернуть информационное сообщение о выполненной тренировке."""


class Running(Training):  # Бег
    def get_spent_calories(self):
        run_coeff_calorie_1 = 18
        run_coeff_calorie_2 = 20
        return (
            (run_coeff_calorie_1 * self.get_mean_speed - run_coeff_calorie_2)
            * self.weight / self.M_IN_KM * self.duration
        )
    """Тренировка: бег."""


class SportsWalking(Training):  # Спортивная ходьба
    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        wlk_coeff_calorie_1 = 0.035
        wlk_coeff_calorie_2 = 0.029
        return (
            (wlk_coeff_calorie_1 * + (self.get_mean_speed**2 // self.height)
             * wlk_coeff_calorie_2 * self.weight) * self.duration
        )
    """Тренировка: спортивная ходьба."""


class Swimming(Training):
    def __init__(self, action, duration, weight, lenght_pool, count_pool):
        super().__init__(action, duration, weight)
        self.lenght_pool = lenght_pool
        self.count_pool = count_pool

    def get_spend_calories(self):
        swm_coeff_calorie_1 = 1.1
        swm_coeff_calorie_2 = 2
        return (
            (self.get_mean_speed + swm_coeff_calorie_1)
            * swm_coeff_calorie_2 * self.weight
        )  # Формула для расчёта израсходованных калорий

    def get_mean_speed(self):
        # lenght_pool  Длина бассейна в метрах
        # count_pool  сколько раз пользователь переплыл бассейн
        return (
            self.lenght_pool * self.count_pool / self.M_IN_KM
            / self.duration
        )  # Формула расчёта средней скорости при плавании
    """Тренировка: плавание."""


def read_package(workout_type: str, data: list) -> Training:
    training_dict = {"SWM": Swimming,
                     "RUN": Running,
                     "WLK": SportsWalking}
    return training_dict[workout_type](*data)
    """Прочитать данные полученные от датчиков."""


def main(training: Training) -> None:
    info = training.show_training_info()
    print(info.get_message())
    """Главная функция."""


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
