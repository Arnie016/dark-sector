"""C-04 reference reconstruction from manually transcribed Silverman et al.
arXiv:2606.02566v1, Table 1. Does not run GIZMO or fit events.
The expanded locally executed audit is tracked by SHA256 in README.
"""
from pathlib import Path
import json
# name, predicted absolute cosmic age [Gyr], run end [Gyr], reached criterion
rows=[("m10q",7.33,10.4,True),("m10d",5.37,9.5,True),
      ("m10i",2.28,5.2,True),("m10b",10.12,9.0,False),
      ("m10f",7.18,6.4,False),("m10j",2.28,4.9,False)]
assert len(set(x[0] for x in rows))==6
margins={n:round(c-p,2) for n,p,c,_ in rows}
assert (margins["m10b"],margins["m10f"],margins["m10j"])==(-1.12,-.78,2.62)
h=13.8
events=sum(event for _,_,_,event in rows)
unknown=sum((not event) and c<h for _,_,c,event in rows)
result={"source":"arXiv:2606.02566v1 Tables 1-3","as_of":"2026-10-18",
        "data_kind":"PUBLISHED SIMULATION TABLE SUMMARY",
        "status":["DERIVED","UNIDENTIFIABLE","DATA_INSUFFICIENT"],
        "at_last_snapshot_events":events,"censored_non_events":unknown,
        "non_events_stopping_before_predicted":sum(not ev and c<p for _,p,c,ev in rows),
        "non_events_surviving_beyond_predicted":sum(not ev and c>=p for _,p,c,ev in rows),
        "margins_Gyr":margins,"target_Gyr":h,
        "sharp_selected_six_count_bounds":[events,events+unknown],
        "not_claimed":"N-body reproduction, population inference, likelihood fit"}
assert result["sharp_selected_six_count_bounds"]==[3,6]
Path("RESULT.json").write_text(json.dumps(result,indent=2)+"\\n")
print(json.dumps(result,indent=2))
