# -*- coding: utf-8 -*-
"""
Created on Sat May  7 14:36:03 2022

tcup_html_converter.py

@author: odoruAFP   twitter @2022_busi_fp_j   or オドルAFP
"""
import urllib.parse
import os

# 掲示板へアクセスするためのURLの固有部分を指定します。
# 例）https://xxxx.teacup.com/yyyyyyyy/bbs/?
# のxxxxの数字と、yyyyyyyyの文字列をそれぞれ定数MY_BBS_NUM、MY_BBS_NAMEに指定してください。

MY_BBS_NAME = 'yyyyyyyy'                            #各掲示板固有の名称yyyyyyyyです
MY_BBS_NUM = str(100)                               #各掲示板固有の番号xxxxです
BREADCRUMBS_NUM = 10                                #パンくずリストの総数です
TOTAL_VOLUME_HTML_FILES = 100                       #バックアップを取ったhtmlファイルの数を指定します
MY_BBS_TITLE_HTML = '<P><h1>ZZZZZZZZZZZ</h1><br>'   #ブラウザで表示されるタイトル名を含むhtmlです

def conv_breadcrumbs(current_file_index:int):

    STR_1 = '<p><a href="'    
    STR_2 = '"><strong>《前のページ</strong></a>&nbsp;<a href="'
    STR_3 = '<p><span><strong>《前のページ</strong></span>&nbsp;<span><strong>'           #youngest_page_index 端部処理
    STR_4 = '"><strong>'
    STR_5 = '</strong></a>&nbsp;<span><strong>'
    STR_6 = '</strong></span>&nbsp;<a href="'
    STR_7 = '</strong></a>&nbsp;<a href="'
    STR_8 = '"><strong>次のページ》</strong></a>&nbsp;</p>'
    STR_9 = '</strong></span>&nbsp;<span><strong>次のページ》</strong></span>&nbsp;</p>'  #eldest_page_index 端部処理

    YOUNGER_OFFSET_VALUE    = BREADCRUMBS_NUM/2 - 1
    ELDER_OFFSET_VALUE      = BREADCRUMBS_NUM/2

    CUT_OFF_FILE_INDEX    = TOTAL_VOLUME_HTML_FILES - ELDER_OFFSET_VALUE
    SATURATION_FILE_INDEX = TOTAL_VOLUME_HTML_FILES - CUT_OFF_FILE_INDEX

    breadcrumbs_html = STR_1
    current_page_index  = TOTAL_VOLUME_HTML_FILES - current_file_index
    link_less_page_index = current_page_index

    if current_file_index < SATURATION_FILE_INDEX:
        youngest_page_index = TOTAL_VOLUME_HTML_FILES - BREADCRUMBS_NUM + 1

    elif (current_file_index >= SATURATION_FILE_INDEX) and (current_file_index <= CUT_OFF_FILE_INDEX):
        youngest_page_index = (TOTAL_VOLUME_HTML_FILES - YOUNGER_OFFSET_VALUE) - current_file_index
    
    else:
        youngest_page_index = 1

    if current_file_index != TOTAL_VOLUME_HTML_FILES - 1:
        previous_file_index = current_file_index + 1
        previous_file_name = MY_BBS_NAME + '_(' + str(int(previous_file_index)) .zfill(3)+ ').html'
        breadcrumbs_html = STR_1 + previous_file_name + STR_2
    else:
        previous_file_index = current_file_index
        breadcrumbs_html = STR_3        

    if current_file_index != 0:    
        next_file_index = current_file_index - 1
        next_file_name     = MY_BBS_NAME + '_(' + str(int(next_file_index)).zfill(3) + ').html'
    else:
        next_file_index = current_file_index
        next_file_name = 'nothing'

    previous_file_name = MY_BBS_NAME + '_(' + str(int(previous_file_index)).zfill(3)+ ').html'

    for i in range(10):
        breadcrumbs_file_index = -youngest_page_index + TOTAL_VOLUME_HTML_FILES - i
        breadcrumbs_file_name = MY_BBS_NAME + '_(' + str(int(breadcrumbs_file_index)) .zfill(3)+ ').html'       
        breadcrumbs_page_index = youngest_page_index + i
             
        if i==9 and current_page_index == TOTAL_VOLUME_HTML_FILES:  
            breadcrumbs_html = breadcrumbs_html +  str(int(breadcrumbs_page_index)) + STR_9
        elif i==9:
            breadcrumbs_html = breadcrumbs_html + breadcrumbs_file_name + STR_4 + str(int(breadcrumbs_page_index))+ STR_7 +  next_file_name + STR_8
        elif breadcrumbs_page_index == link_less_page_index - 1 :
            breadcrumbs_html = breadcrumbs_html + breadcrumbs_file_name + STR_4 + str(int(breadcrumbs_page_index)) + STR_5
        elif breadcrumbs_page_index != link_less_page_index:
            breadcrumbs_html = breadcrumbs_html + breadcrumbs_file_name + STR_4 + str(int(breadcrumbs_page_index)) + STR_7
        else:
            breadcrumbs_html = breadcrumbs_html +  str(int(breadcrumbs_page_index)) + STR_6

    return breadcrumbs_html

def conv_thumbnail_directory(data:str):
    str_replace_imgtag='<IMG BORDER="0" SRC="../image_library/thumbnails/'
    data = str_replace_imgtag + data[37:]
    
    return data

def conv_image_directory(data:str):
    str_replace_atag = '<A HREF="../image_library/'
    data= str_replace_atag + data[25:]
    
    return data

def decode_url_link(html_encoded_str:str):   
    to_find_a_tag_http_str = 'A HREF="/' + MY_BBS_NAME + '/bbs?M=JU&amp;JUR=http%3A%2F%2F'
    to_find_a_tag_https_str = 'A HREF="/' + MY_BBS_NAME + '/bbs?M=JU&amp;JUR=https%3A%2F%2F'
    to_find_a_tag_old_http_str = 'A HREF="http://' + MY_BBS_NUM + '.teacup.com/' + MY_BBS_NAME + '/bbs?M=JU&amp;JUR=http%3A%2F%2F'
       
    if to_find_a_tag_https_str in html_encoded_str:
        init_value_to_find = html_encoded_str.find(to_find_a_tag_https_str)
        shift_value = 33
    elif to_find_a_tag_http_str in html_encoded_str:
        init_value_to_find = html_encoded_str.find(to_find_a_tag_http_str)
        shift_value = 33
    else:
        init_value_to_find = html_encoded_str.find(to_find_a_tag_old_http_str)
        shift_value = 55        
        
    first_description = html_encoded_str[:init_value_to_find + 8]
    html_decoded_str = first_description + urllib.parse.unquote(html_encoded_str[init_value_to_find + shift_value:])

    return html_decoded_str

def conv_thread_directory(data:str):
    if '<li>◇<a href="/' + MY_BBS_NAME + '/bbs/t4/' in data:
        data = '<li>◇<a href="/' + MY_BBS_NAME + '_thread_(003).html"' + data[33:]
    elif '<li>◇<a href="/' + MY_BBS_NAME + '/bbs/t3/' in data:
        data = '<li>◇<a href="/' + MY_BBS_NAME + '_thread_(002).html"' + data[33:]
    elif '<li>◇<a href="/' + MY_BBS_NAME + '/bbs/t2/' in data:
        data = '<li>◇<a href="/' + MY_BBS_NAME + '_(001).html"' + data[33:]
    else:
        data = '<li>◇<a href="/' + MY_BBS_NAME + '_(000).html"' + data[33:]
        
    return data

def conv_return_bbs_directory(data:str):
    data = '<li><a href="' + MY_BBS_NAME + '_(' + TOTAL_VOLUME_HTML_FILES-1 + ').html">掲示板に戻る</a></li>'
    
    return data

def conv_html_title(data:str):
    if '</h1><br></P>' in data:
        data = '<P><h1>test</h1><br></P>'
    else:
        data = '<P><h1>test2</h1><br>'

    return data

for html_file_index in range(TOTAL_VOLUME_HTML_FILES):
    html_file_name = MY_BBS_NAME + '_(' + str(html_file_index) .zfill(3)+ ').html'
    print(html_file_name)
    f=open('./original_html/' + html_file_name ,'r', encoding='UTF-8')

    if not os.path.isfile('./converted_html/' + html_file_name):
        with open('./converted_html/' + html_file_name, mode='a', encoding='UTF-8') as f2:            
            while True:
                data=f.readline()
                if '<A HREF="/' + MY_BBS_NAME + '/img/bbs/' in data:
                    data = conv_image_directory(data)
                    f2.write(data)
                elif '<IMG BORDER="0" SRC="/' + MY_BBS_NAME + '/img/bbs/' in data:
                    data = conv_thumbnail_directory(data)
                    f2.write(data)
                elif 'pagination'  in data:
                    f2.write(data)
                    data=f.readline()
                    data = conv_breadcrumbs(html_file_index)
                    f2.write(data)
                elif '<A HREF="/' + MY_BBS_NAME + '/bbs?M=JU&amp;JUR=https%3A%2F%2F' in data:
                    data = decode_url_link(data)
                    f2.write(data)
                elif '<A HREF="/' + MY_BBS_NAME + '/bbs?M=JU&amp;JUR=http%3A%2F%2F' in data:
                    data = decode_url_link(data)
                    f2.write(data)
                elif '<A HREF="http://' + MY_BBS_NUM + '.teacup.com/' + MY_BBS_NAME + '/bbs?M=JU&amp;JUR=http%3A%2F%2F' in data:
                    data = decode_url_link(data)
                    f2.write(data)                
                elif '<li>◇<a href="/' + MY_BBS_NAME + '/bbs/t' in data:
                    data = conv_thread_directory(data)
                    f2.write(data)               
                elif '<li><a href="/' + MY_BBS_NAME + '/bbs">掲示板に戻る</a></li>' in data:
                    data = conv_return_bbs_directory(data)
                    f2.write(data)
                elif MY_BBS_TITLE_HTML in data:
                    data = conv_html_title(data)
                    f2.write(data)                
                elif data=="":
                    break
                else:
                    f2.write(data)
                        
    f.close()