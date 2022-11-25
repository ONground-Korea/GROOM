import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import io
from urllib import request
from PIL import Image
from webdriver_manager.chrome import ChromeDriverManager
import bart_large_cnn

def main(prompt):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')        # Head-less 설정
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    url = 'https://stabilityai-stable-diffusion-1.hf.space/?__theme=light/'
    driver.get(url)
    # document in stable diffusion

    def expand_shadow_element(element):
        shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
        return shadow_root

    root1 = driver.find_element(By.TAG_NAME, 'gradio-app')
    shadow_root1 = expand_shadow_element(root1)
    # shadow-root in url

    shadow_root1.find_element(By.CSS_SELECTOR, "[data-testid='textbox']").click()
    elem = shadow_root1.find_element(By.CSS_SELECTOR, "[data-testid='textbox']")
    # prompt box

    preprocess_prompt = bart_large_cnn.main(prompt)
    print(f'preprocess_prompt: {preprocess_prompt}')

    prompt_chunk = [preprocess_prompt[i:i+64] for i in range(0, len(preprocess_prompt), 64)]

    for chunk in prompt_chunk:
        elem.send_keys(chunk)
    #elem.send_keys(preprocess_prompt)
    shadow_root1.find_element(By.ID, "component-6").click()
    # prompt box에 prompt 넣고 button click

    imgs = shadow_root1.find_elements(By.CSS_SELECTOR, "[alt]")

    while not len(imgs) > 4:
        imgs = shadow_root1.find_elements(By.CSS_SELECTOR, "[alt]")
        # 사진 뜰 때까지 태그 검색

    output = [0 for i in range(4)]

    for i in range(4):
        url = imgs[i].get_attribute('src')
        res = request.urlopen(url).read()
        output[i] = Image.open(io.BytesIO(res))

        output[i].save("./static/images/output" + str(i+1) + ".jpg", 'JPEG')



if __name__ == "__main__":
    main()