import sys, re

file_path = 'assets/css/app.css'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Replace the @media print .prayers section
target_print = """  /* 2번 파일 스타일: 은은한 연두색 배경 박스 + 진초록 테두리 + 빨간색 기도제목 번호 */
  .prayers {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
    border: 1pt dashed #4caf50 !important;
    background: #f1f8e9 !important;
    border-radius: 6px !important;
    padding: 3mm !important;
    margin: 3mm 0 !important;
    width: 100% !important;
    box-sizing: border-box !important;
    break-inside: avoid;
    page-break-inside: avoid;
  }
  .prayers__title { 
    font-size: calc(11pt * var(--print-scale, 1)) !important; 
    margin: 0 0 2mm !important;  
    color: #2e7d32 !important; 
    font-weight: bold; 
    text-align: left !important; 
    display: block; 
  }
  .prayers__list { padding-left: 0; list-style: none; margin: 0; display: block; counter-reset: prayer; }
  .prayers__item { 
    display: block; 
    padding: 1.5mm 0 !important; 
    border-top: 0.5pt dashed #a5d6a7 !important; 
    margin-top: 1mm !important; 
  }
  .prayers__item:first-child { border-top: none !important; padding-top: 0 !important; margin-top: 0 !important; }
  .prayers__item::before { 
    content: counter(prayer) ". "; 
    font-size: calc(10pt * var(--print-scale, 1)); 
    color: #c62828 !important; 
    font-weight: bold; 
    display: inline; 
  }
  .prayers__name { 
    font-size: calc(10pt * var(--print-scale, 1)) !important; 
    color: #c62828 !important; 
    font-weight: bold; 
    margin: 0; 
    display: inline; 
  }
  .prayers__text { 
    font-size: calc(9.5pt * var(--print-scale, 1)) !important; 
    color: #1a1a1a !important; 
    display: block; 
    margin-top: 1mm; 
    line-height: 1.45; 
    text-align: justify; 
  }
  .prayers__text p { margin: 0 0 0.5mm; border: none; padding: 0; text-indent: 0; }"""

replacement_print = """  /* PDF 레퍼런스 스타일 완벽 반영 */
  .prayers {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
    border: none !important;
    background: transparent !important;
    padding: 0 !important;
    margin: 3mm 0 !important;
    width: 100% !important;
    box-sizing: border-box !important;
    break-inside: avoid;
    page-break-inside: avoid;
  }
  .prayers__title { 
    font-size: calc(10.5pt * var(--print-scale, 1)) !important; 
    margin: 0 0 2mm !important;  
    color: #000 !important; 
    background: #e8f5e9 !important; /* 연두색 배경 */
    border: 1px solid #000 !important; /* 검정 테두리 */
    padding: 1mm 3mm !important;
    font-weight: bold; 
    text-align: center !important; 
    display: inline-block !important; /* 글자 크기만큼만 박스 생성 */
  }
  .prayers__list { padding-left: 0; list-style: none; margin: 0; display: block; counter-reset: prayer; }
  .prayers__item { 
    display: block; 
    padding: 0 !important; 
    border-top: none !important; 
    margin-top: 1.5mm !important; 
  }
  .prayers__item:first-child { margin-top: 0 !important; }
  .prayers__item::before { 
    content: counter(prayer) ". "; 
    font-size: calc(10pt * var(--print-scale, 1)); 
    color: #ff0000 !important; 
    font-weight: bold; 
    display: inline; 
  }
  .prayers__name { 
    font-size: calc(10pt * var(--print-scale, 1)) !important; 
    color: #ff0000 !important; 
    font-weight: bold; 
    margin: 0; 
    display: inline; 
  }
  .prayers__text { 
    font-size: calc(9.5pt * var(--print-scale, 1)) !important; 
    color: #000 !important; 
    display: block; 
    margin-top: 0.5mm; 
    line-height: 1.45; 
    text-align: justify; 
  }
  .prayers__text p { margin: 0 0 0.5mm; border: none; padding: 0; text-indent: 0; }"""

code = code.replace(target_print, replacement_print)

# Now for .is-measuring-print
target_measure = """.is-measuring-print .prayers {
  padding: 3mm !important;
  margin: 3mm 0 !important;
}"""

replacement_measure = """.is-measuring-print .prayers {
  padding: 0 !important;
  margin: 3mm 0 !important;
  border: none !important;
}
.is-measuring-print .prayers__title {
  padding: 1mm 3mm !important;
  border: 1px solid #000 !important;
  display: inline-block !important;
}
.is-measuring-print .prayers__item {
  padding: 0 !important;
  border-top: none !important;
  margin-top: 1.5mm !important;
}
.is-measuring-print .prayers__item:first-child { margin-top: 0 !important; }
.is-measuring-print .prayers__item::before {
  content: counter(prayer) ". ";
}
.is-measuring-print .prayers__text {
  margin-top: 0.5mm !important;
}
.is-measuring-print .prayers__text p {
  margin: 0 0 0.5mm !important;
  padding: 0 !important;
}"""

code = code.replace(target_measure, replacement_measure)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("patched pdf prayers")
