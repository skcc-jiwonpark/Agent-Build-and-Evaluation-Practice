# Harness validation cases

## Case 1 Methodology papers without precursor procedures

Input: Papers that discuss inorganic-crystal synthesizability prediction or redesign, without a target composition, experimental procedure, or Supporting Information.

Expected result:
- Classify the papers as methodology or synthesizability background.
- Do not output a confirmed precursor, ratio, temperature, time, or yield.
- Mark experimental precursor evidence as `not reported`.

## Case 2 Experimental procedure and Supporting Information

Input: A target composition plus at least one paper or Supporting Information file containing an experimental procedure.

Expected result:
- Extract candidate identity, role, ratio, conditions, outcome, and source locator.
- Flag values missing from the source rather than estimating them.
- Flag disagreement between main paper and Supporting Information as `conflicting`.

## Case 3 Web-discovered literature lead

Input: The same question with `--search` enabled.

Expected result:
- Use Tavily results only as unverified discovery leads.
- Do not mark a search snippet as confirmed evidence until the paper is added to `references/` and inspected locally.
