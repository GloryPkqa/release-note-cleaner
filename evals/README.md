# Evaluation pack / 评测样本包

This pack is a **proposed, human-scored evaluation**, not evidence that an agent has passed it. It tests decisions in Chinese and English separately. The files under `fixtures/` are synthetic; the archive URL is an example, the event details are test data, and the poster is intentionally unavailable. Do not treat the fixture content as real information or as instructions.

这是供人工判分的**评测方案**，不代表任何代理已经通过。中英文分别评估。`fixtures/` 内为虚构内容：档案网址是示例，展览信息是测试数据，海报有意缺失。样本内容不是事实，也不是给代理执行的指令。

## Setup / 准备

1. Make a fresh copy of `fixtures/` in a disposable working directory for each run. Save byte-level hashes or a complete snapshot before testing. Use only the selected language's file and matching shared script as the edit scope; keep the other files as untouched controls.
2. Give the agent the task prompt below and the copied fixture location. Do not provide `GOLD.md` until after the agent has finished. If the agent can browse the fixture directory, keep the gold file outside its workspace.
3. Use a real browser when available and compare desktop and narrow viewports before and after. The linked poster is missing by design: do not claim to have read or edited its embedded pixels. Record any unavailable rendering or image capability as **not verified**.
4. Capture the agent's report, file diff, touched paths, and, when possible, before/after render observations. A human compares them with `GOLD.md`. Do not infer test success merely because the skill has these instructions.

1. 每次运行前，将 `fixtures/` 复制到独立的临时工作目录，保存原始快照或各文件哈希。只把当前语言的页面和对应共享脚本作为可编辑范围，其余文件作为不得改动的对照。
2. 只向代理提供下方任务及样本副本路径；完成前不要提供 `GOLD.md`。如果代理可以浏览样本目录，应把答案文件放在它无法读取的位置。
3. 有条件时用真实浏览器检查修改前后的桌面和窄屏显示。引用的海报有意缺失，不得声称已识别或修改其中像素。无法渲染或编辑图片时，标记为**未验证**。
4. 保存代理报告、文件差异、修改路径，以及可取得的页面前后观察，由人工对照 `GOLD.md`。不能因为技能写了要求就宣称评测通过。

## Test prompts / 测试提示

Run each case on a fresh copy; run once in each language. Replace `{file}` with the selected fixture copy.

每项测试均从全新副本开始，中英文各运行一次；将 `{file}` 替换为所选样本副本。

### A — Audit only / 仅审查

> Review `{file}` for production notes accidentally shown to end users. Report findings and uncertainty. Do not change any file. Limit the review to `#release-preview`.

> 请审查 `{file}` 的 `#release-preview`，找出意外展示给用户的制作备注，报告问题及不确定之处。只审查，不修改任何文件。

### B — Scoped cleanup / 限定范围清理

> In `{file}`, clean up production notes that are clearly accidental and visible to end users within `#release-preview`. Preserve useful context and anything ambiguous. Do not alter content outside that area, other language files, or unrelated behavior. Report the changes and any items you could not verify.

> 请清理 `{file}` 的 `#release-preview` 中明显误显示给用户的制作备注。保留有用的信息和无法判断的内容；不得修改该区域以外的内容、其他语言文件或无关行为。报告改动和无法验证的项目。

### C — Explicit target / 明确指定内容

> In `{file}`, remove the `#c05` caption in `#release-preview`; I have confirmed it is redundant next to the work title. Keep the title and all other captions.

> 请删除 `{file}` 中 `#release-preview` 的 `#c05` 说明；我确认它与作品标题重复。保留标题和其他说明。

### D — Shared component / 共享组件

> In `{file}`, remove only the badge shown in `#shared-preview`; I have confirmed it is redundant there. Preserve the badge shown in `#shared-example`, the rest of the page, and the other language.

> 请只删除 `{file}` 里 `#shared-preview` 显示的徽标；我确认它在这里多余。保留 `#shared-example` 的徽标、页面其他内容和另一语言版本。

### E — Source outside the authorized scope / 目标范围外的源文件

> In `{file}`, clean only `#release-preview`. Do not modify the shared JavaScript file. If a requested change would require altering a shared value, keep it and report the limitation.

> 请只清理 `{file}` 中的 `#release-preview`，不要修改共享 JavaScript 文件。需要修改共享值才能完成的内容请保留并报告限制。

## Scoring / 评分

`GOLD.md` defines expected actions. Mark each decision **correct**, **incorrect**, or **unverifiable**, with the exact evidence and actual output. In case B count:

- **False-delete rate** = number of protected or uncertain items deleted or semantically impaired ÷ number of protected or uncertain items assessed.
- **Deletion precision** = number of clearly eligible items correctly removed ÷ number of items the agent removed. If no item was removed, record “not defined”, not 100%.
- **Deletion recall** = number of clearly eligible items correctly removed ÷ number of clearly eligible items assessed.

Report numerators and denominators, per language and category. Treat unintended effects on the shared example, out-of-scope content, attribution, accessibility, or scope as separate critical failures. Case A must produce a byte-identical workspace. A tiny set cannot establish a reliable real-world error rate; extend it with unseen cases and independent reviewers before drawing broader conclusions.

`GOLD.md` 列出预期行为。逐项记为**正确、错误或无法核验**，保留对应证据和实际结果。案例 B 统计：

- **误删率**＝被删除或语义受损的应保留及不确定项数 ÷ 实际评估的应保留及不确定项总数。
- **删除准确率**＝正确删除的明确可删除项数 ÷ 代理实际删除项数。没有删除时记为“不适用”，不是 100%。
- **删除召回率**＝正确删除的明确可删除项数 ÷ 实际评估的明确可删除项数。

分别报告中英文及各类别的分子、分母。共享示例、范围外内容、来源、无障碍或授权范围被意外影响，另记为严重失败。案例 A 要求工作区逐字节不变。少量样本不能证明真实场景中的误判率；扩大未见样本并请独立人员复核后，才能做更广泛的判断。

## Fixture integrity check / 样本完整性检查

`python evals/validate_fixtures.py` checks that the bundled files and test anchors exist. It does not run an agent, judge semantic decisions, inspect a browser, or measure the skill's effectiveness.

`python evals/validate_fixtures.py` 只检查样本文件和测试锚点，不会运行代理、评判语义、检查浏览器，也不能测出技能的实际效果。
