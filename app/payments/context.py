import threading
from contextlib import contextmanager

from app.utils import send_tg_notify

_thread_local = threading.local()


def get_write_off_context():
    return getattr(_thread_local, 'write_off_context', None)


def set_write_off_context(ctx):
    _thread_local.write_off_context = ctx


def report_write_off(user, amount, description=None):
    ctx = get_write_off_context()
    if ctx is not None:
        ctx.write_offs.append({
            'user': user,
            'amount': amount,
            'description': description,
        })
        return True
    return False


@contextmanager
def aggregate_write_offs():
    ctx = type('Context', (), {'write_offs': []})()
    set_write_off_context(ctx)
    try:
        yield ctx
    finally:
        set_write_off_context(None)
        if ctx.write_offs:
            total = sum(w['amount'] for w in ctx.write_offs)
            user = ctx.write_offs[0]['user']
            send_tg_notify(
                f"Списание средств (агрегировано)\n"
                f"Пользователь: {user.username}\n"
                f"Количество операций: {len(ctx.write_offs)}\n"
                f"Общая сумма: {total} RUB\n"
                f"Баланс: {user.balance} RUB"
            )
