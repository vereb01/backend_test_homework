from typing import List, Dict, Type



class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance:float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories
    def get_message(self):
        return  (f'Тип тренировки: {self.training_type}\n'
                 f'Длительность: {self.duration:.3f} ч.\n'
                 f'Дистанция: {self.distance:.3f} км\n'
                 f'Ср.скорость: {self.speed:.3f} км/ч\n'
                 f'Потрачено ккал: {self.calories:.3f}.\n'
                )

class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_IN_H: int = 60
    def __init__(self,
                 action: int, #количество совершённых действий (число шагов при ходьбе и беге либо гребков — при плавании)
                 duration: float, #длительность тренировки
                 weight: float, #вес спортсмена
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
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
        return InfoMessage(self.__class__.__name__,
                self.duration,
                self.get_distance(),
                self.get_mean_speed(),
                self.get_spent_calories()
                )
class Running(Training):
    """Тренировка: бег."""
    RUN_COEFF_1: int = 18
    RUN_COEFF_2: int = 20
    def get_spent_calories(self) -> float:
        return ((self.RUN_COEFF_1 * self.get_mean_speed()
             - self.RUN_COEFF_2) * self.weight
             / self.M_IN_KM * self.duration * self.MIN_IN_H)
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    SW_COEFF_1: float = 0.035
    SW_COEFF_2: float = 2
    SW_COEFF_3: float = 0.029
    def __init__(self,
        action: int,
        duration: float,
        weight: float,
        height: float
        ) -> None:
        super().__init__(action, duration, weight)
        self.height = height
    def get_spent_calories(self) -> float:
        return (self.SW_COEFF_1 * self.weight + (self.get_mean_speed()
                ** self.SW_COEFF_2 // self.height * self.SW_COEFF_3
                * self.weight) * self.duration)
class Swimming(Training):
    """Тренировка: плавание."""
    SWIM_COEFF_1: float = 1.1
    SWIM_COEFF_2: int  = 2
    LEN_STEP: float = 1.38
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
    def get_spent_calories(self):
        return (self.get_mean_speed() + self.SWIM_COEFF_1) * self.SWIM_COEFF_2 * self.weight
def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    telemetry: Dict[str, Type] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return telemetry[workout_type](*data)
def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())
if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)