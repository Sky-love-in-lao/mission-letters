import sys, re

file_path = 'assets/js/views/write_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target_buttons = """        <button type="button" class="btn btn--ghost" id="preview-btn">미리보기</button>
        <button type="button" class="btn btn--ghost" id="pdf-btn">PDF로 저장</button>"""

new_buttons = """        <button type="button" class="btn btn--ghost" id="preview-btn">미리보기</button>
        <button type="button" class="btn btn--ghost" id="pdf-preview-btn">PDF 확인</button>
        <button type="button" class="btn btn--ghost" id="pdf-btn">PDF로 저장</button>"""

code = code.replace(target_buttons, new_buttons)

target_listeners = """  $('#preview-btn').addEventListener('click', preview);
  $('#pdf-btn').addEventListener('click', async (e) => {"""

new_listeners = """  $('#preview-btn').addEventListener('click', preview);
  $('#pdf-preview-btn').addEventListener('click', async (e) => {
    e.preventDefault();
    if (e.target.disabled) return;
    
    // Save draft first
    state.isEdit ? saveEditStatus() : saveStatus();
    
    e.target.disabled = true;
    e.target.textContent = '생성 중...';
    
    try {
      const root = $('#temp');
      root.innerHTML = '';
      root.style.display = 'block';
      
      // Hide UI
      $('#app').style.display = 'none';
      
      // Call printLetter in PREVIEW mode
      await printLetter(root, status => {
         // UI updates if needed
      }, true);
      
      // Add a back button
      const backBtn = document.createElement('button');
      backBtn.textContent = '← 편집으로 돌아가기';
      backBtn.style.position = 'fixed';
      backBtn.style.top = '20px';
      backBtn.style.left = '20px';
      backBtn.style.padding = '12px 24px';
      backBtn.style.background = '#CE1126';
      backBtn.style.color = '#fff';
      backBtn.style.border = 'none';
      backBtn.style.borderRadius = '5px';
      backBtn.style.cursor = 'pointer';
      backBtn.style.zIndex = '9999';
      backBtn.style.fontSize = '16px';
      backBtn.style.boxShadow = '0 4px 6px rgba(0,0,0,0.3)';
      backBtn.onclick = () => {
          root.innerHTML = '';
          root.style.display = 'none';
          document.body.style.background = '';
          document.body.style.padding = '';
          $('#app').style.display = '';
          backBtn.remove();
      };
      document.body.appendChild(backBtn);
      
    } catch (err) {
      console.error(err);
      alert('오류가 발생했습니다.');
    } finally {
      e.target.disabled = false;
      e.target.textContent = 'PDF 확인';
    }
  });

  $('#pdf-btn').addEventListener('click', async (e) => {"""

code = code.replace(target_listeners, new_listeners)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V25 button patch")
