# plugin Dev
- package id defined in `name` in `manifest.yaml`


## dev run
with `.env` configured with

```dotenv
INSTALL_METHOD=remote
REMOTE_INSTALL_HOST=localhost# from your dify instance 
REMOTE_INSTALL_PORT=5003# from your dify instance
REMOTE_INSTALL_KEY= # from your dify instance
```
then run 
```
uv|python run main.py (--active)
```



## Troubleshoot
`PluginDaemonBadRequestError: plugin verification has been enabled, and the plugin you want to install has a bad signature`
- configure `FORCE_VERIFYING_SIGNATURE=false` in container of image `langgenius/dify-plugin-daemon` and then restart