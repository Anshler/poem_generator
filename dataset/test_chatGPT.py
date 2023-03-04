import time
from pyChatGPT import ChatGPT
import json
import os
import pandas as pd

def data_cleaning(text):
    text = text.replace('chu','chữ')
    text = text.replace('luc bat','lục bát')
    return text
def prompt_cleaning(text):
    text = text.replace('\nhoặc','')
    text = text.replace('\nHoặc', '')
    text = text.replace('\n', '')
    if text[0] == "\"":
        text = text[1:-1]
    return text

dataset = pd.read_csv("poems_dataset.csv")
dataset['genre'] = dataset['genre'].apply(lambda x: data_cleaning(x))

#ChatGPT
session_token = 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..1cL5NaNoVQ9p6Nzt.a94LvogSxzTaWEVu7GsFmSCfRrtgWLSuKsf56_2F2s5wA9YB6-TnKexrVIs4E8KmdB00eEd4dN4escciyYoEFojgFuFZwszMUIminvOuawH9a8wChMMLD5suHgAdqQ1wx726vBHvyBxJblZ4GkhhyrjGVk1yU9iXRMM-yXp_QiOuhpYTpvu8dlBRCP-72WEdg4I_ppRh5y1zGSZfO9wHhFh8Un0VpmKCXedHc3l9zXVzR8pKnMOO9a-_PZTaes-JQLgjYHhSxplInxTvcZ01Lpm3jGNN2LviCAhsncHYt9XIAk9TRvb4_I02WN_pujccoyTkOp8WcQvEeN80Lav-0ygGZ_7bCvg7GwxviNNYfOuWHcqAKGhW4wlUOKlCE3LeXelpL41D-BE4IFZyHIsQwNORaYpUcsHFSoPh8czvc8IGy4WenoXb4WvVhIHNiQQX1GN9VtUB6LbYKPK4yaka7lNgo-s-hDRmWGcr4d6LHSkoobgUnwNk68M_EpfPJjMqSfA-NsmBo_t-_qcoYy7dBSRrfqokgtdbpunRlVef_lrEb7tAmgPNLFnuyTAQV9k3Etg4169m9QxGf6PTZ5fd17hEM4b-EizAo3cKQGcc9B4Tz55ZC5A_VmpXe3wyERiDxohZQ7p_oL0mlXElkqRvj7DWzMjQ5E-eyN3i0B-iyHeWK7DhXdutfSZPo-4i5ZsZvAX0uUlnU9MdmzofWID9gd4LtEw5i3_MR40DEBzaGqG48qAZ7oBqzhxYP2Xl85broSBT1n1rl9QMvtp3BlUJ1zMSyXm4LlhQ3k-Du51TxZ5KCslqgPsuTmcl1Hsdrr6AykwgLWI-QXcCIS7sgn7UrPyx9S_idmin-ElREZ79kOxsyR1zxlh6iexLnoDjjP1IFIWE4QBhrlEcXvN2zABpWCrZY-ecUZ3roz7GZX_YYhmHn18dA7pQ-bhhkZrIjJPSPhcjkoKt1tfLoF29j6EHCfQRkqYPYM9eG9j6FYGrEE3Tbge2U72Z4c9vzy0nGZOaPylkoOCSpbR35zjXTlyIyp-9QqLoepTfd3JGA11HlXd26l7b0Ad0XYSeRTdTaABxxnQl71mhILkSYmiBuyQAAi2mEt3a4qexMoXQ6NCAZKXfgnEelogjaplgYqm295SbE00rM_JP0CNWuNS0OMf-w-vEDQ4yuI2DuJ3MZLO_PpkaBcOGubKZnQ7m59QFis8GK1p_nGtxCGArap-QjZgdBxIjS_SOhGoO1dyez-wvBBNNX-8DEcc-eSbU7tkxYuMVZr8oVbgZLDAxsD7AH3qGO5Tim3I_6tHYeDgiYPd5aUwcXPJaXNUMXDcr_buNbcaNiMAxGpCuzvLQz5apmhUYt1ng5-q06v-AjWDTX2BzakWMypC47-FAV-wKCx1_r0kCY02vx_Y8MY0-yyRVMK6zaOnrj749cL6IiRVcONKsF0vQ4oYoUHOEreYs7NCuTM8-il1bgo06wLo6GyKdHCTzax-QD7rv9tS2sfwetJEdKV1l3iUC8yDRPzIuQE9MLl-fd2V95-ceIdJIeLe0Z_fK1y18mrkXvQM1D-PxtTBs-niyr8CLdqmqaR52AsxF8Q-vMBZuCdWFyUNmZu5ho5qr6OwT85oW1P2kDUnH1rDo5qqtuARGS2UCfIjIFOf5pJxMVQRsWjctR5owUsOzeAP7LodaOwVe-oqU1fJD4HRxIWFvUU8SUcRDzHur87yO42BxGXmCr_AArX5osyaQifYTQpnGQQp3p8wgmZNI0C7bnng07bZS4mEBiyRw6ib6Y2kjKeV6r7LKVZ9r3lq6AwbTVut_L9r2OReYPiRQXMjRc1pVd3y9pDOw212QymtATw6DbILTiOW3efH1remaxlh8n5mA9k3qCi_nwUvCVFYS8X0x4F1Sz1NeSFlyXkCd-Y3e4mQ5_SbGJgH9ycOXg5PU3GUV1tbjUS8yQiNr-TDU0hyw4gDUiULND8LDdOLJARbEvmaptSxJYMGAKGXeiNBTd_vLWzW58dMeQDvzM97lObyHmpKK78Y09L9RqsV-7UlFlceGERYHyFffu-9qQnDbpbjxCj61ytpg3_aUvKOJcDC4bbcMo7tV8sACw_XbeNcr-jC6LqqPOJoq9LB42LduhD7gHoE5Ua92rJ_pi431k9Ryb9oJtr3P-DTPoEDCD-LMqowgkP7FmTo3NeoisRLZ8aAmuc2ddVoR5xDvXQF2sv76AvD23C5lrHK7rzDLYvPKr0KX-IMtTiiK8jIrAP3WejK95C-40JsE4wbl3Vu5sFjpfQ8D24m1aoX3TFIYr_sus01LazZImjR9Lz42t1uvV485mcaT1DJFdALoZfWUM4rX0bUH5-2GShZTOFdMskgULrIPbWFRD6LPm-zPpojCRJ9M1EI_heiVKmbOlFLgnIwpDB0k_rhRSRu5kL8DqTnC1c_-PngdUaqUdSINWnDtVb-NQLlrB5llSUBarECJr0BqlWiUdW_2crmXeYfTNtRvfstsE1mY13s1bkG6G-bVixCz9ESCGjcQ7Mf7fBAW7c_nUEnNWXCWS1oSMxm0glTqt2EIPaj9MyWkaLaXJU9rdqo.QhfgXeuKWV-j8xut_n6Ssw'
api = ChatGPT(session_token)

current = 87523 # current index, whenever encounter error, restart from it
outfile = open("../dataset.json", "a", encoding='utf-8')
start = 0 # first prompt must be good, so chatgpt can base the latter prompts off of it
error = 0 # count consecutive error
resp = '' # initiate first response, in case of duplicate
while True:
    try:
        for index, poem in dataset[current:].iterrows():
            print(index)
            current = index
            # ----Limit Poem Length (chatGPT can't handle too long)----
            new_poem = poem['content'].split('\n')
            new_poem = '\n'.join(new_poem[:19]) # 4 paragraphs, or 19 lines
            # -----------------------------------------PROMPT------------------------------------------------
            prompt = """
            Tôi có một bài thơ và cần tạo prompt làm input để train một language model để tạo ra bài thơ. Làm theo một trong hai cách sau:
            - Tóm gọn bài thơ thành văn xuôi, sử dụng câu từ khác bài thơ nhưng giữ càng nhiều ý chính càng tốt. Có thể trích dẫn 1-5 chữ hoặc câu từ bài thơ, ví dụ như: "có chứa từ khóa "xyz"". Bắt đầu với "Prompt: Viết một bài thơ %s về"
            - Tóm gọn bài thơ thành một câu ngắn dưới 20 chữ. Bắt đầu với "Prompt: Viết một bài thơ". (Có thể nêu rõ bài thơ thuộc thể thơ %s)
            
            Bài thơ là như sau:
    
            %s""" % (poem['genre'],poem['genre'], new_poem)
            # -----------------------------------------------------------------------------------------------
            old_resp = resp
            resp = api.send_message(prompt)
            if "Prompt:" not in resp['message']: # faulty response, not in format
                raise Exception('Faulty response')
            if start == 0 and len(resp['message'].split('Prompt:'))>2: # multiple prompts -> bad start
                raise Exception('Bad start')
            if old_resp == resp: # response somehow got duped, new poem got same response as previous
                raise Exception('Dupe response')
            start = 1
            error = 0
            # ----------------------------------------OUTPUT-------------------------------------------------
            print(resp['message'])
            message = prompt_cleaning(resp['message'].split('Prompt:')[1].strip()) # post processing
            data = {"prompt":message, "completion":poem['content']}
            json.dump(data, outfile)
            outfile.write('\n')

            # reset the conversation
            api.reset_conversation()
    except Exception as e:
        error += 1
        print(e)
        # cooldown
        if 'Too many requests' in str(e): # Too many requests in 1 hour. Try again later.
            print('30m cooldown from current index...')
            time.sleep(1800)
        else:
            print('60s cooldown from current index...')
            time.sleep(60)
        # ---------------------------------Refresh or start new window--------------------------------------
        if error == 5:
            os.system("taskkill /im chrome.exe /f") # close chrome window
            time.sleep(1)
            api = ChatGPT(session_token) # open new window
            error = 0
        else:
            api.refresh_chat_page()  # refresh chat page
        start = 0
        continue
    break