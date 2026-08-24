from rest_framework.exceptions import ValidationError


def validate_habit(data):
    """
    Общая валидация привычки.

    Проверяет:
    - нельзя одновременно reward и related_habit;
    - выполнение не больше 120 секунд;
    - связанная привычка должна быть приятной;
    - приятная привычка не может иметь reward или related_habit;
    - периодичность не больше 7 дней.
    """

    reward = data.get("reward")
    related_habit = data.get("related_habit")
    is_pleasant = data.get("is_pleasant", False)
    execution_time = data.get("execution_time")
    period = data.get("period", 1)

    errors = {}

    # Нельзя одновременно указывать награду и связанную привычку
    if reward and related_habit:
        errors["reward"] = (
            "Нельзя одновременно указывать вознаграждение " "и связанную привычку."
        )

    # Время выполнения не больше 120 секунд
    if execution_time is not None and execution_time > 120:
        errors["execution_time"] = "Время выполнения не должно превышать 120 секунд."

    # Связанная привычка должна быть приятной
    if related_habit and not related_habit.is_pleasant:
        errors["related_habit"] = (
            "В связанные привычки можно добавлять " "только приятные привычки."
        )

    # У приятной привычки не может быть награды или связанной привычки
    if is_pleasant and (reward or related_habit):
        errors["is_pleasant"] = (
            "Приятная привычка не может иметь " "вознаграждение или связанную привычку."
        )

    # Нельзя выполнять реже одного раза в 7 дней
    if period > 7:
        errors["period"] = "Периодичность не может быть больше 7 дней."

    if errors:
        raise ValidationError(errors)
