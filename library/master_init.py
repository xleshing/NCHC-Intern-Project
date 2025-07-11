#!/usr/bin/python3
from ansible.module_utils.basic import AnsibleModule
import os
import re

def run(module, cmd_list):
    rc, out, err = module.run_command(cmd_list)
    if rc != 0:
        module.fail_json(msg=f"Command failed: {' '.join(cmd_list)}", rc=rc, stderr=err)
    return out


def main():
    module = AnsibleModule(
        argument_spec={
            'cluster_cidr':          {'type': 'str', 'required': True},
            'cluster_endpoint':  {'type': 'str', 'required': True},
            'kube_user':         {'type': 'str', 'required': True}, 
        },
        supports_check_mode=False
    )

    cluster_cidr = module.params['cluster_cidr']
    cluster_endpoint = module.params['cluster_endpoint']

    # 1. Disable swap
    run(module, ['sudo', 'swapoff', '-a'])
    run(module, ['sudo', 'sed', '-i.bak', '-E', r's@^([^#].*\s+swap\s+)@#\1@', '/etc/fstab'])

    # 2. Enable IPv4 forwarding
    sysctl_conf = '/etc/sysctl.d/k8s.conf'
    run(module, ['bash', '-c', f"echo 'net.ipv4.ip_forward = 1' > {sysctl_conf}"])
    run(module, ['sudo', 'sysctl', '--system'])

    # config containerd
    run(module, ['mkdir', '-p', '/etc/containerd'])
    run(module, ['bash', '-c', 'containerd config default | tee /etc/containerd/config.toml'])
    run(module, [ 
      'sed', '-i.bak',
      r's/SystemdCgroup\s*=\s*false/SystemdCgroup = true/',
      '/etc/containerd/config.toml'
    ])
    run(module, ['sudo', 'systemctl','restart','containerd'])

    # 5. kubeadm init
    init_cmd = [
        'sudo', 'kubeadm','init',
        f'--control-plane-endpoint={cluster_endpoint}',
        f'--pod-network-cidr={cluster_cidr}',
        '--cri-socket=unix:///run/containerd/containerd.sock',
        '--upload-certs'
    ]
    rc, out, err = module.run_command(init_cmd)
    if rc != 0:
        module.fail_json(msg='kubeadm init failed', rc=rc, stderr=err)

    # save output file
    with open('kubeadm-init.out','w') as f:
        f.write(out)

    # 6. Setup kubeconfig
    kube_user = module.params['kube_user']
    home_dir  = f"/home/{kube_user}"
    kubeconfig = os.path.join(home_dir, '.kube', 'config')
    kube_dir   = os.path.dirname(kubeconfig)

    run(module, ['/bin/mkdir', '-p', kube_dir])
    run(module, ['sudo', '/bin/cp', '/etc/kubernetes/admin.conf', kubeconfig])
    run(module, ['sudo', '/bin/chown', f'{kube_user}:{kube_user}', kubeconfig]) 
    
    # extract join info
    lines = out.splitlines()
    join_lines = []
    capture = False

    for l in lines:
        stripped = l.rstrip()
        if not capture and stripped.lstrip().startswith("kubeadm join"):
            capture = True
        if capture:
            join_lines.append(stripped.replace("\\", "").strip())
            if not stripped.endswith("\\"):
                break

    full = " ".join(join_lines)

    pattern = (
        r"kubeadm join\s+(\S+)"                             # endpoint
        r".*?--token\s+(\S+)"                               # token
        r".*?--discovery-token-ca-cert-hash\s+(\S+)"        # hash
        r"(?:.*?--certificate-key\s+(\S+))?"                # optional cert-key
    )
    m = re.search(pattern, full)
    if not m:
        module.fail_json(msg="join command error", stdout=out)

    join_endpoint   = m.group(1)
    token           = m.group(2)
    discovery_hash  = m.group(3)
    certificate_key = m.group(4)  # 若未指定则为 None

    result = {
        "changed": True,
        "join_endpoint": join_endpoint,
        "token": token,
        "discovery_token_hash": discovery_hash,
    }
    if certificate_key:
        result["certificate_key"] = certificate_key

    module.exit_json(**result)

if __name__ == '__main__':
    main()
