# `core2050.soohwalee.com` 배포 가이드 (Cloudflare + 오라클 Docker + Nginx Proxy Manager)

보내주신 **Nginx Proxy Manager (NPM)** 환경(`aihorse_web:80`, `ford_web:80`, `172.17.0.1:8081`)에 100% 맞춰 설정을 최적화했습니다.
기존에 `127.0.0.1`에만 바인딩하면 NPM 컨테이너 내부에서 접근이 막히기 때문에, **`core2050_web:80` 컨테이너명 직접 라우팅**과 **`172.17.0.1:8092` 브리지 라우팅** 두 가지가 모두 작동하도록 구성했고 배포 스크립트가 NPM의 도커 네트워크에 `core2050_web`을 자동으로 물려줍니다.

---

## 1단계: Cloudflare DNS 레코드 추가
1. Cloudflare 대시보드 → `soohwalee.com` → **DNS > Records** 이동
2. **Add record** 클릭:
   - **Type**: `A` (또는 기존 `aihorse`·`trc`와 동일하게 `A` / `CNAME`)
   - **Name**: `core2050`
   - **IPv4 address**: 현재 오라클 클라우드 서버 공인 IP (`aihorse.soohwalee.com`과 동일한 IP)
   - **Proxy status**: **DNS only (회색 구름)** 권장 *(※ NPM에서 Let's Encrypt 인증서를 최초 발급받을 때 회색 구름으로 두면 HTTP-01 인증 오류가 전혀 나지 않으며, 발급 완료 후 필요 시 주황 구름 `Full (strict)`로 켜셔도 됩니다.)*

---

## 2단계: 오라클 서버 SSH에서 원클릭 도커 빌드·네트워크 연결
`core2050-oracle-docker-deploy.zip` 파일을 오라클 서버 `/home/ubuntu/`에 올린 뒤 터미널에서 아래 명령어 한 줄만 실행하세요:

```bash
rm -rf /tmp/core2050-pkg && python3 -m zipfile -e ~/core2050-oracle-docker-deploy.zip /tmp/core2050-pkg && sudo python3 /tmp/core2050-pkg/core2050-oracle-docker/tools/deploy_oracle_core2050.py && rm -f ~/core2050-oracle-docker-deploy.zip
```

스크립트가 자동으로:
1. `/home/ubuntu/core2050` 폴더에 소스를 배치하고 `core2050_web` · `core2050_api` 컨테이너를 빌드·실행합니다.
2. 현재 실행 중인 Nginx Proxy Manager(및 `aihorse_web` 등)의 공유 도커 네트워크를 찾아 `core2050_web`을 자동 연결합니다.

---

## 3단계: Nginx Proxy Manager 웹 화면에서 `Add Proxy Host` 등록
우측 상단 초록색 **`Add Proxy Host`** 버튼을 누르고 기존 `aihorse.soohwalee.com`과 똑같이 입력합니다:

1. **Details 탭**
   - **Domain Names**: `core2050.soohwalee.com` (입력 후 Enter)
   - **Scheme**: `http`
   - **Forward Hostname / IP**: `core2050_web` *(만약 네트워크가 분리되어 있다면 `jsn`처럼 `172.17.0.1` 입력)*
   - **Forward Port**: `80` *(`172.17.0.1` 입력 시에는 `8092`)*
   - **Cache Assets** / **Block Common Exploits**: 체크 켜기
2. **SSL 탭**
   - **SSL Certificate**: `Request a new SSL Certificate` 선택
   - **Force SSL** 및 **HTTP/2 Support**: 체크 켜기
   - Let's Encrypt 약관 동의 체크 후 **Save** 클릭!

Status가 **`Online`** 초록불로 바뀌면 휴대폰 카메라로 토론문 2페이지 상단의 QR코드를 찍었을 때 즉시 `https://core2050.soohwalee.com` 웹 시뮬레이터가 열립니다.
