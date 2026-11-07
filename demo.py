import argparse,joblib
from features import image_features
ap=argparse.ArgumentParser();ap.add_argument('--model',default='outputs/AI02/model.joblib');ap.add_argument('--image',required=True);a=ap.parse_args()
model=joblib.load(a.model); x=image_features(a.image).reshape(1,-1)
print('Loai rac:',model.predict(x)[0]);print('Do tin cay tham khao:',dict(zip(model.classes_,model.predict_proba(x)[0].round(3))))
