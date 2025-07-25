#!/usr/bin/python3
from ansible.module_utils.basic import AnsibleModule
import os
import re


def main():
    module = AnsibleModule(
        argument_spec={},
        supports_check_mode=False
    )

    cmd = [
        'kubeadm','token','create',
        '--print-join-command'
    ]
    rc, out, err = module.run_command(cmd)
    if rc != 0:
        module.fail_json(msg='kubeadm token create failed', rc=rc, stderr=err)

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
    
    result = {
        'changed': True,
        'join_endpoint': m.group(1),
        'token': m.group(2),
        'discovery_token_hash': m.group(3),
    }
    if m.group(4):
        result['certificate_key'] = m.group(4)

    module.exit_json(**result)

if __name__ == '__main__':
    main()
