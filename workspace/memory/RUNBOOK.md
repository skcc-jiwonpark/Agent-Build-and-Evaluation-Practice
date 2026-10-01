# Local Runbook

## 처음 한 번

1. 저장소 루트에서 의존성을 설치한다: `uv sync`
2. 저장소 루트의 `.env.example`을 보고 같은 위치의 `.env`에 키를 넣는다.

`.env`에는 최소 `OPENAI_API_KEY`가 필요하다. 외부 검색은 `TAVILY_API_KEY`,
LangSmith 추적은 `LANGSMITH_API_KEY`, `LANGSMITH_TRACING=true`,
`LANGSMITH_PROJECT`가 추가로 필요하다. 키 값은 어떤 문서·커밋에도 넣지 않는다.

## 표준 실행

```bash
uv run python workspace/run_agent.py
```

실행 순서:

1. `references/`의 PDF를 읽기 전용 텍스트로 `work/extracted/`에 준비한다.
2. `inputs/research_question.md`와 추출 텍스트를 문맥으로 구성한다.
3. LangChain 에이전트가 근거 보고서를 생성한다.
4. 하네스 검사에서 누락된 섹션이 있으면 한 번만 수리한다.
5. 검증 정보가 붙은 보고서를 `outputs/`에 저장한다.

## 외부 탐색 실행

```bash
uv run python workspace/run_agent.py --search
```

Tavily 결과는 후속 문헌을 찾기 위한 `lead`일 뿐이다. PDF 또는 SI를
`references/`에 추가해 직접 확인하기 전에는 후보 근거로 승격하지 않는다.

## 문제 해결

| 증상 | 확인할 것 |
| --- | --- |
| API 키 오류 | `.env`의 변수 이름, 터미널을 다시 연 뒤 실행했는지 |
| Tavily 오류 | `--search` 사용 여부와 `TAVILY_API_KEY` 설정 |
| 전구체 값이 없음 | 실험 섹션·SI가 있는 논문인지; 방법론/리뷰 논문만 있는지 |
| 출력 형식 누락 | `HARNESS.md`, `system_prompt.md`, `evals/validation_cases.md` 확인 |
| LangSmith에 기록 안 됨 | 추적 관련 세 환경변수와 네트워크 설정 확인 |

## 변경 후 검증

```bash
uv run python -m unittest discover -s workspace/tests -v
```

그 다음 작은 연구 질문과 제한된 PDF로 한 번 실행해, 각 후보에 출처 locator와
상태 표기가 남는지 확인한다.
