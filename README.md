后端 README
项目概述
通讯录管理系统后端是一个基于Flask的RESTful API服务，提供联系人数据管理、导入导出功能和数据持久化存储。

技术栈
Python 3.8+ - 编程语言

Flask 2.3.x - Web框架

Flask-CORS - 跨域资源共享

Pandas 2.0+ - 数据处理和Excel操作

JSON - 数据存储格式

datetime - 时间处理

功能特性
已实现功能
联系人CRUD操作

创建、读取、更新、删除联系人

唯一ID自动生成

时间戳记录

收藏功能

切换联系人收藏状态

收藏状态持久化存储

数据持久化

JSON文件存储，无需数据库

自动数据初始化

数据备份和恢复

导入导出功能

导出联系人到Excel文件

从Excel文件导入联系人

支持.xlsx和.xls格式

API设计

RESTful风格API

统一的错误处理

跨域资源共享支持

项目结构
text
backend/
├── app.py              # Flask应用主文件
├── contacts.json       # 数据存储文件（自动生成）
├── requirements.txt    # Python依赖包列表
├── config.py          # 配置文件（可选）
├── utils.py           # 工具函数（可选）
└── README.md          # 后端文档
文件说明
app.py
Flask应用主文件，包含以下主要部分：

初始化配置
python
app = Flask(__name__)
CORS(app)  # 允许跨域请求
CONTACTS_FILE = 'contacts.json'  # 数据文件路径
数据初始化函数
python
def init_data():
    """初始化数据文件"""
    if not os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, 'w') as f:
            json.dump([], f)
API路由
联系人管理API

GET /api/contacts - 获取所有联系人

POST /api/contacts - 添加新联系人

PUT /api/contacts/<int:contact_id> - 更新联系人

DELETE /api/contacts/<int:contact_id> - 删除联系人

PUT /api/contacts/<int:contact_id>/favorite - 切换收藏状态

数据操作API

GET /api/export - 导出联系人到Excel

POST /api/import - 从Excel导入联系人

requirements.txt
Python依赖包列表：

text
Flask==2.3.3
Flask-CORS==4.0.0
pandas==2.0.3
openpyxl==3.1.2
安装与运行
前置要求
Python 3.8 或更高版本

pip 包管理器

安装步骤
克隆项目到本地

进入后端目录：

bash
cd backend
创建虚拟环境（推荐）：

bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
安装依赖包：

bash
pip install -r requirements.txt
运行服务
bash
# 开发模式（默认端口5000）
python app.py

# 生产模式（指定端口）
python app.py --port 5000

# 调试模式
python app.py --debug
测试API
服务启动后，可以通过以下方式测试API：

查看所有联系人：

text
GET http://localhost:5000/api/contacts
添加新联系人：

text
POST http://localhost:5000/api/contacts
Content-Type: application/json

{
  "name": "张三",
  "company": "示例公司",
  "position": "工程师",
  "is_favorite": true,
  "contact_methods": [
    {"type": "phone", "value": "13800138000"},
    {"type": "email", "value": "zhangsan@example.com"}
  ]
}
API接口详细说明
1. 获取所有联系人
端点：GET /api/contacts

响应示例：

json
[
  {
    "id": 1,
    "name": "张三",
    "company": "示例公司",
    "position": "工程师",
    "notes": "重要客户",
    "is_favorite": true,
    "contact_methods": [
      {"type": "phone", "value": "13800138000"},
      {"type": "email", "value": "zhangsan@example.com"}
    ],
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-16T14:20:00"
  }
]
2. 添加联系人
端点：POST /api/contacts

请求体：

json
{
  "name": "李四",
  "company": "测试公司",
  "position": "经理",
  "notes": "",
  "is_favorite": false,
  "contact_methods": [
    {"type": "phone", "value": "13900139000"}
  ]
}
响应：

成功：HTTP 201，返回创建的联系人数据

失败：HTTP 400，错误信息

3. 更新联系人
端点：PUT /api/contacts/<contact_id>

参数：

contact_id：联系人ID（路径参数）

请求体：同添加联系人

响应：

成功：HTTP 200，返回更新后的联系人数据

失败：HTTP 404，联系人不存在

4. 删除联系人
端点：DELETE /api/contacts/<contact_id>

响应：

成功：HTTP 200，{"message": "Contact deleted"}

失败：HTTP 404，联系人不存在

5. 切换收藏状态
端点：PUT /api/contacts/<contact_id>/favorite

响应：

成功：HTTP 200，返回更新后的联系人数据

失败：HTTP 404，联系人不存在

6. 导出联系人
端点：GET /api/export

响应：

成功：返回Excel文件下载

失败：HTTP 500，服务器错误

7. 导入联系人
端点：POST /api/import

请求格式：multipart/form-data

参数：

file：Excel文件（.xlsx或.xls格式）

响应：

成功：HTTP 200，{"message": "Successfully imported X contacts"}

失败：HTTP 400，文件格式错误或处理失败

数据模型
联系人数据结构
json
{
  "id": 1,                     // 唯一标识符，自动生成
  "name": "张三",              // 姓名，必填
  "company": "示例公司",       // 公司，可选
  "position": "工程师",        // 职位，可选
  "notes": "重要客户",         // 备注，可选
  "is_favorite": true,        // 是否收藏，布尔值
  "contact_methods": [        // 联系方式数组
    {
      "type": "phone",        // 类型：phone/email/wechat/address
      "value": "13800138000"  // 联系方式值
    }
  ],
  "created_at": "2024-01-15T10:30:00",  // 创建时间，自动生成
  "updated_at": "2024-01-16T14:20:00"   // 更新时间，自动更新
}
配置选项
修改端口
python
if __name__ == '__main__':
    app.run(debug=True, port=5000)  # 修改端口号
修改数据文件路径
python
# 修改第10行
CONTACTS_FILE = 'path/to/your/contacts.json'
启用生产模式
python
# 修改运行配置
app.run(debug=False, host='0.0.0.0', port=5000)
数据导入导出格式
Excel文件格式
导出的Excel文件包含以下列：

id: 联系人ID

name: 姓名

company: 公司

position: 职位

notes: 备注

is_favorite: 是否收藏

type: 联系方式类型

value: 联系方式值

created_at: 创建时间

updated_at: 更新时间

导入注意事项
文件必须包含表头行

姓名（name）字段为必填

重复导入会自动生成新的ID

无效行会被自动跳过

部署指南
1. 生产环境部署
使用Gunicorn（推荐）
bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
使用Waitress（Windows）
bash
pip install waitress
waitress-serve --port=5000 app:app
2. 容器化部署（Docker）
Dockerfile
dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
构建和运行
bash
docker build -t address-book-backend .
docker run -p 5000:5000 -v ./data:/app/data address-book-backend
3. 云平台部署
阿里云/华为云
创建云服务器（ECS）

安装Python和依赖

配置安全组开放5000端口

使用PM2或Supervisor管理进程

PM2配置
bash
npm install -g pm2
pm2 start app.py --interpreter python --name "address-book"
pm2 save
pm2 startup
安全性考虑
1. 输入验证
所有API端点都验证输入数据

防止SQL注入（虽然使用JSON存储）

文件上传大小限制

2. 生产环境建议
禁用调试模式：debug=False

使用环境变量存储敏感信息

配置HTTPS证书

添加API认证机制

设置请求频率限制

监控和日志
添加日志记录
python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
健康检查端点
python
@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})
故障排除
常见问题
端口被占用

bash
# 查找占用端口的进程
netstat -ano | findstr :5000
# 或
lsof -i :5000

# 杀死进程或更换端口
导入文件失败

检查文件格式是否为.xlsx或.xls

确认文件未损坏

检查是否有读写权限

数据文件损坏

备份contacts.json文件

删除损坏的文件

重启服务自动创建新文件

跨域请求被阻止

检查Flask-CORS配置

确认前端地址在允许列表中

检查浏览器控制台错误

调试模式
启动调试模式查看详细错误：

bash
python app.py --debug
性能优化
1. 数据缓存
python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_contacts_cached():
    with open(CONTACTS_FILE, 'r') as f:
        return json.load(f)
2. 分页支持
python
@app.route('/api/contacts')
def get_contacts_paginated():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # 实现分页逻辑
    start = (page - 1) * per_page
    end = start + per_page
    
    return jsonify(contacts[start:end])
3. 异步处理
对于大数据量导入导出，可以考虑使用Celery进行异步处理。

扩展功能
1. 添加数据库支持
python
# 使用SQLite或PostgreSQL替代JSON文件
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # ... 其他字段
2. 添加用户认证
python
from flask_jwt_extended import JWTManager, jwt_required

app.config['JWT_SECRET_KEY'] = 'your-secret-key'
jwt = JWTManager(app)

@app.route('/api/contacts')
@jwt_required()
def get_contacts():
    # 需要认证才能访问
3. 添加API文档
python
from flasgger import Swagger

swagger = Swagger(app)

@app.route('/api/contacts')
def get_contacts():
    """
    获取所有联系人
    ---
    responses:
      200:
        description: 联系人列表
    """
测试
单元测试
python
import unittest
from app import app

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    
    def test_get_contacts(self):
        response = self.app.get('/api/contacts')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
API测试脚本
bash
# 使用curl测试
curl http://localhost:5000/api/contacts
curl -X POST http://localhost:5000/api/contacts -H "Content-Type: application/json" -d '{"name":"测试"}'
贡献指南
Fork本仓库

创建功能分支：git checkout -b feature/new-feature

提交更改：git commit -m 'Add new feature'

推送到分支：git push origin feature/new-feature

提交Pull Request
