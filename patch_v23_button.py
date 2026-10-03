import sys, re

file_path = 'assets/js/views/write_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Add the new "PDF 형태 미리보기" button next to the regular preview button
target_buttons = """      <div class="actions">
        <button class="btn btn--outline" @click="showPreview = true">미리보기</button>
        <button class="btn btn--primary" @click="handlePrint">
          <i class="icon-download"></i> PDF로 저장
        </button>"""

new_buttons = """      <div class="actions">
        <button class="btn btn--outline" @click="showPreview = true">미리보기</button>
        <button class="btn btn--outline" @click="handlePdfPreview">PDF 확인</button>
        <button class="btn btn--primary" @click="handlePrint">
          <i class="icon-download"></i> PDF 저장
        </button>"""
code = code.replace(target_buttons, new_buttons)

# Add the handlePdfPreview method
target_method = """    async handlePrint() {"""
new_method = """    async handlePdfPreview() {
      if (this.isPrinting) return;
      this.isPrinting = true;
      try {
        const root = document.getElementById('temp');
        root.innerHTML = '';
        root.style.display = 'block';
        
        // Hide UI
        document.getElementById('nav').style.display = 'none';
        const toast = document.getElementById('toast');
        if (toast) toast.style.display = 'none';
        
        await printLetter(root, status => {
           // status update if needed
        }, true); // isPreview = true!
        
        // We do not restore UI because the user is now in Preview Mode!
        // We will add a "Back" button to the preview DOM to let them return.
        const backBtn = document.createElement('button');
        backBtn.textContent = '← 편집으로 돌아가기';
        backBtn.style.position = 'fixed';
        backBtn.style.top = '20px';
        backBtn.style.left = '20px';
        backBtn.style.padding = '10px 20px';
        backBtn.style.background = '#CE1126';
        backBtn.style.color = '#fff';
        backBtn.style.border = 'none';
        backBtn.style.borderRadius = '5px';
        backBtn.style.cursor = 'pointer';
        backBtn.style.zIndex = '9999';
        backBtn.onclick = () => {
            window.location.reload(); // Quickest way to restore state!
        };
        document.body.appendChild(backBtn);
        
      } catch (err) {
        console.error(err);
        alert('미리보기 중 오류가 발생했습니다.');
      } finally {
        this.isPrinting = false;
      }
    },
    
    async handlePrint() {"""
code = code.replace(target_method, new_method)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V23 patches: added PDF preview button")
