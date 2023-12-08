## Simple Blog Front End

用于辅助开发一体式网站前端, 生成的 `style.css` 文件需放在 Django 的根目录下的 `static` 文件夹中

### 安装

```bash
npm install
```

---

### 开发

```bash
npm run dev
```

---

### 构建

```bash
npm run build
```

构建完成后, 可以使用以下命令快速移动 `style.css` 文件至 `static/` 目录

```bash
# powershell
Copy-Item ./dist/style.css ../static/
```

```bash
# cmd
copy ./dist/style.css ../static/
```

```bash
# bash
cp ./dist/style.css ../static/
```
