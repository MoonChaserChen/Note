import codecs
import os


def append_file_content(_from, _to):
    """
    将 _from 文件的内容 复制到 _to 文件
    """
    if not os.path.isfile(_from) or not os.path.isfile(_from):
        return
    f_f = codecs.open(_from, 'r', encoding='utf-8')
    t_f = codecs.open(_to, 'a', encoding='utf-8')
    t_f.write("\n")
    t_f.writelines(f_f.readlines())
    f_f.close()
    t_f.close()
