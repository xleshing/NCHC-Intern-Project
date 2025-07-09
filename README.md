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
 
---
## 使用方法
```
ansible-playbook -i inventory.ini k8s.yml
```
> control-plan, masters 與 workers 的主機清單, SSH 連線資訊, cluster cidr, cluster endpoint, cilium version 等變數在 inventory.ini 裡設定

> 由於無法繞過首次登陸強制變更密碼機制，須先設定完密碼才能使用該腳本

