from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import json
import pandas as pd
import os
from datetime import datetime


app = Flask(__name__)
CORS(app)  # 允许跨域请求

CONTACTS_FILE = 'contacts.json'

# 初始化数据文件
def init_data():
    if not os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, 'w') as f:
            json.dump([], f)

# 获取所有联系人
@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    init_data()
    with open(CONTACTS_FILE, 'r') as f:
        contacts = json.load(f)
    return jsonify(contacts)

# 添加联系人
@app.route('/api/contacts', methods=['POST'])
def add_contact():
    init_data()
    contact = request.json

    with open(CONTACTS_FILE, 'r') as f:
        contacts = json.load(f)

    # 生成ID
    contact['id'] = len(contacts) + 1
    contact['created_at'] = datetime.now().isoformat()
    contact['is_favorite'] = contact.get('is_favorite', False)

    contacts.append(contact)

    with open(CONTACTS_FILE, 'w') as f:
        json.dump(contacts, f, indent=2)

    return jsonify(contact), 201

# 更新联系人
@app.route('/api/contacts/<int:contact_id>', methods=['PUT'])
def update_contact(contact_id):
    init_data()
    updated_data = request.json

    with open(CONTACTS_FILE, 'r') as f:
        contacts = json.load(f)

    for contact in contacts:
        if contact['id'] == contact_id:
            contact.update(updated_data)
            contact['updated_at'] = datetime.now().isoformat()

            with open(CONTACTS_FILE, 'w') as f:
                json.dump(contacts, f, indent=2)

            return jsonify(contact)

    return jsonify({'error': 'Contact not found'}), 404

# 删除联系人
@app.route('/api/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    init_data()

    with open(CONTACTS_FILE, 'r') as f:
        contacts = json.load(f)

    new_contacts = [c for c in contacts if c['id'] != contact_id]

    with open(CONTACTS_FILE, 'w') as f:
        json.dump(new_contacts, f, indent=2)

    return jsonify({'message': 'Contact deleted'})

# 切换收藏状态
@app.route('/api/contacts/<int:contact_id>/favorite', methods=['PUT'])
def toggle_favorite(contact_id):
    init_data()

    with open(CONTACTS_FILE, 'r') as f:
        contacts = json.load(f)

    for contact in contacts:
        if contact['id'] == contact_id:
            contact['is_favorite'] = not contact.get('is_favorite', False)

            with open(CONTACTS_FILE, 'w') as f:
                json.dump(contacts, f, indent=2)

            return jsonify(contact)

    return jsonify({'error': 'Contact not found'}), 404

# 导出为Excel
@app.route('/api/export', methods=['GET'])
def export_contacts():
    init_data()

    with open(CONTACTS_FILE, 'r') as f:
        contacts = json.load(f)

    # 转换为DataFrame
    df = pd.DataFrame(contacts)

    # 处理联系方式数组
    if 'contact_methods' in df.columns:
        # 展开联系方式
        expanded_methods = []
        for contact in contacts:
            base_info = {k: v for k, v in contact.items() if k != 'contact_methods'}
            if 'contact_methods' in contact:
                for method in contact['contact_methods']:
                    row = base_info.copy()
                    row.update(method)
                    expanded_methods.append(row)
        df = pd.DataFrame(expanded_methods)

    # 保存为Excel
    excel_file = 'contacts_export.xlsx'
    df.to_excel(excel_file, index=False)

    return send_file(excel_file, as_attachment=True)

# 导入Excel
@app.route('/api/import', methods=['POST'])
def import_contacts():
    init_data()

    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    try:
        # 读取Excel文件
        df = pd.read_excel(file)

        # 转换为联系人格式
        contacts = []
        for _, row in df.iterrows():
            contact = row.to_dict()
            contact['id'] = len(contacts) + 1
            contact['is_favorite'] = False
            contact['created_at'] = datetime.now().isoformat()
            contacts.append(contact)

        # 保存到文件
        with open(CONTACTS_FILE, 'w') as f:
            json.dump(contacts, f, indent=2)

        return jsonify({'message': f'Successfully imported {len(contacts)} contacts'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':

    app.run(debug=True, port=5000)
