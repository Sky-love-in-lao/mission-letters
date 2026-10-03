import sys

file_path = 'assets/js/views/write_v2.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target_listeners = """  $('#preview-btn', root).onclick = () => preview();
  $('#deploy-btn', root).onclick = () => deploy(root);
  $('#pdf-btn', root).onclick = async e => {"""

new_listeners = """  $('#preview-btn', root).onclick = () => preview();
  $('#deploy-btn', root).onclick = () => deploy(root);
  
  $('#pdf-preview-btn', root).onclick = async e => {
    e.preventDefault();
    if (e.target.disabled) return;
    
    // Save draft first
    state.isEdit ? saveEditStatus() : saveStatus();
    
    e.target.disabled = true;
    e.target.textContent = '생성 중...';
    
    try {
      const tempRoot = document.getElementById('temp');
      tempRoot.innerHTML = '';
      tempRoot.style.display = 'block';
      
      // Hide UI
      document.getElementById('app').style.display = 'none';
      
      // Call printLetter in PREVIEW mode
      await printLetter(tempRoot, status => {
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
          tempRoot.innerHTML = '';
          tempRoot.style.display = 'none';
          document.body.style.background = '';
          document.body.style.padding = '';
          document.getElementById('app').style.display = '';
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
  };

  $('#pdf-btn', root).onclick = async e => {"""

code = code.replace(target_listeners, new_listeners)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied V25 listener patch")
