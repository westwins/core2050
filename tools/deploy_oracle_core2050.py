#!/usr/bin/env python3
"""One-click Oracle Cloud Docker + Nginx Proxy Manager (NPM) auto-network deployment for core2050.soohwalee.com."""
import json
import os
import shutil
import subprocess
import time
import urllib.request

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TARGET_DIR = "/home/ubuntu/core2050"
WEB_CONTAINER = "core2050_web"
HOST_PORT = 8092


def run(cmd, cwd=None, check=True, capture=False):
    print(f"[EXEC] {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=cwd, check=check, text=True, capture_output=capture)


def connect_to_npm_network():
    """Finds the running Nginx Proxy Manager container and attaches core2050_web to its Docker network(s)."""
    res = subprocess.run(
        ["docker", "ps", "--format", "{{.Names}}\t{{.Image}}"],
        capture_output=True,
        text=True,
    )
    if res.returncode != 0:
        return []

    npm_containers = []
    for line in res.stdout.strip().splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        cname, cimg = parts[0], parts[1] if len(parts) > 1 else ""
        if "nginx-proxy-manager" in cimg.lower() or "npm" in cname.lower() or "proxy" in cname.lower():
            npm_containers.append(cname)

    # Also inspect aihorse_web or ford_web if present to grab the exact shared proxy network!
    for ref_name in ["aihorse_web", "ford_web", "hormuz_frontend"]:
        chk = subprocess.run(["docker", "inspect", ref_name], capture_output=True, text=True)
        if chk.returncode == 0 and ref_name not in npm_containers:
            npm_containers.append(ref_name)
            break

    attached_nets = []
    for target in npm_containers:
        insp = subprocess.run(["docker", "inspect", target], capture_output=True, text=True)
        if insp.returncode != 0:
            continue
        try:
            data = json.loads(insp.stdout)
            nets = list(data[0].get("NetworkSettings", {}).get("Networks", {}).keys())
            for net in nets:
                if net in ("bridge", "host", "none", "core2050_net", "core2050_core2050_net"):
                    continue
                conn = subprocess.run(
                    ["docker", "network", "connect", net, WEB_CONTAINER],
                    capture_output=True,
                    text=True,
                )
                if conn.returncode == 0 or "already exists" in (conn.stderr or ""):
                    attached_nets.append(net)
        except Exception:
            pass
    return sorted(set(attached_nets))


def main():
    print("=== CORE 2050 Oracle Docker + Nginx Proxy Manager 배포 시작 ===")
    if os.path.abspath(SRC_DIR) != os.path.abspath(TARGET_DIR):
        os.makedirs(TARGET_DIR, exist_ok=True)
        for item in ["docker-compose.yml", "frontend", "backend", "tools", "README_DEPLOY_KR.md"]:
            s = os.path.join(SRC_DIR, item)
            d = os.path.join(TARGET_DIR, item)
            if os.path.isdir(s):
                if os.path.exists(d):
                    shutil.rmtree(d)
                shutil.copytree(s, d)
            elif os.path.isfile(s):
                shutil.copy2(s, d)

    run(["docker", "compose", "up", "-d", "--build"], cwd=TARGET_DIR)

    attached = connect_to_npm_network()
    if attached:
        print(f"[NPM NETWORK OK] '{WEB_CONTAINER}' 컨테이너를 Nginx Proxy Manager 공유 네트워크({', '.join(attached)})에 자동 연결했습니다!")
    else:
        print("[NPM NETWORK INFO] 공유 사용자 정의 네트워크 미감지 — NPM에서 172.17.0.1:8092 로도 바로 연결 가능합니다.")

    print("헬스체크 확인 중...")
    for _ in range(15):
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{HOST_PORT}/api/health", timeout=3) as resp:
                print("[HEALTH OK]", resp.read().decode("utf-8"))
                break
        except Exception:
            time.sleep(1)

    print("\n==================================================================")
    print("✅ 컨테이너 기동 완료! 이제 Nginx Proxy Manager(Add Proxy Host)에서:")
    if attached:
        print("  • Domain Names        : core2050.soohwalee.com")
        print("  • Scheme              : http")
        print(f"  • Forward Hostname/IP : {WEB_CONTAINER}   (또는 172.17.0.1)")
        print("  • Forward Port        : 80             (172.17.0.1 사용 시 8092)")
    else:
        print("  • Domain Names        : core2050.soohwalee.com")
        print("  • Scheme              : http")
        print("  • Forward Hostname/IP : 172.17.0.1")
        print(f"  • Forward Port        : {HOST_PORT}")
    print("  • SSL 탭              : Request a new SSL Certificate + Force SSL + HTTP/2 체크")
    print("==================================================================")


if __name__ == "__main__":
    main()
