# 전구체 근거 보고서 (Precursor Evidence Report)

## 1. Scope and sources reviewed

본 보고서는 제공된 두 편의 로컬 논문만을 대상으로, 특정 무기 결정에 대한 **추적 가능한(traceable) 전구체 경로**가 보고되어 있는지를 검토하였다. 외부 검색(Tavily)은 사용하지 않았으며, Supporting Information(SI) 원문은 제공되지 않았다.

검토한 출처:

| # | 파일명 | 문서 유형(서지 정보) |
|---|--------|----------------------|
| S1 | `Explainable Synthesizability Prediction of Inorganic Crystal Polymorphs Using Large.txt` | Angew. Chem. Int. Ed. 2025, 64, e202423950 (Kim, Schrier, Jung) — 합성가능성 **예측 방법론** 논문 |
| S2 | `synthesis-aware-materials-redesign-via-large-language-models.txt` | J. Am. Chem. Soc. 2025, 147, 39113−39122 (Choi, Kim, Jung) — 합성가능성 기반 **재설계(redesign) 방법론** 논문 |

**핵심 결론(요약):** 두 출처 모두 특정 무기 결정에 대한 실험적 전구체 경로(전구체 화학종, 비율, 온도, 분위기, 시간, 수율, 상 순도)를 **보고하지 않는다**. 두 논문 모두 합성가능성 *예측/재설계 방법론* 연구이며, 실험 합성 절차 논문이 아니다. 따라서 본 보고서에서 확인(confirmed)된 실험 전구체 조건은 **0건**이다.

## 2. Literature role classification

| 출처 | 논문의 역할 분류 | 분류 근거 (파일 + 페이지/섹션) |
|------|------------------|-------------------------------|
| S1 | **합성가능성 예측 방법론 논문** (예측 모델 개발·설명가능성 연구). 실험 합성 논문 아님 | 초록: "predict whether a hypothetical crystal structure can be synthesized and explain those predictions" (S1, p.1 of 10, Abstract). 데이터는 Materials Project DB(2024년 3월 검색) 기반이며 실험 절차 없음 (S1, p.2 of 10, Results and Discussion — Synthesizability Prediction) |
| S2 | **합성가능성 인지 재설계(generative redesign) 방법론 논문**. 실험 합성 논문 아님 | 초록: "transform synthetically infeasible inorganic crystal structures into synthetically feasible ones" (S2, p.39113, Abstract). "indirect experimental validation"으로 재설계 구조 34개가 문헌에 보고됨을 확인했다고 하나, 이는 본 논문 자체의 실험 합성이 아님 (S2, p.39113, Abstract) |

**방법론 vs. 실험 근거의 구분:**
- S1·S2의 "synthesizability score", "synthesizable/unsynthesizable" 판정은 **모델 예측 결과**이며, 실험실에서의 실제 합성 성공·조건을 의미하지 않는다 (S1, p.2 of 10; S2, p.39114, Crystal Synthesizability Prediction 섹션 — 임계값 0.852는 재보정된 모델 점수).
- S2의 "34 materials ... have indeed been experimentally reported in the literature" (S2, p.39113, Abstract)는 **제3자 문헌에 대한 간접 검증**이며, 해당 34개 물질의 전구체·조건이 제공된 텍스트 내에 인용되어 있지 않다. 이는 확인 근거가 아니라 **발견 리드(discovery lead)**로만 취급해야 한다.
- S1은 이전 연구[51]에서 "조성 정보만으로 합성가능성 및 **합성 전구체 예측**"을 수행했다고 언급한다 (S1, p.1–2 of 10, Introduction). 그러나 이는 **인용된 별도 선행 연구**에 대한 언급이며, 제공된 S1 텍스트 자체에는 전구체 예측 결과나 실험 검증 데이터가 포함되어 있지 않다. 선행 논문[51] 원문이 필요한 리드이다.

## 3. Candidate precursor comparison

제공된 두 출처에서 특정 무기 결정에 대한 전구체 후보는 **식별되지 않았다**. 비교 표는 아래와 같이 모든 필드가 `not reported`이다.

| Candidate | Role | Formula/normalized name | Quantity or ratio | Conditions | Reported outcome | Evidence status | Source locator | Notes |
|-----------|------|--------------------------|-------------------|------------|------------------|-----------------|----------------|-------|
| (후보 없음) | not reported | not reported | not reported | 온도: not reported / 분위기: not reported / 시간: not reported | 수율: not reported / 상 순도: not reported | not reported | S1 전체(제공된 p.1–2 및 이후 truncated 텍스트), S2 전체(제공된 p.39113–39114 및 이후 truncated 텍스트) | 두 논문 모두 특정 타깃 결정의 실험 합성 절차를 포함하지 않음 |

전구체 관련 모든 필드(화학적 동일성, 역할, 비율, 온도, 분위기, 지속시간, 수율, 상 순도)에 대해 두 출처 모두 `not reported`임을 명시한다.

## 4. Evidence notes with source locators

**S1 (Angew. Chem. Int. Ed. 2025, 64, e202423950)**
- 연구 목적은 가상 결정 구조의 합성가능성 **예측 및 설명**이며, 실험 합성 수행이 아니다 (S1, p.1 of 10, Abstract).
- 학습 데이터는 Materials Project에서 2024년 3월에 검색한 60,959개 합성됨/94,402개 가상 구조이며, 실험실 합성 기록이 아니라 데이터베이스 레이블이다 (S1, p.2 of 10, Results and Discussion — Synthesizability Prediction).
- 모델(StructGPT-FT, StoiGPT-FT, PU-GPT-embedding, PU-CGCNN) 성능 비교는 TPR/PREC/FPR 등 분류 지표이며, 전구체·반응 조건·수율 데이터가 아니다 (S1, p.2 of 10, 동일 섹션).
- 전구체 예측은 선행 연구[51]에 대한 인용으로만 존재한다: "fine-tuned LLM could be used to predict inorganic synthesizability and synthesis precursors given only compositional information.[51]" (S1, p.1–2 of 10, Introduction). 제공된 텍스트에 그 예측 결과나 실험 검증은 없음 → `not reported` (S1 본문 기준).
- SI 존재가 언급되나("Additional supporting information can be found online", S1, p.1 of 10) SI 원문이 제공되지 않아 SI 내용은 확인 불가 → `not reported`.

**S2 (J. Am. Chem. Soc. 2025, 147, 39113−39122)**
- 연구 목적은 비합성가능 구조를 합성가능 구조로 **알고리즘적으로 재설계**하는 프레임워크(SynCry-GPT)이다 (S2, p.39113, Abstract; p.39114, Results and Discussion — Crystal Structure Modification).
- 재설계 프롬프트는 "격자 파라미터와 원자 좌표만 수정"하도록 지시하며, 전구체나 반응 조건 생성이 아니다 (S2, p.39114, Crystal Structure Modification 섹션의 프롬프트 인용문).
- "간접 실험 검증"으로 상위 100개 재설계 구조 중 34개가 문헌에 실험 보고되었다고 하나, 해당 문헌들의 전구체·조건이 제공된 텍스트에 인용되어 있지 않다 (S2, p.39113, Abstract) → 전구체 조건 `not reported`.
- SI 존재가 언급되나("sı Supporting Information", S2, p.39113) SI 원문 미제공 → `not reported`.

**왜 실험 레시피로 사용할 수 없는가 (구체적 사유):**
1. 두 논문의 "synthesizable" 판정은 통계적 분류 점수(예: 임계값 0.852, S2 p.39114)이며, 실제 반응 조건·전구체·수율의 실험 관측이 아니다.
2. 두 논문 어디에도 전구체 화학종, 몰비, 반응 온도/분위기/시간, 수율, 상 순도(XRD 등) 데이터가 없다.
3. S2의 34개 "실험 보고" 물질은 제3자 문헌에 대한 사후 대조이며, 그 원문헌이 제공되지 않아 조건 추적이 불가능하다.
4. 모델이 생성한 것은 결정 구조(CIF-string)이지 합성 절차가 아니다 (S2, p.39114, Figure 1 설명 및 프롬프트).

## 5. Missing or conflicting information

**누락된 정보 (모두 `not reported`):**
- 타깃 무기 결정의 특정 화학식/조성: 두 출처 모두 개별 타깃 물질을 지정하지 않음 (MP-30 데이터베이스 전체 대상 방법론 연구).
- 전구체 화학적 동일성, 역할, 비율: not reported (S1, S2 전체).
- 반응 온도, 분위기, 지속시간: not reported.
- 수율, 상 순도(예: XRD 기반): not reported.
- 두 논문의 Supporting Information 원문: 미제공. SI에 예시 구조 목록·모델 세부사항이 있을 수 있으나, 방법론 논문의 SI라도 실험 전구체 조건이 포함될지는 미확인 — 확인을 위해서는 SI 원문 요청 필요.
- S1 인용문헌 [51](조성 기반 전구체 예측 선행 연구) 원문: 미제공. 전구체 *예측* 관련 유일한 리드이나, 예측이더라도 실험 확인은 아님.
- S2에서 "실험 보고됨"으로 언급된 34개 물질의 목록 및 원문헌 인용: 제공된 텍스트에 없음 (S2, p.39113, Abstract에 수치만 존재).

**상충 정보:** 제공된 범위 내에서 출처 간 직접적 상충은 없음. 다만 S1은 "설명(explanation) 중심", S2는 "재설계(generation) 중심"으로 목적이 다르며(S2, p.39114, Introduction에서 S1 계열 선행연구와의 차이를 명시), 이는 상충이 아니라 연구 목적의 구분이다.

## 6. Researcher review checklist

연구자가 직접 판단·확인해야 할 사항 (본 보고서는 구매·실험 실행을 권고하지 않음):

- [ ] 두 논문의 Supporting Information 원문을 확보하여, 예시 구조 목록·34개 실험 보고 물질의 원문헌 인용이 있는지 확인할 것.
- [ ] S1의 인용문헌 [51](전구체 예측 선행 연구) 원문을 확보할 것 — 단, 해당 논문도 *예측* 논문일 가능성이 높으므로 실험 근거 여부를 별도 판별할 것.
- [ ] S2의 34개 "실험 보고" 물질에 대해, 원문헌(실제 합성 논문)을 직접 확보하여 전구체·조건·수율·상 순도를 1차 문헌에서 확인할 것.
- [ ] 모델의 "synthesizable" 예측을 실험 성공으로 해석하지 않도록 연구 기록에서 예측 근거와 실험 근거를 명확히 분리할 것.
- [ ] 특정 타깃 결정이 정해지면, 해당 조성의 실험 합성 논문(예: ICSD 기반 원문헌, 합성 절차가 포함된 논문 및 SI)을 추가로 제공받아 본 추출 절차를 재수행할 것.
- [ ] 향후 실제 전구체 후보가 확보될 경우, 안전성 분류·스케일업·조달 가능성은 본 보고서가 아닌 연구자가 별도 검토할 사항임을 유념할 것.

---

**검증 상태 요약:** 확인된(confirmed) 실험 전구체 조건 0건 / 상충(conflicting) 0건 / 추론(inference) 0건 / not reported — 전구체 관련 전 필드. 두 출처 모두 합성가능성 **방법론** 논문이며 직접 실험 근거가 아님이 확인됨.

---

## Harness verification

- Accepted: True
- Evidence status present: True
- Missing required sections: none
