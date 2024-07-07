'''
Description: 
Author: sky
Date: 2024-07-07 09:57:18
LastEditTime: 2024-07-07 10:04:43
LastEditors: sky
'''
def read_white_list(file_path='./writelist.txt'):
    """
    读取指定文件，返回其中的有效行组成的列表。
    
    参数:
    - file_path (str): 白名单文件的路径，默认为'.writelist'。
    
    返回:
    - list: 包含有效行的列表。
    
    异常:
    - FileNotFoundError: 如果文件不存在。
    - IOError: 如果文件读取时发生错误。
    """
    try:
        with open(file_path, 'r') as file:
            white_list = [line.strip() for line in file if line.strip() and not line.startswith('#')]
        return white_list
    except FileNotFoundError:
        print(f"文件 {file_path} 不存在，请检查文件路径。")
        raise
    except IOError as e:
        print(f"读取文件 {file_path} 时发生错误：{e}")
        raise