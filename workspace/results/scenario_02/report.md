# 전구체 증거 갭 맵 (Evidence-Gap Map) — 시나리오 2

## 1. Scope and sources reviewed

**연구 질문:** 목표 무기질 결정(조성 미확정)의 전구체 선정 전, 현재 로컬 문헌이 무엇을 확립하는지, 어떤 문서를 다음에 확보해야 하는지 파악.

**검토한 로컬 소스 (2건, 전부):**

| # | 파일명 | 문헌 정보 | 로컬 상태 |
|---|--------|-----------|-----------|
| S1 | `Explainable Synthesizability Prediction of Inorganic Crystal Polymorphs Using Large.txt` | Kim, Schrier, Jung, *Angew. Chem. Int. Ed.* 2025, 64, e202423950 | 본문 일부만 수록 (로컬 실행에서 절단됨). Supporting Information 미제공 |
| S2 | `synthesis-aware-materials-redesign-via-large-language-models.txt` | Choi, Kim, Jung, *J. Am. Chem. Soc.* 2025, 147, 39113–39122 | 본문 일부만 수록 (로컬 실행에서 절단됨). Supporting Information 미제공 |

**범위 한계:** 외부 검색(Tavily) 미사용. 두 소스 모두 "[Source truncated locally for this run]"으로 절단되어 후반부 페이지는 미검토. 양쪽 논문의 Supporting Information(SI)은 로컬에 없음.

---

## 2. Literature role classification

| 소스 | 문헌 유형 | 전구체 증거로서의 역할 | 분류 근거 (파일 + 페이지/섹션) |
|------|-----------|------------------------|-------------------------------|
| S1 | 계산/ML 방법론 논문 (합성가능성 *예측* 및 설명) | **실험 전구체 증거 없음.** 예측 모델의 입력·데이터·성능만 기술. 단, 조성만으로 전구체를 예측한 선행 연구[51]를 인용 → 문서 발견 리드로만 가치 | S1, p.1 (Abstract); p.1–2 (Introduction, ref [51] 언급); p.2 (Results and Discussion — Synthesizability Prediction) |
| S2 | 계산/ML 방법론 논문 (비합성가능 구조의 *재설계*) | **실험 전구체 증거 없음.** "간접적 실험 검증"으로 재설계 구조 34건이 문헌에 보고됨을 언급하나, 새 실험·전구체·조건은 보고하지 않음 | S2, p.39113 (Abstract); p.39114 (Figure 1 및 Results, SynCry-GPT) |

**분류 결론:** 두 로컬 논문 모두 예측 방법론 문헌이며, 어떤 특정 결정에 대한 실험적 전구체 조건(시약, 양, 비율, 온도, 분위기, 수율)을 확립하지 않는다. 하네스 가드레일에 따라 예측 논문에서 전구체 조건을 추론하지 않았다.

---

## 3. Candidate precursor comparison

로컬 소스에는 전구체 후보가 하나도 보고되어 있지 않다. 아래 표는 부재 필드를 `not reported`로 보존한다.

| Candidate | Role | Formula/normalized name | Quantity or ratio | Conditions | Reported outcome | Evidence status | Source locator | Notes |
|-----------|------|-------------------------|-------------------|------------|------------------|-----------------|----------------|-------|
| (후보 없음 — S1에서 추출 불가) | not reported | not reported | not reported | not reported | not reported | not reported | S1, p.1–2 (Abstract, Introduction, Results) | 예측 방법론 논문; 실험 전구체 데이터 없음 |
| (후보 없음 — S2에서 추출 불가) | not reported | not reported | not reported | not reported | not reported | not reported | S2, p.39113–39114 (Abstract, Figure 1, Results) | 재설계 방법론 논문; 실험 전구체 데이터 없음 |
| 선행 연구 ref [51] (Kim et al., 조성 기반 전구체 예측) — **문서 리드이며 로컬 소스 아님** | not reported | not reported | not reported | not reported | not reported | not reported (인용만 존재, 원문 미확보) | S1, p.1–2 (Introduction: "fine-tuned LLM could be used to predict inorganic synthesizability and synthesis precursors given only compositional information.[51]") | 확인 증거로 사용 불가. 원문 확보 전까지 어떤 전구체 주장도 인용 불가 |

---

## 4. Evidence notes with source locators

아래는 두 로컬 논문이 **직접** 뒷받침하는 주장만 기록한다 (모두 `confirmed`는 "논문이 이 내용을 기술한다"는 의미이며, 실험 조건의 확인이 아님).

**S1 (Angew. Chem. Int. Ed. 2025, 64, e202423950):**
- 결정 구조의 합성가능성을 예측하는 LLM/PU-learning 방법론을 다룬다. — `confirmed` (논문 성격). 위치: S1, p.1, Abstract.
- 데이터: Materials Project(2024년 3월 검색), 합성됨 60,959 + 가상 94,402 구조; Robocrystallographer로 텍스트 변환; MP30(단위셀 내 고유 원자 자리 ≤30) 및 10,000자 초과 설명 제외 후 100,195건(합성 38,347 + 가상 61,848); 20% hold-out 테스트. — `confirmed` (데이터셋 기술). 위치: S1, p.2, Results and Discussion — "Synthesizability Prediction".
- OpenAI GPT-4o-mini를 파인튜닝; 모델·프롬프트·파인튜닝 상세는 SI에 있음; GPT-3.5 기반 결과는 열등(Tables S3, S4); 변환 예시는 Figure S1. — `confirmed` (SI 존재 사실). 위치: S1, p.2, 동 섹션.
- 선행 연구에서 조성 정보만으로 합성가능성과 **합성 전구체 예측**을 수행했음을 언급. — `confirmed` (인용 사실). 단, 그 전구체 예측의 내용 자체는 로컬에 없음 → `not reported`. 위치: S1, p.1–2, Introduction, ref [51].
- SI가 온라인에 존재. — `confirmed`. 위치: S1, p.1, "Additional supporting information can be found online…".

**S2 (J. Am. Chem. Soc. 2025, 147, 39113–39122):**
- 비합성가능 구조를 합성가능 구조로 재설계하는 LLM 프레임워크(SynCry-GPT)를 제안. — `confirmed` (논문 성격). 위치: S2, p.39113, Abstract; p.39114, Figure 1.
- "간접적 실험 검증"으로 상위 100개 재설계 구조 중 34개가 문헌에 실험 보고됨을 주장. — `confirmed` (주장의 존재). 단, 34개 물질의 목록·원문헌·합성 조건은 절단된 로컬 범위에 없음 → `not reported`. 위치: S2, p.39113, Abstract.
- MP-30(총 원자 수 <30) 사용, 80% 학습/20% 테스트, GPT-4o-mini 파인튜닝; 성능은 선행 그래프 모델[32]·LLM 모델[31]보다 약간 우수(Table S1, SI); 모델 간 일관성 Figure S1; 가상 구조 12,389개 중 11,753개를 예측(이후 절단). — `confirmed` (기술 사실). 위치: S2, p.39114, Results.
- 투고 2025-05-08, 게재 2025-10-06. — `confirmed`. 위치: S2, p.39113, 받은 날짜란.

**상충 여부:** 두 논문 간 직접적 상충은 발견되지 않음. S2는 S1 계열 선행 연구[31, 58]를 인용하며 방법을 확장하는 후속 성격(S2, p.39114, Introduction). 다만 S2의 성능 비교 대상 수치는 SI(Table S1)에 있어 로컬 확인 불가 → `not reported`.

---

## 5. Missing or conflicting information

**목표 결정 관련 (결론 불가 영역):**
- 목표 조성·다형체가 미확정 → 어떤 전구체 후보도 매핑 불가. 두 논문 모두 특정 목표 물질을 다루지 않음.
- 전구체의 화학종, 순도, 몰비, 용매, 온도, 시간, 분위기, 수율 등 모든 실험 필드: `not reported` (S1, S2 전 범위).

**문서 수준 결측:**
- S1의 SI 미확보: 모델/프롬프트/파인튜닝 상세, Figure S1, Tables S3–S4 (S1, p.2에서 존재만 언급).
- S2의 SI 미확보: Table S1 (성능 비교), Figure S1 (모델 일관성), 34개 검증 물질의 목록 및 출처 가능성 (S2, p.39113–39114에서 존재만 언급).
- 두 소스 모두 로컬 텍스트가 절단됨: S1은 p.2 이후(총 10쪽 중), S2는 p.39114 이후(총 39113–39122 중) 미검토. 후반부에 추가 사례·표가 있을 수 있으나 현재로서는 `not reported`.
- S1의 ref [51] (조성 기반 전구체 예측 선행 논문) 원문 미확보 — 전구체 관련성이 가장 높은 인용이나 내용 확인 불가.
- S2의 34개 "문헌에 실험 보고된" 물질의 1차 실험 문헌 미확보.

**상충:** 로컬 범위 내 논문 간·논문 내 상충 없음. 단, SI 미확보 상태이므로 본문–SI 불일치 여부는 검증 불가.

---

## 6. Researcher review checklist

다음 문서를 검토할 순서를 3단계로 구분한다. 실험·구매·가열 조건 제안은 의도적으로 포함하지 않는다.

### 우선순위 1 — 두 로컬 논문이 직접 뒷받침하는 사항 (추가 문서 없이 확인 가능)
- [ ] 두 논문이 예측/재설계 방법론 문헌이며 실험 전구체 증거를 포함하지 않음을 연구 기록에 명시 (S1 p.1 Abstract; S2 p.39113 Abstract).
- [ ] S1의 데이터 기준(MP 2024-03, MP30 필터)이 향후 목표 결정의 예측 적용 범위와 부합하는지 검토 (S1, p.2, Synthesizability Prediction).
- [ ] S2의 재설계 프레임워크 입력 형식(MP-CIF string)이 보유한 목표 구조 데이터와 호환되는지 검토 (S2, p.39114, Figure 1).

### 우선순위 2 — SI 또는 인용 1차 문헌에 존재할 수 있는 정보 (다음에 확보할 문서)
- [ ] **S2의 Supporting Information 확보** — 34개 실험 보고 물질의 목록과 그 1차 문헌 인용이 SI에 있을 가능성이 가장 높음 (존재 근거: S2, p.39113 Abstract; p.39114 Table S1/Figure S1 언급). → 전구체 1차 문헌으로 연결되는 최우선 문서.
- [ ] **S1의 ref [51] 원문 확보** — "조성만으로 합성 전구체 예측"을 다룬 선행 논문 (인용 위치: S1, p.1–2, Introduction). 전구체 후보 도출과 가장 직접적으로 관련된 인용.
- [ ] **S1의 Supporting Information 확보** — 모델 상세 및 Tables S3–S4 (존재 근거: S1, p.2).
- [ ] **두 논문의 전체 본문(절단되지 않은 PDF) 확보** — S1 p.3–10, S2 p.39115–39122 미검토분. 후반부에 사례 연구·표가 있을 수 있음.
- [ ] S2가 인용하는 선행 그래프 모델[32] 및 LLM 모델[31] 원문 — 성능 비교의 근거 확인용 (S2, p.39114).

### 우선순위 3 — 목표 결정이 지정되기 전에는 결론 불가한 정보
- [ ] 목표 조성 및 다형체 확정 — 이 없이는 어떤 문서도 전구체 후보를 특정할 수 없음.
- [ ] 목표 결정에 대한 전구체 화학종·비율·반응 조건 — 로컬 문헌 전부 `not reported`; 목표 확정 후 우선순위 2의 1차 문헌에서 탐색.
- [ ] 목표 결정의 합성가능성 판단 자체 — 예측 모델 출력은 참고 리드일 뿐 실험 확인 증거가 아님을 연구자가 유의.

**검토자 주의사항:** 본 보고서의 모든 `confirmed`는 "해당 논문이 이 내용을 기술한다"는 서지적 확인이며, 실험 조건·전구체 유효성의 확인이 아니다. 예측 논문(S1, S2)에서 전구체 조건·수율·실험 성공을 추론하지 말 것. 시약 조달, 안전 분류, 실험 실행 여부는 본 보고서의 범위 밖이며 연구자 판단 사항이다.

---

## Harness verification

- Accepted: True
- Evidence status present: True
- Missing required sections: none
