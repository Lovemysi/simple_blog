## Simple Blog

基于 Django 开发的简易博客

---

### 开发

安装依赖

```bash
pip install -r requirements.txt
```

迁移数据库

```bash
python ./manage.py makemigrations users posts
python ./manage.py migrate
```

运行服务器

```bash
python ./manage.py runserver
```

---

## 前端模板

文件夹 `front_end` 为构建前端模板的地方, 详情请 [查看](./front_end/README.md)

---

## 测试

单元测试

```bash
python ./manage.py test ./apps/
```

覆盖测试

```bash
coverage run ./manage.py test ./apps/

# 覆盖测试报告
coverage report
```

---

## TODO

- [ ] 添加文章标签
