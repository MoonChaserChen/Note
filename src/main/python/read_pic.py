import cv2
import hashlib


def get_text(img):
    """
    图片转文本d（题目：https://b1.rippletek.com/games/bits-pic.html）
    :param img: 图片路径
    :return: 文本内容
    """
    img = cv2.imread(img, 1)
    # 将图片转换成的字节数组（最后会将此字节数组转换成文本）
    re_byte_array = bytearray()
    # 每8位解析成一个字节，这里用cnt进行循环计数
    cnt = 0
    # 连续8位的int值表示
    v = 0
    # 连续0的数量，达到4表示结束
    zero_cnt = 0
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            # rgb=(255,255,255)表示白色，即0；否则为1
            vt = 0 if (img[i, j] == [255, 255, 255]).all() else 1
            v = (v << 1) | vt
            if cnt == 7:
                re_byte_array.append(v)
                if v == 0:
                    zero_cnt += 1
                    if zero_cnt == 4:
                        return re_byte_array.decode("utf-8")
                else:
                    zero_cnt = 0
                v = 0
                cnt = 0
            else:
                cnt += 1
    return re_byte_array.decode("utf-8")


text = get_text('task.png')
print(text)
md5 = hashlib.md5()
md5.update(text.encode(encoding='utf-8'))
print(md5.hexdigest())
