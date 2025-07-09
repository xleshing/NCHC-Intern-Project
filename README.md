## 檔案說明

- ansible.cfg 
: Ansible 全域設定檔，目前設定了python interpreter 位置與 remote_tmp 位置

- group_vars
: 放置以群組或主機為單位的變數檔，目前存放登入密碼（未加密）


- inventory.ini
: INI 格式的 Inventory，定義 control-plan, masters 與 node 的主機清單、SSH 連線資訊，以及 cluster cidr, cluster endpoint, cilium version 等變數。

- k8s.yml
: 主 Playbook

- library/*
: 自訂 module，負責 control-plan 初始化、 masters, workers 節點初始化與加入

- roles/* 
: 安裝 Cilium CNI, Kubernetes 依賴套件（Docker、kubeadm、kubectl、kubelet 等）與 NVIDIA GPU Operator 的 role

>  變數說明
> - controlplan ansible_host
> : 執行 kubectl 指令的host ip（已設定 .kube）
> 
> - master_i ansible_host
> : 其他 control-plan ip (未設定 .kube，執行 kubectl 命令時，會找不到api server) 
>  
> - node_i ansible_host
> : worker node ip
> 
> - nfsserver ansible_host
> : nfs server ip
> 
> - cluster_cidr_args
> : cluster cidr (xxx.xxx.xxx.xxx/xx)
> 
> - cluster_endpoint_args
> : cluster endpoint (xxx.xxx.xxx.xxx:xxxxx)
> 
> - nfs_server_args
> : nfs server ip (會自動取用nfs_server group 裡的第一個 ip)
> 
> - nfs_path_args
> : nfs 共享目錄

## 使用方法
```
ansible-playbook -i inventory.ini k8s.yml
```
> control-plan, masters 與 workers 的主機清單, SSH 連線資訊, cluster cidr, cluster endpoint, cilium version 等變數在 inventory.ini 裡設定

> 由於無法繞過首次登陸強制變更密碼機制，須先設定完密碼才能使用該腳本

