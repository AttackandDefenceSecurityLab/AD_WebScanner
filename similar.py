dim = 75

'''
将url转化为特征向量后，计算url之间的余弦相似度
'''

def turn_num(url, length):
    '''
    转化为特征向量
    :param url: url
    :param length: 域名和协议的长度，我们只需要后面的部分，前面的部分每个url都一样，节省计算
    :return: url的特征向量
    '''
    url = url[length:]
    url = list("".join([j for j in url]))
    for i in range(0, len(url)):
        url[i] = ord(url[i])
    for i in range(len(url), dim):
        url.append(0)
    return url


def cos(vector1,vector2):
    '''
    余弦相似度计算
    :param vector1: url1
    :param vector2: url2
    :return: 相似度大小
    '''
    dot_product = 0.0
    normA = 0.0
    normB = 0.0
    for a,b in zip(vector1,vector2):
        dot_product += a*b
        normA += a**2
        normB += b**2
    if normA == 0.0 or normB==0.0:
        return None
    else:
        return dot_product / ((normA*normB)**0.5)


def similarities(data, url, length):
    '''
    将url与一组url比较相似度
    :param data: 数据集
    :param url: 目标url
    :param length: 长度
    :return: 判定结果
    '''
    url_list = [turn_num(i, length) for i in data]
    target_url = turn_num(url, length)
    for i in url_list:
        try:
            if cos(target_url, i) > 0.995:
                print('similar')
                return 1
        except:
            return 0
    return 0
