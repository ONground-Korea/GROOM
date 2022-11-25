import os
import sys
import urllib.request
import json
import re
import unicodedata
from transformers import pipeline
import torch

THRESHOLD = 40
DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu") 

def main(text):
    client_id = "9O__9M4k3AUtPQAMmUsc" # 파파고 임시 Client ID
    client_secret = "Mf_Gyn2W54" # 파파고 임시 Client Secret

    summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=DEVICE)

    #text = """1. 빵의 한쪽 면에 버터를 바르고 뜨거운 프라이팬에 빵의 버터 면을 아래로 향하게 놓으세요.
    #2. 치즈를 위에 얹은 다음, 다른 빵 조각을 위에 올리세요.
    #3. 밑단이 살짝 갈색이 될 때까지 요리한 다음 뒤집으세요.
    #4. 치즈가 녹을 때까지 계속 요리하세요."""

    def preprocess_sentence(w):
        w = w.strip()

        # 약간 전처리
        w = re.sub(r"([?.!,¿])", r" \1 ", w)
        w = re.sub(r'[" "]+', " ", w)
        w = re.sub(r'[ |ㄱ-ㅎ|ㅏ-ㅣ]+', " ", w)

        w = w.strip()

        return w

    text = preprocess_sentence(text)

    encText = urllib.parse.quote(text)
    data = "source=ko&target=en&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        result = json.loads(response_body.decode('utf-8'))
        result = result['message']['result']['translatedText']
        
        if len(result) > THRESHOLD:
            result = summarizer(result, max_length=30, min_length=10, do_sample=False)[0]['summary_text']
        else:
            result = result
        
        return result
    else:
        return "Error Code:" + rescode

if __name__ == "__main__":
    main()