
## powershell

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
iwr -useb https://openclaw.ai/install.ps1 | iex
```

## npm

<https://www.npmjs.com/package/openclaw>

```shell
npm install -g openclaw@latest
```

## ollama

```
ollama launch openclaw
```

- Pre-requisite: nodejs
