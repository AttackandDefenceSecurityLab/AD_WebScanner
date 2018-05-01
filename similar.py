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

    char_index = [i for i in range(len(url)) if url[i] == '/']
    char_index.insert(0, 0)

    char_weight = []
    for i in range(len(char_index)):
        try:
            char_weight.append(url[char_index[i]:char_index[i + 1]])
        except:
            char_weight.append(url[char_index[i]:])

    num = len(char_weight)

    url_weight = [ord(j)*(num-i)*(num-i) for i in range(len(char_weight)) for j in char_weight[i]]

    for i in range(len(url_weight), dim):
        url_weight.append(0)
    return url_weight


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
            if cos(target_url, i) > 0.9995:
                print('similar')
                return 1
        except:
            return 0
    return 0

