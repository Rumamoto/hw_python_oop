class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(
            self, training_type: str,
            duration: float, distance: float,
            speed: float, calories: float) -> None:

        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> None:
        return (f"Тип тренировки: {self.training_type}; "
                f"Длительность: {self.duration:.3f} ч.; "
                f"Дистанция: {self.distance:.3f} км; "
                f"Ср. скорость: {self.speed:.3f} км/ч; "
                f"Потрачено ккал: {self.calories:.3f}.")


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOURS: int = 60

    def __init__(self,
                 # количество совершённых действий (число шагов при ходьбе и
                 # беге либо гребков — при плавании)
                 action: int,
                 duration: float,  # длительность тренировки
                 weight: float,  # вес спортсмена
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    # расчёт дистанции, которую пользователь преодолел за тренировку
    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):  # Бег
    run_coeff_calorie_1 = 18
    run_coeff_calorie_2 = 20

    def get_spent_calories(self) -> float:
        return ((self.run_coeff_calorie_1 *
                 self.get_mean_speed()
                 - self.run_coeff_calorie_2) *
                self.weight
                / self.M_IN_KM
                * self.duration
                * self.MIN_IN_HOURS)
    """Тренировка: бег."""


class SportsWalking(Training):  # Спортивная ходьба
    wlk_coeff_calorie_1 = 0.035
    wlk_coeff_calorie_2 = 0.029

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.wlk_coeff_calorie_1 *
                 self.weight
                 + (self.get_mean_speed()**2
                    // self.height) *
                 self.wlk_coeff_calorie_2
                 * self.weight) *
                self.duration
                * self.MIN_IN_HOURS)
    """Тренировка: спортивная ходьба."""


class Swimming(Training):
    LEN_STEP = 1.38  # переопределение длины гребка, вместо длины шага

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            length_pool: float,
            count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_spent_calories(self) -> float:
        swm_coeff_calorie_1 = 1.1
        swm_coeff_calorie_2 = 2
        return (
            (self.get_mean_speed() + swm_coeff_calorie_1)
            * swm_coeff_calorie_2 * self.weight
        )  # Формула для расчёта израсходованных калорий

    def get_mean_speed(self) -> float:
        # lenght_pool  Длина бассейна в метрах
        # count_pool  сколько раз пользователь переплыл бассейн
        return (
            self.length_pool * self.count_pool / self.M_IN_KM
            / self.duration
        )  # Формула расчёта средней скорости при плавании
    """Тренировка: плавание."""


def read_package(workout_type: str, data: list) -> Training:
    training_dict = {"SWM": Swimming,
                     "RUN": Running,
                     "WLK": SportsWalking}
    if workout_type not in training_dict:
        raise ValueError(f'Тип тренировки {workout_type} не определен.')
    return training_dict[workout_type](*data)
    """Прочитать данные полученные от датчиков."""


def main(training: Training):
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
