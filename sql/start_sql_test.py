import subprocess
import os

def run_tests():
    """
    Автоматически запускает тесты с помощью pytest и сохраняет результат в лог-файл.
    """
    test_file = "sql_test.py"
    
    log_file = "test_results.log"

    try:
        if not os.path.exists(test_file):
            raise FileNotFoundError(f"Файл {test_file} не найден.")

        print(f"Запуск тестов из файла {test_file}...")
        result = subprocess.run(
            ["pytest", "-s", test_file], 
            capture_output=True,         
            text=True,        
            check=True                   
        )

        with open(log_file, "w", encoding="utf-8") as log:
            log.write(result.stdout)
        print("Тесты выполнены успешно.")
        print(result.stdout)  

    except subprocess.CalledProcessError as e:
        print("Ошибка выполнения тестов.")
        with open(log_file, "w", encoding="utf-8") as log:
            log.write(e.stdout or "No stdout output.\n")
            log.write(e.stderr or "No stderr output.\n")
        print(e.stdout)  
        print(e.stderr)  

    except FileNotFoundError as e:
        print(e)

if __name__ == "__main__":
    run_tests()