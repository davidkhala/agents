# NVIDIA OpenShell
[source](https://github.com/NVIDIA/OpenShell)


## Install
```
curl -LsSf https://raw.githubusercontent.com/NVIDIA/OpenShell/main/install.sh | sh
```


Install the public OpenShell skills for your coding agent: `npx skills add NVIDIA/OpenShell`
- Support IBM Bob

## GetStarted

Setup
```
openshell sandbox create --name demo
```
- It create 2 containers of image `nvcr.io/nvidia/base/ubuntu` and `ghcr.io/nvidia/openshell/supervisor`
- Then terminal will go into of container of `nvcr.io/nvidia/base/ubuntu`, open a shell session with `ubuntu@sandbox-demo`
- delete it by `openshell sandbox delete demo`