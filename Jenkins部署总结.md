# Jenkins 部署总结

### Jenkins 是什么

- Jenkins 是开源的持续集成 / 持续交付（CI/CD）自动化工具，用来自动化执行测试、构建、部署等任务
- 一句话：让测试流程自动跑，到时间点 Jenkins 自动跑框架，不用人工手动点

### CI 和 CD

- CI（持续集成）：开发把代码提交到仓库（gitee/github/gitlab），Jenkins 自动拉取代码跑，发现问题
- CD（持续交付）：测试完成后自动执行部署、打包、发布，从代码到上线全流程

### 为什么把接口自动化部署到 Jenkins

- 定时执行（早上 / 晚上）
- 运行完结果通知团队（邮件 / 企业微信 / 钉钉）
- 生成测试报告

### 部署需要的东西

- 框架（python + requests + pytest + allure + yaml/excel）
- 仓库（gogs / github / gitee / svn）
- jdk 环境
- jenkins（本地或服务器）
- python 环境

### 部署步骤（面试直接背）

1. 把接口自动化框架代码上传到 xx 仓库
2. jenkins 配置关联 xx 仓库
3. jenkins 配置运行自动化脚本
4. 自动执行用例，生成 allure 报告
5. 配置企业微信 / 邮箱，把结果发送给相关人员

### 上传代码的核心命令

```bash
touch README.md
git init                                # 初始化
git add README.md                       # 添加到暂存区
git commit -m "first commit"            # 提交
git remote add origin http://xxx.git    # 关联仓库地址
git push -u origin master               # 推送到远程仓库
```

### 定时执行表达式

| 表达式 | 含义 |
|--------|------|
| `*/2 * * * *` | 每 2 分钟执行 |
| `H 8 * * *` | 每天早上 8 点执行 |
| `H/5 * * * *` | 每 5 分钟执行 |
| `H 9 * * 1-5` | 周一到周五 9 点执行 |

### 框架执行命令

```bash
python3 -m venv myvenv                    # 创建虚拟环境
source myvenv/bin/activate                # 虚拟环境生效
pip install -r requirement.txt -i 镜像    # 安装依赖
python main.py                            # 执行框架
```

### 注意

- 框架代码一定要先在本地跑通，再放到 Jenkins，这样 Jenkins 上报错基本不是代码问题
- allure-results 一定要和本地项目生成的 allure 一致
