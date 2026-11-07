import argparse,json
from pathlib import Path
import joblib,numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix,f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from features import collect,image_features

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--images',required=True,help='folder dataset-resized containing six label subfolders');ap.add_argument('--out',default='outputs/AI02');a=ap.parse_args()
 out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
 paths,y=collect(a.images)
 print('Dang trich xuat dac trung HOG cho',len(paths),'anh...')
 x=np.vstack([image_features(p) for p in paths]);ix=np.arange(len(y))
 i,j=train_test_split(ix,test_size=.2,stratify=y,random_state=2026)
 model=make_pipeline(StandardScaler(),LogisticRegression(max_iter=1200,class_weight='balanced'))
 model.fit(x[i],y[i]); pred=model.predict(x[j])
 m={'accuracy':float(accuracy_score(y[j],pred)),'macro_f1':float(f1_score(y[j],pred,average='macro')),
    'classification_report':classification_report(y[j],pred,output_dict=True,zero_division=0),
    'labels':list(model.classes_),'confusion_matrix':confusion_matrix(y[j],pred,labels=model.classes_).tolist(),
    'method':'HOG(gray 64x64) + RGB histogram + LogisticRegression','split':'stratified dev 80/20 seed 2026'}
 joblib.dump(model,out/'model.joblib');(out/'metrics.json').write_text(json.dumps(m,indent=2,ensure_ascii=False),encoding='utf-8')
 (out/'demo_image_path.txt').write_text(str(paths[j[0]].resolve()),encoding='utf-8')
 print('AI02 OK',round(m['macro_f1'],3),'image:',paths[j[0]])
if __name__=='__main__':main()
