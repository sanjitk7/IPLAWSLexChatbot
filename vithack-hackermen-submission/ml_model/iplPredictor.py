

def predictor(team1,team2):
  import numpy as np
  import pandas as pd
  import joblib
  matches=pd.read_csv('s3://new-dataset-vithack/VITHACK_Data.csv')
  matches[pd.isnull(matches['winner'])]
  matches['winner'].fillna('Draw', inplace=True)
  matches[pd.isnull(matches['city'])]
  matches['city'].fillna('Dubai',inplace=True)
  matches.replace(['Mumbai Indians','Kolkata Knight Riders','Royal Challengers Bangalore','Deccan Chargers','Chennai Super Kings',
                 'Rajasthan Royals','Delhi Daredevils','Gujarat Lions','Kings XI Punjab',
                 'Sunrisers Hyderabad','Rising Pune Supergiants','Rising Pune Supergiant','Kochi Tuskers Kerala','Pune Warriors','Delhi Capitals']
                ,['MI','KKR','RCB','DC','CSK','RR','DD','GL','KXIP','SRH','RPS','RPS','KTK','PW','DCP'],inplace=True)

  encode = {'team1': {'MI':1,'KKR':2,'RCB':3,'DC':4,'CSK':5,'RR':6,'DD':7,'GL':8,'KXIP':9,'SRH':10,'RPS':11,'KTK':12,'PW':13,'DCP':14},
          'team2': {'MI':1,'KKR':2,'RCB':3,'DC':4,'CSK':5,'RR':6,'DD':7,'GL':8,'KXIP':9,'SRH':10,'RPS':11,'KTK':12,'PW':13,'DCP':14},
          'toss_winner': {'MI':1,'KKR':2,'RCB':3,'DC':4,'CSK':5,'RR':6,'DD':7,'GL':8,'KXIP':9,'SRH':10,'RPS':11,'KTK':12,'PW':13,'DCP':14},
          'winner': {'MI':1,'KKR':2,'RCB':3,'DC':4,'CSK':5,'RR':6,'DD':7,'GL':8,'KXIP':9,'SRH':10,'RPS':11,'KTK':12,'PW':13,'DCP':14,'Draw':15}}
  matches.replace(encode, inplace=True)
  dicVal = encode['winner']
  filename= 's3://new-dataset-vithack/newModel.sav'
  model = joblib.load(filename)
  teamA= team1
  teamB = team2
  #if teamA wins
  toss_winner=teamA
  input=[dicVal[team1],dicVal[team2],'14',dicVal[toss_winner],'2','1']
  input = np.array(input).reshape((1, -1))
  output=model.predict(input)
  pred1=list(dicVal.keys())[list(dicVal.values()).index(output)]
  #print("if" ,teamA,"wins the toss, then" ,pred1,"wins the match") 

  #if teamB wins
  toss_winner=teamB
  input=[dicVal[team1],dicVal[team2],'14',dicVal[toss_winner],'2','1']
  input = np.array(input).reshape((1, -1))
  output=model.predict(input)
  pred2= list(dicVal.keys())[list(dicVal.values()).index(output)]
  print("if" +str(teamA)+"wins the toss, then" +str(pred1)+"wins the match"+"\n"+"if" +str(teamB)+"wins the toss, then" +str(pred2)+"wins the match")
  return("if" +str(teamA)+"wins the toss, then" +str(pred1)+"wins the match"+"\n"+"if" +str(teamB)+"wins the toss, then" +str(pred2)+"wins the match")

