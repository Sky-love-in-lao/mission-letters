const fs = require('fs');
const file = 'assets/js/views/write_v2.js';
let code = fs.readFileSync(file, 'utf8');

const target = `      textarea.setSelectionRange(start + 2, start + 2 + selectedText.length);
    };
  });`;

const replacement = `      textarea.setSelectionRange(start + 2, start + 2 + selectedText.length);
    };
  });

  $$('.block__format select[data-action=color]', wrap).forEach(select => {
    select.onchange = () => {
      const color = select.value;
      if (!color) return;
      
      const i = Number(select.dataset.i);
      const textarea = wrap.querySelector(\`textarea[data-i="\${i}"]\`);
      if (!textarea) return;
      
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const text = textarea.value;
      
      let selectedText = text.substring(start, end);
      if (!selectedText) selectedText = "글자";
      
      const prefix = \`[c:\${color}|\`;
      const suffix = \`]\`;
      const newText = text.substring(0, start) + prefix + selectedText + suffix + text.substring(end);
      textarea.value = newText;
      state.body.blocks[i].value = newText;
      persist(root);
      
      select.value = ""; // reset
      textarea.focus();
      textarea.setSelectionRange(start + prefix.length, start + prefix.length + selectedText.length);
    };
  });`;

code = code.replace(target, replacement);
fs.writeFileSync(file, code);
console.log('patched');
