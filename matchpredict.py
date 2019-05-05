import numpy as np
import pandas as pd
import models
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold, train_test_split, RepeatedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn import metrics

encode = {'team1': {'MI':1,'KKR':2,'RCB':3,'DC':4,'CSK':5,'RR':6,'KXIP':7,'SRH':8},
  'team2': {'MI':1,'KKR':2,'RCB':3,'DC':4,'CSK':5,'RR':6,'KXIP':7,'SRH':8},
  'toss_winner': {'MI':1,'KKR':2,'RCB':3,'DC':4,'CSK':5,'RR':6,'KXIP':7, 'SRH':8},
  'winner': {'MI':1,'KKR':2,'RCB':3,'DC':4,'CSK':5,'RR':6,'KXIP':7,'SRH':8},
  'daynight':{'Y':1, 'N':0}, 'mom_to_wining_team':{'Y':1, 'N':0}, 'winner_home_team':{'Y':1, 'N':0}}
dicVal = encode['winner']
class matchPrediction:
    def _getMatchData(self):
        mymodel = models.DbHandler()
        mdata = mymodel._getMatchSummary('match')
        DataSet = pd.DataFrame(mdata)
        DataSet.replace(encode, inplace=True)
        #print(self.DataSet.describe())
        DataSet = DataSet[['team1','team2','loc', 'daynight', 'winner_home_team', 'toss_decission','toss_winner','winner']]
        """
        print(dicVal['CSK'])
        print(list(dicVal.keys())[list(dicVal.values()).index(5)]) #find key by value search
        temp1=DataSet['toss_winner'].value_counts(sort=True)
        temp2=DataSet['winner'].value_counts(sort=True)
        print('No of toss winners by each team')
        for idx, val in temp1.iteritems():
           print('{} -> {}'.format(list(dicVal.keys())[list(dicVal.values()).index(idx)],val))
        print('No of match winners by each team')
        for idx, val in temp2.iteritems():
           print('{} -> {}'.format(list(dicVal.keys())[list(dicVal.values()).index(idx)],val))
         """
        var_mod = ['loc','toss_decission']
        le = LabelEncoder()
        for i in var_mod:
            DataSet[i] = le.fit_transform(DataSet[i])
        #print(self.DataSet.dtypes)
        return DataSet

    def classification_model(self, model, data, predictors, outcome):
        model.fit(data[predictors],data[outcome])
        predictions = model.predict(data[predictors])
        accuracy = metrics.accuracy_score(predictions,data[outcome])
        kf = KFold(n_splits=7, random_state=1, shuffle=True)
        error = []
        for train, test in kf.split(data):
            train_predictors = (data[predictors].iloc[train,:])
            train_target = data[outcome].iloc[train]
            model.fit(train_predictors, train_target)
            error.append(model.score(data[predictors].iloc[test,:], data[outcome].iloc[test]))

        print('Cross-Validation Score : %s' % '{0:.3%}'.format(np.mean(error)))
        model.fit(data[predictors],data[outcome])

if __name__ == '__main__':
    mp = matchPrediction()
    df = mp._getMatchData()
    outcome_var=['winner']
    predictor_var = ['team1','team2','toss_winner', 'toss_decission']
    model = LogisticRegression(solver='lbfgs', multi_class='auto')
    mp.classification_model(model, df,predictor_var,outcome_var)

    team1='RCB'
    team2='KXIP'
    toss_winner='KXIP'
    input=[dicVal[team1],dicVal[team2],dicVal[toss_winner],1]
    input = np.array(input).reshape((1, -1))
    output=model.predict(input)
    print(list(dicVal.keys())[list(dicVal.values()).index(output)]) #find key by value search output

    team1='CSK'
    team2='SRH'
    toss_winner='CSK'
    input=[dicVal[team1],dicVal[team2],dicVal[toss_winner],1]
    input = np.array(input).reshape((1, -1))
    output=model.predict(input)
    print(list(dicVal.keys())[list(dicVal.values()).index(output)]) #find key by value search output

    team1='RR'
    team2='DC'
    toss_winner='DC'
    input=[dicVal[team1],dicVal[team2],dicVal[toss_winner],1]
    input = np.array(input).reshape((1, -1))
    output=model.predict(input)
    print(list(dicVal.keys())[list(dicVal.values()).index(output)]) #find key by value search output

    model = RandomForestClassifier(n_estimators=100)
    predictor_var = ['team1', 'team2', 'loc', 'daynight', 'toss_winner','toss_decission']
    mp.classification_model(model, df,predictor_var,outcome_var)

    input=[dicVal[team1],dicVal[team2],0,0, dicVal[toss_winner],1]
    input = np.array(input).reshape((1, -1))
    output=model.predict(input)
    print(list(dicVal.keys())[list(dicVal.values()).index(output)]) #find key by value search output

    input=[dicVal[team1],dicVal[team2],2, 0, dicVal[toss_winner],1]
    input = np.array(input).reshape((1, -1))
    output=model.predict(input)
    print(list(dicVal.keys())[list(dicVal.values()).index(output)]) #find key by value search output

    input=[dicVal[team1],dicVal[team2],5, 0, dicVal[toss_winner],1]
    input = np.array(input).reshape((1, -1))
    output=model.predict(input)
    print(list(dicVal.keys())[list(dicVal.values()).index(output)]) #find key by value search output
