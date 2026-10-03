import sys, re

file_path = 'assets/css/app.css'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Add green box styles to print CSS
print_css_rules = """
  /* 기도편지 박스 스타일 (녹색 바탕) */
  .print-prayer-box {
    background-color: #f0fdf4 !important;
    border: 1px solid #166534 !important;
    padding: 15px !important;
    margin-top: 10px !important;
    break-inside: avoid !important;
    display: block !important;
  }
  .print-prayer-title-wrapper {
    background-color: #fff !important;
    border: 1px solid #166534 !important;
    padding: 4px 8px !important;
    display: inline-block !important;
    margin-bottom: 10px !important;
  }
  .print-prayer-box .prayers__title {
    margin: 0 !important;
    font-size: calc(13pt * var(--print-scale, 1)) !important;
    color: #000 !important;
    font-weight: 800 !important;
  }
  .print-prayer-list {
    list-style: none !important;
    padding: 0 !important;
    margin: 0 !important;
    display: block !important;
  }
  .print-prayer-item {
    margin-bottom: 8px !important;
    display: block !important;
  }
  .print-prayer-item::before {
    display: none !important; /* Hide original counters */
  }
  .print-prayer-num {
    color: #dc2626 !important;
    font-size: calc(10pt * var(--print-scale, 1)) !important;
    font-weight: bold !important;
    display: block !important;
  }
  .print-prayer-desc {
    margin: 2px 0 0 0 !important;
    font-size: calc(9pt * var(--print-scale, 1)) !important;
    color: #000 !important;
    line-height: 1.4 !important;
  }
  
  /* 동참하기(후원계좌) 인쇄에서 숨기기 */
  .support {
    display: none !important;
  }
"""

code = code.replace('@media print {', '@media print {' + print_css_rules)

# Update screen CSS to handle the same layout for web view (if needed) but keep it simple
# Actually, the user says "두손모아기도해주세요는 이전에 기도편지를 첨부했으니 형식을 그대로 바꿔줘"
# I will only apply this inside the print view or universally? The user said "바꿔줘", maybe universally.
# Let's apply it universally to be safe!
universal_rules = """
.print-prayer-box {
  background-color: #f0fdf4;
  border: 1px solid #166534;
  padding: 15px;
  margin-top: 10px;
}
.print-prayer-title-wrapper {
  background-color: #fff;
  border: 1px solid #166534;
  padding: 4px 8px;
  display: inline-block;
  margin-bottom: 10px;
}
.print-prayer-box .prayers__title {
  margin: 0;
  font-size: 18px;
  color: #000;
  font-weight: 800;
}
.print-prayer-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.print-prayer-item {
  margin-bottom: 8px;
}
.print-prayer-num {
  color: #dc2626;
  font-size: 15px;
  font-weight: bold;
  display: block;
}
.print-prayer-desc {
  margin: 2px 0 0 0;
  font-size: 14px;
  color: #000;
  line-height: 1.4;
}
.print-prayer-item::before { display: none; }
"""

code += universal_rules

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied green box CSS and hid support section")
