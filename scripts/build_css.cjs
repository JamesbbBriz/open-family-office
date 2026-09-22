const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');let pkg;
try{pkg=require.resolve('tailwindcss/package.json',{paths:[root]});}catch(e){if(!process.env.TAILWIND_PACKAGE_DIR)throw new Error('Run npm install or set TAILWIND_PACKAGE_DIR to a local Tailwind compiler.');pkg=path.join(process.env.TAILWIND_PACKAGE_DIR,'package.json');}
const dir=path.dirname(pkg),tw=require(path.join(dir,'dist/lib.js'));
(async()=>{const theme=fs.readFileSync(path.join(dir,'theme.css'),'utf8'),preflight=fs.readFileSync(path.join(dir,'preflight.css'),'utf8');
const sources=['dashboard.html','dashboard.js','landing.html','shared.css','landing.js','sandbox.js'];
const text=sources.filter(f=>fs.existsSync(path.join(root,'site',f))).map(f=>fs.readFileSync(path.join(root,'site',f),'utf8')).join('\n');
const candidates=[...new Set(text.match(/[A-Za-z0-9_!@:[\].\/-]+/g)||[])];
const subset=fs.readFileSync(path.join(root,'vendor/daisyui/components.source.css'),'utf8');
const css='@layer theme,base,daisyui,components,utilities;@layer theme{'+theme+'}'+
'@theme inline{--color-base-100:var(--of-base);--color-base-200:var(--of-soft);--color-base-content:var(--of-ink);--radius-box:var(--of-box);--radius-selector:var(--of-selector);}' +
'@layer base{'+preflight+'}'+subset+'@tailwind utilities;';
const compiler=await tw.compile(css);const out=compiler.build(candidates);fs.writeFileSync(path.join(root,'site/tailwind.generated.css'),out);console.log('Compiled Tailwind '+JSON.parse(fs.readFileSync(pkg)).version+' + daisyUI source subset: '+out.length+' bytes');})();
