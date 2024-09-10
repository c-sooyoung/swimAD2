# Troubleshooting

swimAD2를 사용하면서 겪은 오류나 문제사항, 그리고 찾은 해결방안들입니다.

#### 맥에서 SDK 설치 오류 (2024.09.09 / 최욱진)

SDK 설치 할 때 `/Library/Frameworks/` 에 `dwf.framework` 폴더를 넣어야 하는데, 관리자 권한 없이 설치툴을 실행하면 제대로 복사되지 않는다. `/Library/Frameworks/` 폴더를 직접 열어서 드래그하면 관리자 비밀번호를 넣어서 복사 가능하다.
