# Flask-SQLite3-Template

一个基于 Flask + SQLite3 的 API 模板。

本项目默认使用 Python 3.13，其他版本暂未测试。

## 功能特性
- **用户管理**：内置用户管理功能，包括用户注册、登录、认证等。
- **接口文档**：集成自动化生成的 API 文档。
- **随机用户头像**：通过集成随机图像库为用户生成头像。
- **多环境部署**：支持通过 Gunicorn 部署生产环境。

## 安装与使用

### 1. 克隆项目
```sh
git clone https://github.com/sky984-11/flask-sqlite3-template.git
cd flask-sqlite3-template
```

### 2. 创建虚拟环境
建议使用虚拟环境，避免包依赖冲突和对系统环境的干扰。
```sh
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate
```

### 3. 安装依赖模块
```sh
pip install -r requirements.txt
```

### 4. 运行项目
启动开发服务器：
```sh
python3 run.py
```
默认运行在 [http://127.0.0.1:5000](http://127.0.0.1:5000)。

访问自动生成的 API 文档：
[http://127.0.0.1:5000/apidocs/](http://127.0.0.1:5000/apidocs/)
![image](https://github.com/user-attachments/assets/5d882e88-0427-4898-9eb5-5e33947fe880)


## 文件结构说明

```plaintext
flask-sqlite3-template/
├── routes/                  # 存放路由函数
├── static/                  # 存放静态文件
├── utils/                   # 存放工具函数
├── .env                     # 开发环境和正式环境配置
├── config.py                # 配置文件
├── db.py                    # 数据库模型
├── README.md                # 项目说明文档
├── requirements.txt         # 项目依赖
├── router.py                # 路由入口文件
└── run.py                   # 项目入口
```

## 配置说明
可以通过 `config.py` 配置不同环境的参数，通过.env 文件来切换开发和生产环境。

- **开发环境**：
  - 默认使用 SQLite 数据库。
  - 启用 Flask Debug 模式。
- **生产环境**：
  - 配置 WSGI 服务器，如 Gunicorn。


## 部署
推荐使用 Gunicorn 部署生产环境：

```sh
gunicorn -w 4 -b 127.0.0.1:5000 run:app
```


## 贡献
如果您发现问题或希望新增功能，可以提交 Issue 或 Pull Request。

## 许可证
本项目基于 [MIT License](LICENSE) 开源。

