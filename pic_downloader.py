import requests, os
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from selenium import webdriver


#Ссылка на страницу
url = ""
# Папка сохранения
fol = ""



def get_url_img():
    driver = webdriver.Firefox()
    driver.get(url)
    order = 1
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    file_links = soup.find_all('img')
    for i in file_links:
        file_url = i.get('src') or i.get('href')

        """
        Отмените комментарий, и подставьте остаток кода под условие, если вам нужно 
        скачать только изображения с определённым окончаниям, а не все со страницы
        """

        #if file_url and file_url.endswith('.webp'):
        download_and_convert(file_url, order)
        order += 1


def download_and_convert(url, order, output_format="PNG", quality=90):
    """
    Скачивает изображение и конвертирует в указанный формат.
    :param url: URL изображения
    :param order: Порядок сохранения изображения
    :param output_format: Формат для сохранения (PNG, JPEG, WEBP)
    :param quality: Качество (1-100) (Не применимо для PNG)
    """
    #Путь сохранения, по умолчанию сохранения в папку с проектом.
    folder = 'downloads/' + fol
    os.makedirs(folder, exist_ok=True)

    try:
        # Скачивание
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Загрузка в Pillow и конвертация
        with Image.open(BytesIO(response.content)) as img:
            # Формируем имя файла
            filename = os.path.join(
                folder,
                f"{order}.{output_format.lower()}"
            )

            # Сохранение в нужном формате
            img.save(filename, format=output_format, quality=quality)

        return filename

    except Exception as e:
        print(f"Ошибка при обработке {url}: {e}")
        return None


get_url_img()