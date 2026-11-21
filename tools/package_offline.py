"""Bundle the current buildless app as a self-contained HTML for venue use."""
from pathlib import Path
import base64, re, mimetypes, shutil
ROOT=Path(__file__).resolve().parents[1]
front=ROOT/'frontend'
assets=front/'assets'
doc=ROOT/'docs/2026_지방시대엑스포_토론문_이수화_개정본.docx'
pdf=doc.with_suffix('.pdf')
shutil.copy2(doc,assets/'core2050-proposal.docx')
shutil.copy2(pdf,assets/'core2050-proposal.pdf')
html=(front/'index.html').read_text(encoding='utf8')
html=html.replace('href="assets/core2050-proposal.pdf" target="_blank" rel="noopener"','href="assets/core2050-proposal.pdf" download="CORE2050_발제문.pdf"')
css=(assets/'core.css').read_text(encoding='utf8')
data=(assets/'core-data.js').read_text(encoding='utf8')
js=(assets/'core.js').read_text(encoding='utf8')
def uri(f):
    mime=mimetypes.guess_type(f.name)[0] or 'application/octet-stream'
    return 'data:'+mime+';base64,'+base64.b64encode(f.read_bytes()).decode('ascii')
css=css.replace("url('PretendardVariable.woff2')",'url('+uri(assets/'PretendardVariable.woff2')+')')
html=re.sub(r'<link rel="stylesheet"[^>]+>',lambda m:'<style>'+css+'</style>',html)
html=re.sub(r'<script defer src="assets/core-data.js[^>]+></script>',lambda m:'<script>'+data+'</script>',html)
html=re.sub(r'<script defer src="assets/core.js[^>]+></script>','',html)
for name in ['terrain.webp','qr_core2050.png']:
    js=js.replace('assets/'+name,uri(assets/name))
html=html.replace('</body>','<script>'+js+'</script></body>')
for name in ['scar_honor_hero.jpg','sunshine_dure_lounge.jpg','core-mark.svg','core2050-proposal.docx','core2050-proposal.pdf']:
    html=html.replace('"assets/'+name+'"','"'+uri(assets/name)+'"')
out=ROOT/'docs/core2050_standalone_singlefile.html';out.write_text(html,encoding='utf8')
print('Offline HTML:',out.stat().st_size,'bytes')
