import re

with open('assets/css/app.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. 1페이지 2페이지 사이 글들 정리해 (break-after: avoid on subheadings)
# Find: .letter__text .subheading { display: block; font-size: 11.5pt; color: #004080; font-weight: bold; margin-top: 4mm; margin-bottom: 1.5mm; }
# Replace with: .letter__text .subheading { display: block; font-size: 11.5pt; color: #004080; font-weight: bold; margin-top: 4mm; margin-bottom: 1.5mm; break-after: avoid; page-break-after: avoid; }
css = css.replace(
    ".letter__text .subheading { display: block; font-size: 11.5pt; color: #004080; font-weight: bold; margin-top: 4mm; margin-bottom: 1.5mm; }",
    ".letter__text .subheading { display: block; font-size: 11.5pt; color: #004080; font-weight: bold; margin-top: 4mm; margin-bottom: 1.5mm; break-after: avoid; page-break-after: avoid; }"
)

# 2. 마무리 말 글씨 다르네 해결 (make .letter__closing match .letter__body)
# Find: .letter__closing { margin-top: 6mm; padding-top: 4mm; border-top: 1pt solid #ccc; font-size: 10pt; color: #333; text-align: justify; word-break: keep-all; }
# Replace with: .letter__closing { margin-top: 6mm; padding-top: 4mm; border-top: 1pt solid #ccc; font-size: 10.5pt; line-height: 1.6; color: #1a1a1a; text-align: justify; word-break: keep-all; break-inside: avoid; }
css = css.replace(
    ".letter__closing { margin-top: 6mm; padding-top: 4mm; border-top: 1pt solid #ccc; font-size: 10pt; color: #333; text-align: justify; word-break: keep-all; }",
    ".letter__closing { margin-top: 6mm; padding-top: 4mm; border-top: 1pt solid #ccc; font-size: 10.5pt; line-height: 1.6; color: #1a1a1a; text-align: justify; word-break: keep-all; break-inside: avoid; }"
)

# 3. 사역 동참하기/계좌번호 자동 제거
# Find:   .support {
#    margin-top: 6mm; padding-top: 4mm; border-top: 1pt solid #ccc; break-inside: avoid;
#  }
# Replace with:   .support { display: none !important; }
css = re.sub(
    r'\.support \{\s*margin-top: 6mm; padding-top: 4mm; border-top: 1pt solid #ccc; break-inside: avoid;\s*\}',
    '.support { display: none !important; }',
    css
)
css = css.replace(
    ".support__title { font-size: 11pt; font-weight: bold; color: #1a2b45; margin: 0 0 2mm; }",
    ".support__title { display: none !important; }"
)
css = css.replace(
    ".support__account { display: block; margin: 0; }",
    ".support__account { display: none !important; }"
)
css = css.replace(
    ".support__row { display: block; padding: 1mm 0; font-size: 10pt; border-bottom: 1pt dotted #ccc; }",
    ".support__row { display: none !important; }"
)
css = css.replace(
    ".support__row dt { display: inline; font-weight: bold; }",
    ".support__row dt { display: none !important; }"
)
css = css.replace(
    ".support__row dd { display: inline; margin-left: 2mm; }",
    ".support__row dd { display: none !important; }"
)
css = css.replace(
    ".support__note { font-size: 9pt; color: #555; margin-top: 2mm; }",
    ".support__note { display: none !important; }"
)

with open('assets/css/app.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated print CSS to v3")
