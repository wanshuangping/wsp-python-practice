from pypdf import PdfReader
r = PdfReader("/Users/temu/WorkBuddy/2026-08-31-18-47-03/szu2026/szu_grad_report_2025.pdf")
out=[]
for i,p in enumerate(r.pages):
    t = p.extract_text() or ""
    out.append(f"\n===== PAGE {i+1} =====\n"+t)
text="\n".join(out)
open("/Users/temu/WorkBuddy/2026-08-31-18-47-03/szu2026/report_text.txt","w").write(text)
print("pages", len(r.pages), "chars", len(text))
