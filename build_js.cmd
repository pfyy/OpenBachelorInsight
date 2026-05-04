call npx esbuild --bundle src\inject\main.ts --outfile=rel\main.js
call npx esbuild --bundle src\inject\reader.ts --outfile=rel\reader.js
pause
