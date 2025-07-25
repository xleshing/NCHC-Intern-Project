## Ansible Playbook 參數說明
> 除 Ansible 設定檔與主機列表外，其餘參數由 group\_vars/all.yml 統一管理
 
### Ansible 設定檔
> 檔案位置：ansible.cfg

| 參數                   | 說明                                 | 預設值                |
|----------------------|------------------------------------|--------------------|
| `host_key_checking`  | 關閉嚴格 SSH 主機金鑰檢查，避免 Fingerprint 錯誤。 | `False`            |
| `interpreter_python` | 遠端主機 Python 直譯器路徑。                 | `/usr/bin/python3` |
| `remote_tmp`         | Ansible 在遠端使用的暫存目錄。                | `~/.ansible/tmp`   |

### 主機列表
> 檔案位置：inventory.ini

| 群組                 | 主機                | IP               |
|--------------------|-------------------|-------------------|
| `local` |localhost | localhost |


### 全域參數

| 參數                 | 說明                | 預設值               |
|--------------------|-------------------|-------------------|
| `ssh_user`<sup>[*\**](#ssh_user)</sup>         | 所有遠端主機 SSH 登入使用者。 | `ubuntu`          |
| `secret`           | `ssh_user` 的密碼。   |  |
| `twcc_project_id`  | TWCC 專案 ID。       |              |
| `twcc_solution_id` | TWCC 解決方案 ID。     |              |
| `twcc_api_key`     | TWCC API Key。     |             |
| `control_count`<sup>[*\**](#control_count)</sup>    | control plane VM 數量。    | 必須等於 `1`           |
| `master_count`     | master VM 數量。           | `2`           |
| `worker_count`<sup>[*\**](#flavorcounts)</sup>     | worker VM 數量。           | 由 `create_vm.flavor_counts` 決定           |
|`ceph_control_count`| ceph control_count VM 數量。 | 必須等於 `1`|
|`ceph_master_count`| ceph master VM 數量。 | `2`|
|`ceph_worker_count`| ceph worker VM 數量。 | `3`|
| `volume_count` | ceph sc 磁碟數量。 | `3` | 
| `vol_size` | 預設資料碟大小 (GiB)。 | `100`     |
| `cluster_cidr_args`| Kubernetes Pod 網路 CIDR。 | `10.0.0.0/16` |
| `endpoint_target_group_name`<sup>[*\**](#endpoint_group)</sup>| Kubernetes Cluster Endpoint 所在的群組名稱。 | `loadbalancer` |
|`ceph_cluster_cidr_args`|Ceph Cluster Kubernetes Pod 網路 CIDR。| `10.0.0.0/16`|
|`ceph_endpoint_target_group_name`<sup>[*\**](#endpoint_group)</sup>|Ceph Cluster Kubernetes Cluster Endpoint 所在的群組名稱。| `ceph_loadbalancer`|
|`cp_target_group_name`<sup>[*\**](#target_group_name)</sup>|control-plan 群組名稱。| `control_plan`
|`master_target_group_name`<sup>[*\**](#target_group_name)</sup>|master 群組名稱。| `masters`
|`worker_target_group_name`<sup>[*\**](#target_group_name)</sup>|worker 群組名稱。| `workers`
|`ceph_cp_target_group_name`<sup>[*\**](#target_group_name)</sup>| Ceph Control Plan 群組名稱。|`ceph_control_plan`
|`ceph_master_target_group_name`<sup>[*\**](#target_group_name)</sup>| Ceph Master 群組名稱。|`ceph_masters`
|`ceph_worker_target_group_name`<sup>[*\**](#target_group_name)</sup>| Ceph Worker 群組名稱。|`ceph_workers`
|`wait_etcd_timeout`|加入 Worker 後，等待 etcd 穩定的時間(秒)。| `20`
### add_node.yml參數


| 參數                 | 說明                | 預設值               |
|--------------------|-------------------|-------------------|
|`add_cp_ip`	|欲新增 Node 集群之控制平面 IP。	|
|`flavor_counts`<sup>[*\**](#flavorcounts)</sup>	|各類型 VM 規格的數量設定（dict）。	|	

### add_vol.yml參數
| 參數                 | 說明                | 預設值               |
|--------------------|-------------------|-------------------|
 | `ceph_add_cp_ip`|欲新增 Vol 集群之 Ceph 控制平面 IP。| 
 | `ceph_worker_flavor`|VM 規格。| `v.xsuper`
 | `max_vol_per_worker`|單節點 Vol 上限。| `2`
 | `volume_count`<sup>[*\**](#volume_count)</sup>|欲新增 Vol 數量。| `0`
 
### 各角色參數

---

#### create vm<sup>[*\**](#creatvm)</sup>

| 參數                     | 說明                               | 預設值                            |
|------------------------|----------------------------------|--------------------------------|
| `twcc_api_host`        | TWCC API 主機名稱。                   | `openstack-taichung-default-2` |
| `key_pair_name`        | 注入 VM 的 Key Pair 名稱。             | *目前還沒有自動創建 Key Pair*     |
| `cp_flavor`               | Control Plan VM 規格。                           | `v.xsuper`                     |
| `master_flavor`               | Master VM 規格。                           | `v.xsuper`                     |
| `ceph_cp_flavor`               | Ceph Cluster Control Plan VM 規格。                           | `v.xsuper`                     |
| `ceph_master_flavor`               | Ceph Cluster Master VM 規格。                           | `v.xsuper`                     |
| `ceph_worker_flavor`               | Ceph Cluster Worker VM 規格。                           | `v.xsuper`                     |
|`flavor_counts`<sup>[*\**](#flavorcounts)</sup>	|各類型 VM 規格的數量設定（dict）。	|
| `volume_size`          | 系統碟大小 (GiB)。                     | `100`                          |
| `volume_type`          | 系統碟類型。                           | `block_storage-hdd`            |
| `private_network`      | 私有網路名稱。                          | `default_network`              |
| `sg_name`              | 安全群組名稱。                          |  *目前還沒有自動創建安全群組* |
| `vm_name`<sup>[*\**](#vm_name)</sup>              | VM 基本名稱。                         |        動態計算               |
| `vm_desc`              | VM 描述。                           | \`\`                           |
| `api_timeout`          | TWCC API 呼叫超時 (秒)。               | `600`                           |
| `initial_waiting_time` | VM 建立後初始等待 (秒)。                  | `60`                           |
| `poll_interval`        | VM 狀態輪詢間隔 (秒)。                   | `20`                           |
| `poll_retries`         | VM 狀態輪詢重試次數。                     | `30`                           |
| `vm_ssh_port`          | VM SSH 連接埠。                      | `22`                           |
| `ssh_interval`         | SSH 可用性檢查間隔 (秒)。                 | `20`                           |
| `ssh_timeout`          | SSH 等待超時 (秒)。                    | `600`                          |
| `ubuntu_version`       | Ubuntu 映像篩選名稱。                   | `Ubuntu-22.04`                 |
| `init_command`<sup>[*\**](#init_command)</sup>         | VM 初始化命令 (cloud-init/User Data)。 | 

#### create vol<sup>[*\**](#creatvol)</sup>

| 參數                     | 說明                        | 預設值                            |
|------------------------|---------------------------|--------------------------------|
| `twcc_api_host`        | TWCC API 主機名稱。            | `openstack-taichung-default-2` |
| `vol_name`<sup>[*\**](#vol_name)</sup>              | Volume 名稱，從 worker VMs 名取得前綴。          | 動態計算
| `server_idx`<sup>[*\**](#server_idx)</sup>           | 要掛載 volume 的 VM 索引 (0 起)。 | `0`                            |
| `api_timeout`          | TWCC API 呼叫超時 (秒)。               | `600`                           |
| `initial_waiting_time` | 建立後初始等待 (秒)。              | `60`                           |
| `poll_interval`        | 狀態輪詢間隔 (秒)。               | `20`                           |
| `poll_retries`         | 狀態輪詢重試次數。                 | `30`                           |
| `vol_type`         | 預設資料碟類型。        | `hdd`         |
#### create lb

| 參數                     | 說明                                                  | 預設值                            |
|------------------------|-----------------------------------------------------|--------------------------------|
| `twcc_api_host`        | TWCC API 主機名稱。                                      | `openstack-taichung-default-2` |
| `lb_name`              | LoadBalancer 名稱，從 control\_plane VM 名取得前綴 ( <timestamp><"lb"> ) 。          | 動態計算                           |
| `lb_desc`              | LoadBalancer 描述。                                    | \`\`                           |
| `pool_protocol`        | Pool 通訊協定 (HTTP/TCP/HTTPS)。                         | `TCP`                          |
| `pool_port`            | Pool 和 Listener 使用埠。                                | `6443`                         |
| `members_port`         | Pool 成員使用埠。                                         | `6443`                         |
| `method`               | 負載演算法 (ROUND\_ROBIN/LEAST\_CONNECTIONS/SOURCE\_IP)。 | `ROUND_ROBIN`                  |
| `private_ip_name`      | 私有網路名稱，對應 TWCC 回傳的 network name。                    | `default_network`              |
| `enable_pub_ip`        | 是否分配公網浮動 IP (boolean)。   | `false`   |
| `api_timeout`          | TWCC API 呼叫超時 (秒)。     | `600`             |
| `initial_waiting_time` | 建立後初始等待 (秒)。                                        | `60`                           |
| `poll_interval`        | 狀態輪詢間隔 (秒)。                                         | `20`                           |
| `poll_retries`         | 狀態輪詢重試次數。                                           | `30`                           |


#### install cilium

| 參數               | 說明                    | 預設值      |
|------------------|-----------------------|----------|
| `cilium_version` | Cilium Helm Chart 版本。 | `1.17.5` |

#### install ntp

| 參數              | 說明                 | 預設值                        |
|-----------------|--------------------|----------------------------|
| `ntp_driftfile` | NTP drift file 路徑。 | `/var/lib/ntp/ntp.drift`   |
| `ntp_servers`   | NTP 伺服器清單。         | Alibaba / Cloudflare 等 ips |


#### install Nvidia-GPU-Operator

| 參數                       | 說明                      | 預設值                                                                     |
|--------------------------|-------------------------|-------------------------------------------------------------------------|
| `helm_get_url`           | Helm 安裝 script URL。     | `https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3` |
| `helm_script`            | 本地 Helm 安裝腳本檔名。         | `get_helm.sh`                                                           |
| `nvidia_repo_name`       | NVIDIA Helm Repo 名稱。    | `nvidia`                                                                |
| `nvidia_repo_url`        | NVIDIA Helm Repo URL。   | `https://helm.ngc.nvidia.com/nvidia`                                    |
| `gpu_operator_namespace` | GPU Operator namespace。 | `gpu-operator`                                                          |
| `gpu_operator_chart`     | GPU Operator Chart 名稱。  | `nvidia/gpu-operator`                                                   |
| `gpu_operator_version`   | GPU Operator Chart 版本。  | `v25.3.1`                                                               |
#### install Rook-Ceph

| 參數                  | 說明                     | 預設值                                |
|---------------------|------------------------|------------------------------------|
| `rook_repo_url`     | Rook GitHub Repo URL。  | `https://github.com/rook/rook.git` |
| `rook_repo_version` | Rook Git Tag 或 Branch。 | `v1.17.6`                          |
| `rook_repo_dest`    | Rook 本地 clone 位置。      | `/home/{{ kube_user }}/rook`       |
|`wait_etcd_timeout`|創建ceph資源後，等待 etcd 穩定的時間(秒)。| `20`
| `wait_health_retries`|ceph cluster 健康狀態輪詢重試次數。| `30`
|  `wait_health_delay`|ceph cluster 健康狀態輪詢間隔(秒)。| `20`
| `wait_retries`| cephfs-filesystem 與 rbd-data-pool 狀態輪詢重試次數。| `30`
|`wait_delay`|cephfs-filesystem 與 rbd-data-pool 健康狀態輪詢間隔(秒)。| `20`
|`wait_prometheus_retries`|Prometheus Endpoint 狀態輪詢間隔(秒)。| `30`
|`wait_prometheus_delay`|Prometheus Endpoint 健康狀態輪詢重試次數。| `20`

#### Get Vol

| 參數                  | 說明                     | 預設值                                |
|---------------------|------------------------|------------------------------------|
|twcc_api_host|TWCC API 主機名稱。| "openstack-taichung-default-2"
|  server_idx<sup>[*\**](#server_idx)</sup> |要掛載 volume 的 VM 索引 (0 起)。| 0
    
---

<a id="control_count"></a>
> 1. 這裡由 `control_count` 所創建的 `control-plan` 指的是能夠使用 kubectl command 的主機並且初始 `kubeadm init` 指令也是在此主機上執行，其餘與 masters group 內的主機一樣。
<a id="endpoint_group"></a>
> 2. 此參數會創建一個群組拿來存 `control-plane-endpoint/ceph_control-plane-endpoint` 並把該群組的第一個 `IP:Port` 傳給 `kubeadm init --control-plane-endpoint` 來使用。
<a id="target_group_name"></a>
> 3. 此參數如需更動，也需手動更改 `k8s.yml` 內的 `hosts` 參數。
<a id="creatvm"></a>
> 4. 所有創建的 VM 會共用此設定檔內的參數。
<a id="ssh_user"></a>
> 5. 除創建相關腳本外 ( 部署 cilium 或部署 ceph 之類的 ) 的腳本，ssh登錄名之參數為 `kube_user` ，其由 k8s.yml 內的 `ansible_user` 傳遞並繼承全域參數 `ssh_user` 。 
<a id="vm_name"></a>
> 6. `vm_name` 會是以 `<timestamp>_<control/master/worker>-<idx>` 的形式表示。
<a id="init_command"></a>
> 7. 預設指令為 `sed -i '1iaccount sufficient pam_permit.so' /etc/pam.d/common-account  && echo "{{ ssh_user }}:{{ new_password }}" | chpasswd && printf "{{ ssh_user }} ALL=(ALL) NOPASSWD:ALL\nroot ALL=(ALL) NOPASSWD:ALL\n" >/etc/sudoers.d/{{ ssh_user }} && chmod 440 /etc/sudoers.d/{{ ssh_user }}` 此指令會在 `/etc/pam.d/common-account` 的第一行加上 `account sufficient pam_permit.so` ***這會讓 `pam_permit.so` 總是返回允許從而讓該文件內所有帳戶都不會因帳戶到期而被 PAM 拒絕***。
<a id="creatvol"></a>
> 8. 所有創建的 Vol 會共用此設定檔內的參數且每個 worker 都會有一個自己的 Vol。
<a id="vol_name"></a>
> 9. `vol_name` 會從 worker VM 名取得前綴 ( <timestamp><"vol"> )，但因需要迭代 worker idx 所以放在 `k8s.yml` 中設定。 
<a id="server_idx"></a>
> 10. 目前看每個 VM 只有一個，但其回傳的 `Response.Servers` 結構為 `list` ，以防萬一用 `idx` 來指定。
<a id="flavorcounts"></a>
> 11. `Worker` 數量會是 `flavor_counts` 總數。
<a id="volume_count"></a>
> 12. 如果超過 `max_vol_per_worker` 所限制的數量，腳本會自動新增新節點。

## 使用方法

### 創建集群
```
ansible-playbook -i inventory.ini k8s.yml --private-key <your_key_pair_name>
```
    
### 加入新節點
```
ansible-playbook -i inventory.ini add_node.yml --private-key <your_key_pair_name>
```

### 加入新儲存區
```
ansible-playbook -i inventory.ini add_vol.yml --private-key <your_key_pair_name>

