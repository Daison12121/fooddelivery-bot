import subprocess
import sys
import os

def test_production_locally():
    print("🧪 Тестирование продакшн версии локально...")
    
    # Устанавливаем переменные окружения для тестирования
    os.environ["TELEGRAM_BOT_TOKEN"] = "7942867452:AAHUPUnZaKiH-U90hFdnU4Zr3xPlAMBmEh8"
    os.environ["SECRET_KEY"] = "test-secret-key"
    os.environ["DEBUG"] = "False"
    
    print("✅ Переменные окружения установлены")
    
    # Запускаем продакшн версию бота
    print("🤖 Запуск продакшн версии бота...")
    try:
        subprocess.run([sys.executable, "bot_production.py"], check=True)
    except KeyboardInterrupt:
        print("\n⏹️ Остановлено пользователем")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    test_production_locally()
