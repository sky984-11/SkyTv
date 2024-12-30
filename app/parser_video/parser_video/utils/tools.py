'''
Description: 
Author: sky
Date: 2024-07-07 09:57:18
LastEditTime: 2024-07-20 17:52:40
LastEditors: sky
'''
import yaml

def read_white_list(file_path='./writelist.yaml'):
    """
    读取 YAML 文件并转换为元组迭代器，每个元组包含影视作品名称和类型。
    
    参数:
    - file_path (str): YAML 文件的路径。
    
    返回:
    - generator: 形如 ((名称, 类型), ...) 的元组迭代器。
    """
    try:
        with open(file_path, 'r') as file:
            white_list_data = yaml.safe_load(file)
            for category, items in white_list_data.items():
                for item in items:
                    yield (item, category)
    except FileNotFoundError:
        print(f"文件 {file_path} 不存在，请检查文件路径。")
        raise
    except yaml.YAMLError as exc:
        print(f"解析 YAML 文件 {file_path} 时发生错误：{exc}")
        raise