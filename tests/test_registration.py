import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users


@pytest.fixture(scope="module")
def setup_database():
    """Фикстура для настройки базы данных перед тестами и её очистки после."""
    create_db()
    yield
    os.remove('users.db')


def test_create_db(setup_database):
    """Тест создания базы данных и таблицы пользователей."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Таблица 'users' должна существовать в базе данных."


def test_add_new_user(setup_database):
    """Тест добавления нового пользователя."""
    assert add_user('testuser', 'testuser@example.com', 'password123') == True


def test_add_existing_user(setup_database):
    """Тест попытки добавления пользователя с существующим логином."""
    add_user('testuser2', 'testuser2@example.com', 'password123')
    assert add_user('testuser2', 'testuser2@example.com',
                    'password123') == False


def test_authenticate_user_success(setup_database):
    """Тест успешной аутентификации пользователя."""
    add_user('auth_user', 'auth@example.com', 'password123')
    assert authenticate_user('auth_user', 'password123') == True


def test_authenticate_user_failure(setup_database):
    """Тест неудачной аутентификации пользователя (неверные данные)."""
    assert authenticate_user('nonexistent_user', 'no_password') == False


def test_authenticate_user_wrong_password(setup_database):
    """Тест аутентификации с неправильным паролем."""
    add_user('user_wrong_pass', 'userwrong@example.com', 'correct_password')
    assert authenticate_user('user_wrong_pass', 'wrong_password') == False


def test_display_users(setup_database, capsys):
    """Тест отображения списка пользователей."""
    add_user('display1', 'display1@example.com', 'pass1')
    add_user('display2', 'display2@example.com', 'pass2')
    display_users()
    captured = capsys.readouterr()
    assert "Логин: display1, Электронная почта: display1@example.com" in captured.out
    assert "Логин: display2, Электронная почта: display2@example.com" in captured.out

# Если ты используешь функции для интерактивного ввода, тебе понадобится мокать input и проверять функции main и user_choice.

# Возможные варианты тестов тут:
"""
Тест добавления пользователя с существующим логином.
Тест успешной аутентификации пользователя.
Тест аутентификации несуществующего пользователя.
Тест аутентификации пользователя с неправильным паролем.
Тест отображения списка пользователей.
"""