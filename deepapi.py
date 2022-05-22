import requests

def text_to_image(text: str):
    '''
    Входные параметры:
    text: str -- текст, по которому будет формироваться картинка

    Выходной результат:
    r.json() -- словарь вида
    {
        'id': id
        'output_url': ссылка на изображение
    }
    '''
    r = requests.post(
        "https://api.deepai.org/api/text2img",
        data={
            'text': text,
        },
        headers={'api-key': '84268f70-d9fd-4557-be37-a0603eff4056'}
    )
    return(r.json())
