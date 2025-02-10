import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import io.github.katalium.driver.KataliumDriver;

public class TestClass {

    public static void main(String[] args) {
        // Укажите путь к вашему ChromeDriver
        System.setProperty("webdriver.chrome.driver", "path/to/chromedriver");

        // Создание экземпляра Chrome WebDriver
        WebDriver driver = new ChromeDriver();

        // Пример использования Katalium
        KataliumDriver kataliumDriver = new KataliumDriver(driver);

        driver.get("https://www.example.com");
        // Ваши тестовые действия

        // Закрыть браузер
        driver.quit();
    }
}
