"""Render original synthetic verification figures from the tested public scripts."""
import pathlib,runpy,numpy as np
root=pathlib.Path(__file__).resolve().parent
fdd=runpy.run_path(str(root/"nine_channel_fdd_demo.py"))
lqr=runpy.run_path(str(root/"lqr_vibration_robustness_demo.py"))

def header(title,subtitle):
 return [f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="455" viewBox="0 0 1000 455" role="img" aria-label="{title}">',
 '<rect width="1000" height="455" fill="#0f172a"/>',
 f'<text x="70" y="55" font-size="27" fill="#f8fafc" font-family="Arial, sans-serif" font-weight="bold">{title}</text>',
 f'<text x="70" y="82" font-size="14" fill="#94a3b8" font-family="Arial, sans-serif">{subtitle}</text>']
def grid(ticks,xmin,xmax,ymin,ymax,ylabels):
 out=[]
 def xs(v):return 85+850*(v-xmin)/(xmax-xmin)
 def ys(v):return 362-240*(v-ymin)/(ymax-ymin)
 for x in ticks:
  xx=xs(x);out +=[f'<line x1="{xx:.1f}" y1="122" x2="{xx:.1f}" y2="362" stroke="#334155" stroke-width="1" />',
  f'<text x="{xx:.1f}" y="389" fill="#94a3b8" text-anchor="middle" font-size="13" font-family="Arial">{x:g}</text>']
 for y,t in ylabels:
  yy=ys(y);out +=[f'<line x1="85" y1="{yy:.1f}" x2="935" y2="{yy:.1f}" stroke="#334155" stroke-width="1" />',
  f'<text x="72" y="{yy+4:.1f}" fill="#94a3b8" text-anchor="end" font-size="12" font-family="Arial">{t}</text>']
 return out,xs,ys
def poly(x,y,xs,ys,color,step=1):
 points=" ".join(f'{xs(xx):.2f},{ys(yy):.2f}' for xx,yy in zip(x[::step],y[::step]))
 return f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/>'
def save(name,out):
 out.append('<text x="85" y="432" fill="#64748b" font-size="12" font-family="Arial">ORIGINAL SYNTHETIC VERIFICATION — not field measurements or client results</text>')
 out.append('</svg>')
 p=root/name;p.write_text("\n".join(out),encoding="utf-8")
 print(name,p.stat().st_size)
# FDD first singular-value spectrum
freq=np.asarray(fdd["freqs"])
sv=np.asarray(fdd["svals"])[:,0]
db=10*np.log10(np.maximum(sv,1e-16)/sv[(freq>=2)&(freq<=25)].max())
sel=(freq>=0)&(freq<=25)
x=freq[sel];y=np.clip(db[sel],-65,0)
out=header("Operational Modal Analysis | 9-channel FDD","First singular-value spectrum (dB) - simulated sensors, Welch CSD 9 x 9")
gr,xs,ys=grid([0,5,10,15,20,25],0,25,-65,0,[(-60,"-60"),(-40,"-40"),(-20,"-20"),(0,"0")])
out.extend(gr);out.append(poly(x,y,xs,ys,"#38bdf8",step=4))
for peak in fdd["f_identified"]:
 xx=xs(float(peak));out.extend([f'<line x1="{xx:.1f}" y1="122" x2="{xx:.1f}" y2="362" stroke="#fbbf24" stroke-width="1.6" stroke-dasharray="5,5"/>',f'<text x="{xx+3:.1f}" y="112" font-size="13" fill="#fbbf24" font-family="Arial">{float(peak):.2f} Hz</text>'])
out+=['<text x="510" y="412" fill="#cbd5e1" text-anchor="middle" font-size="14" font-family="Arial">Frequency (Hz)</text>','<text x="950" y="155" fill="#38bdf8" font-size="14" font-family="Arial">FDD SV1</text>']
save("fdd_9channel_spectrum.svg",out)
# LQR pulse response: baseline and controlled, time axis
times=np.asarray(lqr["t_eval"])
base=np.asarray(lqr["p"])[0,:]*1000
controlled=np.asarray(lqr["c"])[0,:]*1000
sel=times<=4.0
out=header("Vibration Control | LQR vs Uncontrolled","Linear mass-spring-damper, 100 N pulse for 0.25 s, synthetic state-feedback benchmark")
gr,xs,ys=grid([0,1,2,3,4],0,4,-550,550,[(-500,"-500"),(-250,"-250"),(0,"0"),(250,"250"),(500,"500")])
out.extend(gr);out.append(poly(times[sel],base[sel],xs,ys,"#fb923c",step=4));out.append(poly(times[sel],controlled[sel],xs,ys,"#2dd4bf",step=4))
out.extend(['<text x="510" y="412" fill="#cbd5e1" text-anchor="middle" font-size="14" font-family="Arial">Time (s)</text>',
'<text x="690" y="106" fill="#fb923c" font-size="13" font-family="Arial">Uncontrolled</text>',
'<text x="820" y="106" fill="#2dd4bf" font-size="13" font-family="Arial">LQR controlled</text>'])
save("lqr_pulse_response.svg",out)
