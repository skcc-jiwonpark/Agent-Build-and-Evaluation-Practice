# Crystal-to-Precursor Evidence Agent

문헌과 Supporting Information에서 무기결정 합성의 전구체 후보·반응 조건·근거를
출처와 함께 비교하는 로컬 LangChain 에이전트다. 합성 레시피를 지어내거나 실험을
승인하지 않으며, 누락·충돌 정보를 연구자가 검토할 수 있게 남긴다.

## 빠른 시작

1. 저장소 루트의 `.env.example`을 참고하여 저장소 루트의 `.env`에 API 키를 설정한다.
2. `inputs/research_question.md`에 목표 물질과 비교 기준을 적는다.
3. 논문 PDF와 SI를 `references/`에 넣는다.
4. 아래 명령으로 로컬에서 실행한다.

```bash
uv run python workspace/run_agent.py
```

추가 문헌 탐색이 필요할 때만 Tavily를 켠다.

```bash
uv run python workspace/run_agent.py --search
```

자세한 실행·오류 대응은 `memory/RUNBOOK.md`를 따른다.

## 구조

| 위치 | 역할 |
| --- | --- |
| `../workspace_seed/AGENTS.md` | 모든 작업 전 읽는 핵심 메모리와 안전 규칙 |
| `memory/` | 프로젝트 맥락, 결정 이력, 운영 절차, 검증된 교훈 |
| `HARNESS.md` | 에이전트가 반드시 지킬 실행 계약 |
| `system_prompt.md` | 모델의 기본 역할과 출력 형식 |
| `../workspace_seed/skills/precursor-evidence/` | PDF 텍스트 추출과 근거 정리 워크플로 |
| `inputs/` | 실행별 연구 질문 |
| `references/` | 사용자가 제공한 논문·SI 원본 (Git 비추적) |
| `outputs/` | 실행 결과 보고서 (Git 비추적) |
| `evals/` · `tests/` | 회귀 검증 기준과 저장소 계약 테스트 |

## 현재 상태

현재 `references/`의 두 논문은 합성 가능성 예측/재설계 방법론을 다룬다.
직접적인 전구체 조성이나 실험 조건의 근거가 충분한 합성 논문·SI가 추가되면,
후보 비교표의 근거 밀도가 크게 높아진다.

## Git 원칙

`.env`, 가상환경, 추출 캐시, 생성 보고서, 논문 PDF는 커밋하지 않는다.
질문·프롬프트·하네스·평가·코드·메모리는 커밋 대상으로 관리한다.
