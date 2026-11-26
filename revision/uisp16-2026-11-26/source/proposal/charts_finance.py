from pathlib import Path
import json
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

w=Path(__file__).resolve().parent
risk=w.parent/'finance'/'results'/'risk-base-seed12026.json'
inp=Path(sys.argv[1]) if len(sys.argv)>1 else w/'model_metrics_raw.json'
with plt.rc_context({'font.family':'DejaVu Sans','text.color':'#234234','font.size':9,'axes.facecolor':'#edf4ee','figure.facecolor':'#edf4ee','axes.edgecolor':'#b7cbbd','axes.labelcolor':'#234234','xtick.color':'#234234','ytick.color':'#234234'}):
    if risk.is_file():
        d=json.loads(risk.read_text())['simulation']
        x=[r['npv'] for r in d['rows']]
        fig,ax=plt.subplots(figsize=(6.2,2.02))
        fig.subplots_adjust(left=.12,right=.95,bottom=.27,top=.94)
        ax.hist(x,bins=24,color='#326950',edgecolor='#EDF4EE',linewidth=.55)
        ax.axvline(d['summary']['npv']['p50'],color='#85663c',linewidth=2,label='Median hasil')
        ax.set_xlabel('NPV proyek (Rp juta)');ax.set_ylabel('Percobaan')
        ax.legend(loc='upper right',frameon=False)
        ax.xaxis.set_major_formatter(FuncFormatter(lambda z,_: f'{z:,.0f}'.replace(',','.')))
        fig.savefig(w/'npv_histogram.png',dpi=300,facecolor=fig.get_facecolor());plt.close(fig)
    if inp.is_file():
        raw=json.loads(inp.read_text())
        for field,fn,ylab in [('orders','orders.png','Pesanan selesai'),('fcff','cash.png','FCFF · Rp juta nominal')]:
            if not all(isinstance(raw.get(k),dict) and field in raw[k] for k in ['base','downside','upside']):continue
            fig,ax=plt.subplots(figsize=(6.2,1.83))
            fig.subplots_adjust(left=.13,right=.95,bottom=.24,top=.86)
            for k,lab,c in [('downside','Konservatif','#95735A'),('base','Dasar','#185544'),('upside','Optimistis','#689988')]:
                vals=raw[k][field]
                if field=='fcff': vals=[v for v in vals]
                years=list(range(2037-len(vals),2037))
                ax.plot(years,vals,color=c,linewidth=1.8,label=lab,marker='o',markersize=2.5)
            ax.axhline(0,linewidth=.55,color='#999999')
            ax.set_ylabel(ylab);ax.set_xticks([2027,2029,2031,2033,2036])
            ax.legend(loc='lower left' if field=='fcff' else 'upper left',frameon=False,ncol=3,bbox_to_anchor=(0.0,1.0),borderaxespad=0)
            ax.grid(axis='y',color='#d6e3d8',linewidth=.6)
            for wall in ['right','top']:ax.spines[wall].set_visible(False)
            fig.savefig(w/fn,dpi=300,facecolor=fig.get_facecolor());plt.close(fig)
