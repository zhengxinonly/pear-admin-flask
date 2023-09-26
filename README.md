

## 贡献指南

如果想参与项目的贡献，提交代码之前需要启用 pre-commit、commitizen 对代码进行校验，运行以下指令即可。

初始化 pre-commit

```shell
pre-commit install
```

检查代码是否符合规范

```shell
git add .
```

```shell
pre-commit run --all-files
```

初始化 commitizen

```shell
pre-commit install -t commit-msg
```

使用 `cz commit` 代替 `git commit` 进行提交