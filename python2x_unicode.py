# -*- coding: utf-8 -*-
"""
@ author:        Chien Chun
@ description:   以下範例僅適用於 Python 2.x ，Python 3.x 沒有這些問題。
@ reference:
此範例只節錄了部分基本觀念，關於 Python 2.x 的編碼機制建議閱讀下面這兩篇連結。
[Unicode In Python, Completely Demystified](http://farmdev.com/talks/unicode/)
[Python UnicodeDecodeError - Am I misunderstanding encode?](http://stackoverflow.com/questions/368805/python-unicodedecodeerror-am-i-misunderstanding-encode#370199)
"""
def main():
    # 了解 python 2.x 中，「unicode 型態字串」與 「str 型態字串」的不同
    unicode_vs_str_object()
    # 讀取檔案時，預設會以「str 型態」讀進資料
    read_file_default()
    # 用 codecs module 讀寫檔案時可指定 encoding，可以「unicode 型態」讀進資料
    read_file_with_codecs()
    # 用不同 module 對資料做處理時，可能改變其型態（例如 json）
    read_json()
    # 結論：  1. Decode early   2. Unicode everywhere   3. Encode late
    conclusion()
    # python 的 encode() 和 decode() 也能用來轉換其他編碼
    other_usage()


def unicode_vs_str_object():
    print '\nunicode_vs_str_object()'

    # 建立一個內容為 '金城武' 的 python 「str 物件」
    str_name = '金城武'
    print '1', str_name, type(str_name)
    # 1 金城武 <type 'str'>

    # 藉由在字串前面加上 u ，建立一個內容為 '金城武' 的 python 「unicode 物件」
    uni_name = u'金城武'
    print '2', uni_name, type(uni_name)
    # 2 金城武 <type 'unicode'>

    """
    說明：
    此時 uni_name 的資料型態是 python 的 「unicode 物件」，並非「str 物件」
    故當對 uni_name 這個變數做 「str 物件」的操作時會出現錯誤
    （例如與另一個「str 物件」相加）：
    """
    # print str(uni_name)
    # 錯誤：UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-2: ordinal not in range(128)

    # print uni_name + "也略懂"
    # 錯誤：UnicodeEncodeError: 'ascii' codec can't decode byte 0xe6 in position 0: ordinal not in range(128)

    """
    我們可以對 uni_name 這個變數做「unicode 物件」操作
    （例如與另一個「unicode 物件」相加）：
    """
    print '3', uni_name + u"也略懂"
    # 3 金城武也略懂

    """
    相對的，str_name 是 python 「str 物件」，故做「str 物件」的操作時不會出現錯誤
    （例如與另一個「str 物件」相加）：
    """
    print '4', str_name + "也略懂"
    # 4 金城武也略懂

    """
    python 有個 method 叫做 encode([encoding_], [errors='strict'])
    這個方法可以將「unicode 物件」轉換成以 encoding_ 方式編碼的「str 物件」
    """
    # 剛剛的 uni_name 變數原本是 「unicode 物件」
    # 用 .encode('utf-8') 將其以 utf-8 編碼方式轉換為「str 物件」
    new_name = uni_name.encode('utf-8')
    print '5', new_name, type(new_name)
    # 5 金城武 <type 'str'>

    """
    new_name 已經是「str 物件」，做「str 物件」的操作時不會出現錯誤
    （例如與另一個「str 物件」相加）：
    """
    print '6', new_name + "略懂略懂"
    # 6 金城武略懂略懂

    # print '6', new_name + u"略懂略懂"
    # UnicodeDecodeError: 'ascii' codec can't decode byte 0xe9 in position 0: ordinal not in range(128)

    """
    同樣的道理，我們也可以用 decode([encoding_]) 將「str 物件」還原成「unicode 物件」
    """
    original_unicode_form = new_name.decode('utf-8')
    print '7', original_unicode_form, type(original_unicode_form)
    # 7 金城武 <type 'unicode'>

    # 之後就可對此變數「unicode 物件」操作（例如與另一個「unicode 物件」相加）
    print '8', original_unicode_form + u"略懂略懂"
    # 8 金城武略懂略懂

    # print '8', original_unicode_form + "略懂略懂"
    # UnicodeDecodeError: 'ascii' codec can't decode byte 0xe7 in position 0: ordinal not in range(128)

    """
    pyhton 的 「unicode 物件」除了在操作時不用擔心編碼問題外，
    也可以直接插入字元的 unicode code print，例如：
    """
    print '9', original_unicode_form + u"\u6211\u672C\u4EBA\u5566"
    # 9 金城武我本人啦

    # 註1. 在 python 中，以 "\uXXXX" 表示 unicode code print 的 U+XXXX，例如 '\u5566' 代表 U+5566
    # 註2. http://www.charbase.com/5566-unicode-cjk-unified-ideograph
    # 註3. \u6211 = 我, \u672C = 本, \u4EBA = 人, \u5566 = 啦

def read_file_default(file_name='lectures.txt'):
    """
    python 預設的讀檔方式會將資料讀取成 python 的「str 物件」型態
    """
    print '\nread_file_default()'
    with open(file_name, 'r') as file_handler:
        for line in file_handler:
            print line.rstrip(), type(line)
            # 出師表 <type 'str'>
            # 諸葛亮 <type 'str'>

def read_file_with_codecs(file_name='lectures.txt'):
    """
    import codecs 後，可善用 codecs.open(encoding) 的 encoding 參數，
    若設定正確，則 python 會自動在讀取資料時轉換成 python 的「unicode 物件」型態
    """
    print '\nread_file_with_codecs()'
    import codecs
    with codecs.open(file_name, 'r', encoding='utf-8') as file_handler:
        for line in file_handler:
            print line.rstrip(), type(line)
            # 出師表 <type 'unicode'>
            # 諸葛亮 <type 'unicode'>

def read_json(file_name='lectures.json'):
    """
    當使用 json.loads 讀取 json 資料時，回傳的結果會是「unicode 物件」型態
    """
    print '\nread_json()'

    import json
    with open(file_name, 'r') as file_handler:
        data = json.loads(file_handler.read())
        lectures = data['lectures']

        title  = lectures[0]['title']
        author = lectures[0]['author']
        print title, type(title)
        # 出師表 <type 'unicode'>
        print author, type(author)
        # 諸葛亮 <type 'unicode'>

def conclusion(file_in='lectures.txt', file_out='output.txt'):
    """
    As suggested in this slide:
    http://farmdev.com/talks/unicode/
        1. Decode early
        2. Unicode everywhere
        3. Encode late
    While using codecs.open(encoding) as a shortcut
    """
    import codecs
    with codecs.open(file_in, 'r', encoding='utf-8') as fin, codecs.open(file_out, 'w', encoding='utf-8') as fout:
        for line in fin:
            fout.write(line.rstrip() + u'不能亡\u5566\n')
            # 出師表不能亡啦
            # 諸葛亮不能亡啦
            # 註： '\u5566' 是 "啦"這個字的 unicode code print

def other_usage():
    """
    python 的 encode() 和 decode() 除了轉換 unicode 和 str 物件外，也能用來轉換其他編碼，例如 base64
    """
    print '\nother_usage()'

    str_name = '金城武'
    print str_name, type(str_name)
    # 金城武 <type 'str'>

    base64_name = str_name.encode('base64')
    print 'Base64 of', str_name, 'is', base64_name
    # Base64 of 金城武 is 6YeR5Z+O5q2m

    # print base64_name.decode('base64')
    # 金城武

if __name__ == '__main__':
    main()
