"""Builds index.html and data/story.json from the story table and the scene kit."""
import json, re, os, pandas as pd
import scenes as S, chars, chars2
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from chars2 import maria, role, daughter, nurse
SRC = os.path.join(ROOT, 'data', 'maria_story.csv')
df = pd.read_csv(SRC)
tk = lambda t: re.sub(r'৳\s?', 'Tk ', str(t))
TITLES = ["The English copy","The testimonial","The first ID card","The first passport","The driving licence","Giving birth","The teacher's arrears",
          "The trade licence","The shop meter","Land mutation","The mortgage registration","The police case","The family pension","Maria dies","The death certificate","The heirs' certificate"]
DEV = {1:"First she is told it can't be done now. Then an employee quietly suggests she \"give something\" and come back tomorrow.",
 2:"A clerk wanted Tk 500 for 3 or 4 sheets of paper. The principal said, almost openly, that the school runs on the money students give.",
 4:"Refused three times for small reasons, until a dalal says Tk 1,500 will fix it. Dalals have their own code that they type where the applicant's email should go. At another office, a counter writes a number on a slip and sends people to a shop outside.",
 5:"A man points her to a \"sir\": Tk 500 or she fails. The officer warns about the CCTV and takes it under an envelope. In another report, an officer explains that a 100% pass rate can't be shown to the bosses, so the people who pay are logged as passed.",
 6:"A tip at every handover: Tk 200 leaving the operating theatre, Tk 200 on the ward for \"cleaning\", then Tk 100 each time after.",
 10:"A sweeper with a shop outside the land office steers people to his shop. He is not an official, but the office runs through him.",
 11:"In another land registration, the broker agrees Tk 2.4 lakh. Hours later: \"the government rate went up, Tk 20,000 more\", then \"the registrar needs Tk 20,000\". She borrows from the seller to finish.",
 12:"In another police report, a patrol stops the car and one officer goes shop to shop saying \"the vehicle is waiting, go pay\". The shopkeepers walk over and hand it in. One person is assigned to collect.",
 15:"At the councillor's office: Tk 3,000 per form, \"or it won't be done\". Two forms, Tk 6,000 in cash.",
 16:"In another inheritance report, Tk 50,000 is asked for the heir's mutation of a dead father's plot. Tk 15,000 is paid, and a month later nothing has happened."}
AGENOTE = {1:"her mother acts",14:"",15:"her family acts",16:"her children act"}
C = S.counter
SVGS = [
 C('MUNICIPALITY','BIRTH REGISTRATION',['window','almirah','calendar'],'clerk',
   [('o','English copy? Not possible now.'),('o','Tk 2,000. Collect it tomorrow.'),('m','Tk 1,000. That is all I have.'),('o','Hm. Come tomorrow.')],'Tk 1,000',chars.mother(),'files','', 'F','o','1000'),
 C('SCHOOL OFFICE','TESTIMONIALS',['window','calendar','board'],'clerk',
   [('o','Testimonial? Tk 4,000.'),('m','It is only three sheets!'),('t','The school runs on this money.'),('m','Tk 725, sir. Please.')],'Tk 725',maria(16,bag=True),'files','principal','B','o','725'),
 C('ELECTION COMMISSION','NATIONAL ID SERVICE',['window','flag','calendar'],'officer',
   [('t',"This won't happen. Talk to sir."),('o','(Says no number. Just waits.)'),('m','Tk 2,750. First in the serial?'),('o','Card in 72 hours.')],'Tk 2,750',maria(18),'computer','peon','F','o','2750'),
 S.gate([('o','Fault in the form. Come again.'),('t','Tk 2,011. No more faults.'),('m','Tk 2,500 in all. Please.'),('t','Done. The file is clean now.')],'Tk 2,500','2500'),
 S.ground([('m','I passed every step.'),('t','Result says fail. Tk 4,750.'),('m','Tk 3,500. That is my limit.'),('o','Next date: pass.')],'Tk 3,500','3500'),
 S.ward('birth',[('o','Tk 1,000 for the delivery.'),('m','We have nothing to give.'),('o','No payment, no help.'),('m','Tk 500, please. Only that.')],'Tk 500','500',role('husband'),[nurse()]),
 C('EDUCATION OFFICE','ACCOUNTS SECTION',['window','almirah','calendar'],'assistant',
   [('o','Not ready. Come tomorrow.'),('o','Tk 5,000 and it moves.'),('m','Tk 4,500. Please move it.'),('o','All right. It moves today.')],'Tk 4,500',maria(32,folder=True),'tall','','F','o','4500'),
 C('CITY CORPORATION','TRADE LICENCE',['window','board','calendar'],'clerk',
   [('o','New paper needed. Come again.'),('t','Tk 12,000. Nothing else needed.'),('m','Tk 3,000 now, then the fee.'),('t','Licence tomorrow.')],'Tk 3,000',maria(40,folder=True),'files','peon','F','F','3000'),
 S.shop([('t','Cancelled. Too far from the pole.'),('o','Tk 4,250 and I fix it.'),('m','Tk 5,500 in all. Do it.'),('o','Meter is on at the same spot.')],'Tk 5,500','5500'),
 S.landoffice([('o','Six months. Tk 12,000 to move it.'),('m','I can give Tk 10,000.'),('o','I will see every desk for you.'),('o','Hearing is fixed. Come Monday.')],'Tk 10,000','10000'),
 C('SUB-REGISTRY','DEED REGISTRATION',['window','almirah','flag'],'registrar',
   [('o','Fingerprint step. Tk 12,000.'),('o','Or the registration is cancelled.'),('m','Tk 2,000. That is all I have.'),('o','Fine. Thumb here, please.')],'Tk 2,000',maria(52,folder=True),'typewriter','scribe','B','o','2000'),
 C('POLICE STATION','GENERAL DIARY',['window','flag','board'],'police',
   [('o','Land-grab? Come again tomorrow.'),('o','These cases cost. Tk 20,000.'),('m','Tk 3,000 is what I have.'),('o','We will see. Come again.')],'Tk 3,000',maria(55,folder=True),'files','','F','o','3000'),
 C('EDUCATION OFFICE','PENSION ACCOUNTS',['window','almirah','calendar'],'clerk',
   [('o','Family pension? Tk 62,500.'),('t','In two parts. Half now.'),('m','Tk 20,000. Please start it.'),('o','Come next week for the rest.')],'Tk 20,000',maria(66),'tall','peon','F','o','20000'),
 S.ward('dead',[('o','The body cannot go without payment.'),('m','Please. We are in mourning.'),('t','Tk 700 for the trolley and ward.'),('m','Here. Let us take her home.')],'Tk 700','700',role('son'),[role('aide'),role('aide')]),
 C('COUNCILLOR OFFICE','BIRTH & DEATH REGISTRATION',['window','flag','calendar'],'clerk',
   [('o','Death certificate? Tk 2,000.'),('m','Is there no other way?'),('o','No other way.'),('m','Tk 3,000 in cash. Here.')],'Tk 3,000',role('son'),'files','','F','o','3000'),
 C('UPAZILA OFFICE','HEIRS CERTIFICATE',['window','almirah','flag'],'officer',
   [('t','I visited your house. Tk 2,000.'),('m','Paid at home. And here too?'),('o','Tk 1,000 at the office.'),('o','Your heirs certificate is ready.')],'Tk 3,000 in all',daughter(),'tall','assistant','B','o','1000'),
]
assert len(SVGS)==16
scenes=[]
for _,r in df.iterrows():
    st=int(r.step); age=int(str(r.maria_age).split()[0])
    a=None if pd.isna(r.asked_median_bdt) else int(r.asked_median_bdt)
    p=None if pd.isna(r.paid_median_bdt) else int(r.paid_median_bdt)
    if isinstance(r.n_paid_over_n_asked,str) and '/' in r.n_paid_over_n_asked:
        np_,na=r.n_paid_over_n_asked.split('/'); n=f'Medians from {np_} paid and {na} asked reports.'
    else: n='One report only, so there is no median.'
    if p is None and not pd.isna(r.amount_in_source_report_bdt): p=int(r.amount_in_source_report_bdt)
    scenes.append(dict(step=st,age=age,ageNote=AGENOTE.get(st,''),stage=r.life_stage,title=TITLES[st-1],story=tk(r.story),asked=a,paid=p,n=n,
        device=DEV.get(st,''),src=re.sub(r'\s*\(\+\s*','; ',str(r.source_report_ids)).replace(')','').replace(';',',')))
json.dump(scenes,open(os.path.join(ROOT,'data','story.json'),'w'),indent=1,ensure_ascii=False)
html=open(os.path.join(ROOT,'site','template.html')).read().replace('__SCENES__',json.dumps(scenes)).replace('__SVGS__',json.dumps(SVGS))
open(os.path.join(ROOT,'index.html'),'w').write(html)
print('built',len(html)//1024,'KB')
