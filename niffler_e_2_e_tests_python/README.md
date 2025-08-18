Перед запуском тестов создать нового пользователя:
aslavret
12345

[//]: # (Как запускать тесты:)

[//]: # ()
[//]: # (Для Windows &#40;CMD/PowerShell&#41;:)

[//]: # (cmd)

[//]: # (cd niffler-py-st3\niffler_e_2_e_tests_python)

[//]: # (python -m pytest tests\test_categories.py & ^)

[//]: # (python -m pytest tests\test_login.py & ^)

[//]: # (python -m pytest tests\test_profile.py & ^)

[//]: # (python -m pytest tests\test_register.py & ^)

[//]: # (python -m pytest tests\test_spending.py)

[//]: # ()
[//]: # ()
[//]: # (Для Linux/MacOS:)

[//]: # (bash)

[//]: # (cd niffler-py-st3\niffler_e_2_e_tests_python)

[//]: # (python -m pytest tests/test_categories.py; \)

[//]: # (python -m pytest tests/test_login.py; \)

[//]: # (python -m pytest tests/test_profile.py; \)

[//]: # (python -m pytest tests/test_register.py; \)

[//]: # (python -m pytest tests/test_spending.py)

**Как запускать тесты:**

python -m pytest tests --alluredir=allure-results 
allure serve allure-results
