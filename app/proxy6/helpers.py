





from app.utils import send_tg_notify


def send_not_enough_money_error(user, amount, operation):
    send_tg_notify(
        f"Не удалось списать средства с баланса пользователя: Недостаточно средств\n"
        f"Операция: {operation}\n"
        f"Пользователь: {user.username}\n"
        f"Сумма: {amount}\n"
        f"Баланс: {user.balance}"
    )


def send_prolong_error_notification(user, errors):
    error_lines = [f"- Proxy ID {pid}: {err}" for pid, err in errors]
    send_tg_notify(
        f"Ошибки продления прокси\n"
        f"Пользователь: {user.username}\n"
        f"Количество ошибок: {len(errors)}\n"
        + "\n".join(error_lines)
    )