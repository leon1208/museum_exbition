## node和npm管理

推荐使用volta管理node和pnpm版本, 可以避免不同项目之间的node和npm版本冲突问题。但要注意PATH上要把volta的bin目录添加到环境变量中,并且优先于系统的node和npm。

### 安装volta

```bash
# 安装volta
curl https://get.volta.sh | bash
```

### 配置node

```bash
# 配置volta
volta install node@20.17.0
volta install pnpm
```



## 开发

```bash
# 进入项目目录
cd ruoyi-ui

# 安装依赖
pnpm install

# 启动服务
pnpm run dev
```

浏览器访问 http://localhost:1024

## 发布

```bash
# 构建测试环境
pnpm run build:stage

# 构建生产环境
pnpm run build:prod
```