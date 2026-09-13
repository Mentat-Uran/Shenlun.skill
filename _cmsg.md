拆分为三个 skill：router + 小题 + 大作文

背景：单文件 SKILL.md 累积到 404 行 / 9547 非空白字符，
而它按 skill 调用整体加载——小题任务也要付大作文整库的成本。
上一层瘦身只降 27%（再压就得削掉刚加的门控与禁令），故按需求拆分为三个 skill。

架构：

  skills/
  ├── shenlun-router/     总调度：输入处理 · 真题识别 · 命题预判 · 错题库 · 分派
  │   └── references/prediction-methodology.md
  ├── shenlun-xiaoti/     小题：归纳概括／综合分析／对策／公文，双视角作答
  │   └── references/  bai-lu · xiaoma · scoring-rules · writing-rules · real-exams/
  ├── shenlun-dawenti/    大作文：袁东体系、四类文评分、无题干兜底评改
  │   └── references/  yuan-dong-methodology · fallback-eval-rules
  └── shared/             三者共用
      ├── references/  error-bank-rules · expression-upgrade-rules · image-reading-rules
      └── scripts/export_docx.py

效果：小题任务加载 router + xiaoti + 白鹭或小马哥库 + 评分规则（约 15k 字符）；
大作文任务加载 router + dawenti + 袁东库（约 16k 字符）——两条路径互不加载对方材料。

关键实现细节：

1. 三个 skill 必须各自作为技能目录的直接子目录
   （读 dsh-skill-filesystem 源码确认：discoverRoot 单层扫描，
   只认 <root>/<name>/SKILL.md，不递归）。故仓库内建 skills/ 容器，
   由三个 junction 分别指入——README 已写明安装方式（Junction 免管理员权限）。

2. 跨 skill 相对路径统一改为 ../shared/references/、../shenlun-*/references/
   形式（skill 基目录即各 skill 文件夹，与 junction 目标一致）。
   已用脚本校验：markdown 内 25 处引用 + 三个 SKILL.md 内 11 处引用，全部可解析。

3. 共用资源归 shared/（而非复制三份），避免口径分岔——
   这是本项目反复踩过的坑（同一规则两处维护会不一致）。

4. 错题库仍由 router 统一负责（跨题型），小题/大作文 SKILL.md 末尾
   各自明确指向它，避免"批改完忘记记录"。

5. README 更新：新增「架构」与「安装」两节；更正已过时的功能描述
   （原写"3W 十六字方针""分论点三步搜索法"均已被真题样本证伪）。

校验：三个 skill 已能被技能目录识别（catalog 已出现 shenlun-router /
shenlun-xiaoti / shenlun-dawenti）；frontmatter 三项有效；引用 0 失效。
