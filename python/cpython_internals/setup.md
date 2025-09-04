# setup for neovim 

## 配置pyright

我会 等下上传一下配置。

```json

{
	"include": [
		"Lib/**/*",
		"Include/**/*",
		"Modules/**/*",
		"Python/**/*",
		"Tools/**/*.py"
	],
	"exclude": [
		"build/**/*",
		"Doc/**/*",
		"Misc/**/*",
		"PC/**/*",
		"Scripts/**/*",
		"test/**/*",
		"venv/**/*",
		"*.egg-info/**/*"
	],
	"pythonPlatform": "linux",
	"typeCheckingMode": "basic",
	"extraPaths": [
		"Lib",
		"Include",
		"Modules",
		"Python"
	],
	"analysis": {
		"autoSearchPaths": true,
		"useLibraryCodeForTypes": true,
		"diagnosticMode": "workspace",
		"includePackageData": true,
		"strictParameterNoneValue": false,
		"allowUnusedVariables": false,
		"allowUnreachableCode": false
	},
	"ignore": [
		{
			"code": "reportMissingImports",
			"path": "Lib/**/*"
		},
		{
			"code": "reportUndefinedVariable",
			"path": "Modules/**/*"
		}
	]
}
```

## 配置C

clangd + bear
先使用bear 生成一个配置文件

not work，经过我的测试，实际上这样还是步行。
最后无奈 😮‍💨 专项vscode + vim 


