---
trigger: always_on
---
# 선교편지 자동 미리보기 규칙 (Auto Preview Rule)

선교편지의 내용을 새로 작성하거나 수정할 때는, **사용자가 따로 요청하지 않더라도 반드시 `generative_ui` 기능을 이용해 완성된 편지의 HTML 미리보기를 채팅창에 띄워주어야 합니다.**

1. 편지 내용을 반영한 `preview.html` 형태의 파일을 생성하세요.
2. `<agent-embed src="file:///[경로]/preview.html"></agent-embed>` 태그를 이용해 채팅창에 인라인으로 렌더링되게 하세요.
3. 이 규칙은 이 저장소에서 활동할 때 항상 적용됩니다.
