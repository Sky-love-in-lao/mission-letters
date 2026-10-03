const fs = require('fs');

// We can't easily run the DOM paginator in Node.js because it requires a real browser layout engine (scrollWidth, clientWidth).
// So we can't perfectly simulate the paginator here.
// BUT we can create an HTML file that the USER can open, which automatically runs the paginator and DISPLAYS the result instead of printing it!
