"""Build the two-page Korean discussion paper using python-docx and Pillow.
Run with the Codex bundled Python from the repository root. Render using Word or the packaged renderer.
"""
from pathlib import Path
import math, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from docx import Document
from docx.shared import Mm, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs'
ASSETS=ROOT/'frontend/assets'
OUT.mkdir(exist_ok=True)
FONT=Path('C:/Windows/Fonts/malgun.ttf')
FONT_BOLD=Path('C:/Windows/Fonts/malgunbd.ttf')
def font(n,bold=False): return ImageFont.truetype(str(FONT_BOLD if bold else FONT),n)
def figure():
    im=Image.new('RGB',(1700,510),'white'); d=ImageDraw.Draw(im)
    pts=[('풍기',128.525,36.871,60),('예산',126.849,36.682,66),('충주',127.926,36.991,44),('단양',128.365,36.984,43),('공주',127.124,36.455,41),('오송',127.329,36.625,26),('수도권',126.978,37.566,46)]
    def merc(lat): return math.log(math.tan(math.pi/4+lat*math.pi/360))
    def proj(lon,lat): return ((lon-125.8)/3.55*650,(merc(37.95)-merc(lat))/(merc(37.95)-merc(35.7))*370)
    terrain=Image.open(ASSETS/'terrain.webp').resize((650,370))
    for x,title,kind in [(0,'지역 자산을 찾는 히트맵','heat'),(685,'같은 기록 수의 로그 막대','bars')]:
        d.text((x+4,4),title,font=font(30,True),fill='#172a26')
        panel=terrain.copy()
        if kind=='heat':
            heat=Image.new('RGBA',(650,370));hd=ImageDraw.Draw(heat)
            for name,lon,lat,n in pts:
                px,py=proj(lon,lat)
                for radius,col in [(35,'#204bf168'),(26,'#02c5deaa'),(18,'#a75be6cc'),(10,'#fa638fdc')]:
                    rr=radius*math.sqrt(n/60)
                    hd.ellipse((px-rr,py-rr,px+rr,py+rr),fill=col)
            heat=heat.filter(ImageFilter.GaussianBlur(4));panel=Image.alpha_composite(panel.convert('RGBA'),heat).convert('RGB')
        pd=ImageDraw.Draw(panel)
        for name,lon,lat,n in pts:
            px,py=proj(lon,lat)
            if kind=='bars':
                py+=40;h=math.log10(n+1)/math.log10(67)*85
                pd.rectangle((px-6,py-h,px+7,py),fill='#96c9ae')
                pd.polygon([(px+7,py),(px+16,py-6),(px+16,py-h-6),(px+7,py-h)],fill='#53896f')
                pd.polygon([(px-6,py-h),(px+3,py-h-6),(px+16,py-h-6),(px+7,py-h)],fill='#e6efd3')
            pd.ellipse((px-3,py-3,px+3,py+3),fill='#fff0c2')
            if name in ('풍기','예산','수도권'):
                tx=px-72 if name=='예산' else px+12;ty=py-7
                box=pd.textbbox((tx,ty),name,font=font(27,True));pd.rectangle((box[0]-3,box[1]-4,box[2]+4,box[3]+3),fill='#142a25');pd.text((tx,ty),name,font=font(27,True),fill='#ffe8c0')
        im.paste(panel,(x,58))
    qr=Image.open(ASSETS/'qr_core2050.png').convert('RGB').resize((290,290),Image.Resampling.NEAREST)
    im.paste(qr,(1394,65));d.text((1395,371),'앱에서 직접 보기',font=font(27,True),fill='black')
    d.text((3,447),'지형은 공개 고도 자료 · 색과 막대는 실증 설계용 예시이며 경제효과의 증명이 아님',font=font(27),fill='#505c51')
    d.text((3,482),'core2050.soohwalee.com   |   풍토 지도 · 스카 마케팅 · AI 하방 · 100일 실증',font=font(24),fill='#505c51')
    im.save(OUT/'atlas-and-qr.png')

P1=[
('heading','소프트웨어 지능혁명을 지역정책의 중심에'),
('body','AI 정책의 성과는 주민이 자기 문제를 해결하고 그 결과를 소유할 능력을 얼마나 얻었는가로 평가해야 한다. 시설 유치와 부서별 서비스 도입을 나열하는 방식만으로는 이 변화에 답하기 어렵다. 나는 지역 주민을 AI 서비스의 이용자에서 생산자로 바꾸는 소프트웨어발 지능혁명을 균형발전 정책의 중심에 놓자고 제안한다.'),
('body','자연어로 작은 소프트웨어를 만들고 고칠 수 있는 환경에서, 현장의 결핍을 알고 결과를 판단하는 사람의 역할이 커진다. 농부와 상인, 숙련 노동자가 자기 일의 문제를 정의하고 AI에게 역할을 나누며 결과를 검증하는 국민개발자가 되어야 한다. 이를 뒷받침하는 공통 도구와 권한, 연결 규칙, 현장 지원망이 지능 에이전트 고속도로다.'),
('heading','풍기사과에서 예산사과로 이어지는 지역의 원본'),
('body','풍기 힐링스토리펜션에서 구상한 사과 마케팅은 이 전환을 작게 시험할 출발점이다. 소백산 남쪽 과수원의 굴곡과 계절, 사과를 지켜온 농부의 손, 펜션 주인의 환대는 하나의 지역 원본이다. 예산에서는 황토사과의 재배 역사와 농가의 경험, 가공과 체류의 조건을 다시 읽어야 한다. 같은 사과라도 땅의 냄새와 맛의 기억을 획일적인 홍보 문구로 덮어서는 안 된다.'),
('body','스카 마케팅은 외관의 흠을 숨기기보다 재배와 선별의 이력을 정직하게 드러내는 전략이다. 상처가 맛이나 기능성을 높인다고 단정하지 않는다. 식용 적합성을 확인한 사과에 농부의 말과 기록을 붙이고, AI가 이를 다음의 다섯 사업으로 구체화하도록 한다.')
]
ROWS=[
('맛','농가별 시식과 조리 경험','품종·수확일·시식 기록을 담은 소개'),
('체험','수확·사과청·숙성 기록','예약과 체험 기록을 연결하는 도구'),
('머무름','힐링스토리펜션의 딥워크 체류','실제 객실·호스트 조건에 맞춘 안내'),
('여행','과수원과 지역 문화의 연결','풍기·예산 각각의 맥락을 살린 해설'),
('산업','가공 적합 사과와 협업 생산','공동 주문·재고·원가·정산 소프트웨어')
]
P2=[
('heading','시니어 전문가와 AI 짚인간이 함께 일하는 마을방'),
('body','AI 하방은 경험 많은 전문가가 자발적으로 지역에 머물며 주민과 공동 작업하는 정책이다. 농부가 문제의 주인이고, 시니어는 분야의 판단력으로 설계를 돕고, 청년은 운영과 연결을 맡는다. 주민센터·도서관·지역대학의 기존 공간을 AI 마을방으로 열어, 실제 과제를 함께 끝내는 현대식 두레를 만들자.'),
('body','홍길동의 짚인간처럼 움직이는 AI 분신은 조사·기획·번역·제작·운영·검증의 역할을 나누어 맡는다. 한 사람의 현장 지식이 여러 작업으로 펼쳐지는 실행조직이다. 분신의 수가 곧 생산성은 아니다. 공개·계약·결제는 사람이 확인하고, 지역 지식의 이용 범위와 공동 제작물의 권리, 유지관리 책임을 먼저 정해야 한다.'),
('heading','첫 100일의 결과로 AI 햇살정책을 검증하자'),
('body','지방정부와 지역대학, 현장 전문가가 작은 공동 설계팀을 꾸려 3개 생활권, 주민 300명, 프로젝트 30개의 100일 실증을 시작하자. 이는 제안 규모다. 첫 20일은 주민의 과제와 기존 비용·시간을 기록하고, 50일까지 작은 도구를 만들며, 80일까지 현장에서 고친 뒤, 100일째 계속할 일과 멈출 일을 결정한다.'),
('body','공공은 기본 에이전트와 현장 지원을 보장하는 접근 배당, 구술·사진·업무 지식 제공에 정당한 대가를 지급하는 참여 배당, 실제 순수익을 약정에 따라 나누는 성과 배당을 연결해야 한다. AI 이용료와 운영비를 뺀 순수익, 반복 사용, 시간 절감, 재방문, 주민 만족을 기록하고 소프트웨어와 운영 지식을 지역에 남겨야 한다.'),
('body','이것이 내가 제안하는 AI 햇살정책이다. 지능 생산수단에 대한 접근과 성과의 권리를 주민에게 돌려주는 일이다. 풍기의 사과가 예산의 사과로 바뀔 때 복제할 것은 지역의 얼굴이 아니라, 각자의 고유함을 스스로 사업으로 키워내는 방법이다.')
]

def set_font(style,size,bold=False):
    style.font.name='맑은 고딕';style.font.size=Pt(size);style.font.bold=bold;style.font.color.rgb=RGBColor(0,0,0)
    style.element.get_or_add_rPr().rFonts.set(qn('w:eastAsia'),'맑은 고딕')
def para(doc,text,style='Normal',size=None):
    p=doc.add_paragraph(text,style=style)
    if size:
        for r in p.runs:r.font.size=Pt(size)
    return p
def table_borders(table):
    pr=table._tbl.tblPr;b=OxmlElement('w:tblBorders')
    for edge in ['top','left','bottom','right','insideH','insideV']:
        el=OxmlElement('w:'+edge);el.set(qn('w:val'),'single');el.set(qn('w:sz'),'4');el.set(qn('w:color'),'D9D9D9');b.append(el)
    pr.append(b)
    margins=OxmlElement('w:tblCellMar')
    for edge,num in [('top',70),('bottom',70),('left',95),('right',95)]:
        e=OxmlElement('w:'+edge);e.set(qn('w:w'),str(num));e.set(qn('w:type'),'dxa');margins.append(e)
    pr.append(margins)

def build():
    figure();doc=Document();sec=doc.sections[0];sec.page_width=Mm(210);sec.page_height=Mm(297)
    sec.top_margin=Mm(17);sec.bottom_margin=Mm(17);sec.left_margin=Mm(20);sec.right_margin=Mm(20)
    set_font(doc.styles['Normal'],10.5);set_font(doc.styles['Title'],20,True);set_font(doc.styles['Heading 1'],12,True)
    for border in list(doc.styles.element.iter(qn('w:pBdr'))): border.getparent().remove(border)
    normal=doc.styles['Normal'].paragraph_format;normal.line_spacing=Pt(17);normal.space_after=Pt(6)
    doc.styles['Title'].paragraph_format.space_after=Pt(8)
    h=doc.styles['Heading 1'].paragraph_format;h.space_before=Pt(12);h.space_after=Pt(6);h.keep_with_next=True
    doc.core_properties.author='이수화';doc.core_properties.title='지역의 고유성을 생산력으로 바꾸는 AI 하방 정책'
    p=para(doc,'2026 지방시대 엑스포 특별세션  |  지방자치분권 균형발전의 회고와 2050 비전 라운드테이블',size=8.5)
    p.paragraph_format.space_after=Pt(2)
    p=para(doc,'2026년 12월 10일  오송 C&V센터',size=8.5);p.paragraph_format.space_after=Pt(12)
    para(doc,'지역의 고유성을 생산력으로 바꾸는\nAI 하방 정책','Title')
    p=para(doc,'풍기와 예산을 잇는 지능 에이전트 고속도로 실증 제안',size=10.5);p.paragraph_format.space_after=Pt(8)
    p=para(doc,'이수화  서울대학교 빅데이터혁신융합대학 연구교수 · 법무법인 디엘지 AI센터장',size=8.5);p.paragraph_format.space_after=Pt(9)
    for kind,text in P1:para(doc,text,'Heading 1' if kind=='heading' else 'Normal')
    table=doc.add_table(rows=1,cols=3);table.autofit=False
    for c,w in zip(table.columns,[17,65,88]):c.width=Mm(w)
    for c,t in zip(table.rows[0].cells,['영역','지역에서 만들 경험과 사업','AI가 맡을 구체적 일']):c.text=t
    for row in ROWS:
        for c,t in zip(table.add_row().cells,row):c.text=t
    table_borders(table)
    for i,row in enumerate(table.rows):
        for j,cell in enumerate(row.cells):
            cell.width=Mm([17,65,88][j])
            cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'E8EDF0' if i==0 else ('F7F8F8' if i%2==0 else 'FFFFFF'));cell._tc.get_or_add_tcPr().append(shade)
            for p in cell.paragraphs:
                p.paragraph_format.space_after=Pt(0);p.paragraph_format.line_spacing=Pt(13)
                if j==0:p.alignment=WD_ALIGN_PARAGRAPH.CENTER
                for r in p.runs:r.font.size=Pt(8.8);r.bold=i==0
    p=para(doc,'주류·부산물 사업은 적격 사업자와 가공 적합성·운영 조건을 검토한 뒤 추진한다.',size=8)
    p.paragraph_format.space_before=Pt(5);p.paragraph_format.space_after=Pt(0)
    doc.add_page_break()
    p=doc.add_paragraph();p.paragraph_format.space_after=Pt(2);p.paragraph_format.line_spacing=1.0;p.add_run().add_picture(str(OUT/'atlas-and-qr.png'),width=Mm(170))
    for kind,text in P2:para(doc,text,'Heading 1' if kind=='heading' else 'Normal')
    p=para(doc,'자료  영주시 문화관광 영주사과 · 예산군 문화관광 예산사과의 역사 · 농촌진흥청 사과 고온 장해 자료\n지도  Mapzen Terrain Tiles / USGS SRTM · 예시 데이터와 방법, 원문 출처는 QR 앱의 자료와 방법에 공개',size=7.8)
    p.paragraph_format.space_before=Pt(7);p.paragraph_format.line_spacing=Pt(11);p.paragraph_format.space_after=Pt(0)
    out=OUT/'2026_지방시대엑스포_토론문_이수화_개정본.docx';doc.save(out)
    (OUT/'발제문_개정원고.txt').write_text('\n\n'.join(t for _,t in P1)+'\n\n'+'\n'.join(' | '.join(r) for r in ROWS)+'\n\n'+'\n\n'.join(t for _,t in P2),encoding='utf8')
    print(out)
if __name__=='__main__':build()
