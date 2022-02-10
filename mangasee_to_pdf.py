from PyPDF2 import PdfFileMerger, PdfFileReader
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from PIL import Image
import requests, time, io, os

# main function
def start():

    # download image as png
    def download_image(download_path, url, file_name):
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, "wb") as f:
            image.save(f, "PNG")

    # convert png to pdf
    def png_to_pdf(file_path):
        image1 = Image.open(file_path + ".png")
        image_converted = image1.convert("RGB")
        image_converted.save(file_path + ".pdf")
        os.remove(file_path + ".png")

    # create merged pdf file from pdfs
    def merge_pdfs(source_links_list, file_path, manga_request, chapter_request):
        merged_file = PdfFileMerger()
        
        for num in range(1, len(source_links_list) + 1):
            merged_file.append(PdfFileReader(file_path + str(num) + ".pdf", "rb"))
            os.remove(file_path + str(num) + ".pdf")

        merged_file.write(file_path + "COMPLETED" + ".pdf")


    # path (can be changed)
    direct_file_path = input("Path to save files at: ")

    # manga and chapter input
    manga_request = input("What manga would you like?: ")
    chapter_request = input("What chapter would you like?: ")

    # timer starts
    start_time = time.time()

    # firefox webdriver init.
    driver = webdriver.Firefox()

    # goes to website
    driver.get('https://mangasee123.com/')

    # types manga name in search-box
    search_bar = driver.find_element(By.CLASS_NAME, "form-control")
    time.sleep(1)
    search_bar.send_keys(manga_request + Keys.RETURN)
    time.sleep(1)

    # gets reading url of manga and ch.
    main_manga_url = driver.current_url 
    sections = main_manga_url.split("/")
    reading_url = f"https://mangasee123.com/read-online/{sections[-1]}-chapter-{chapter_request}.html"

    # prints reading url (not needed)
    print("\n" + reading_url)

    # goes to reading url
    driver.get(reading_url)

    # creats a list of source img links
    source_links_list = driver.find_elements(By.CLASS_NAME, "img-fluid")
    print("\nTotal images: " + str(len(source_links_list)))
    links = []
    for source in source_links_list:
        link = source.get_attribute("src")
        links.append(link)

    # download img, give it a name and convert
    num = 1
    for i in links:
        download_image(direct_file_path, i, f"{manga_request}-{chapter_request}-{num}.png")
        png_to_pdf(direct_file_path + f"{manga_request}-{chapter_request}-{num}")
        num += 1

    # merge all pdfs
    merge_pdfs(source_links_list, direct_file_path + f"{manga_request}-{chapter_request}-", manga_request, chapter_request)

    # quit firefox, stop timer
    time.sleep(2)
    driver.quit()
    stop_time = time.time()
    total_time = stop_time - start_time
    print(f"\nSCRAPE SUCCESSFUL, TIME ELAPSED: {str(round(total_time))} seconds\n")


# start if not imported
if __name__ == "__main__":
    start()

