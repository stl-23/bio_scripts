import sys
from argparse import ArgumentParser
from sklearn.model_selection import train_test_split,cross_val_score,GridSearchCV
from sklearn.linear_model import LogisticRegression,LogisticRegressionCV
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import label_binarize
from sklearn import metrics
from itertools import cycle
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# https://blog.csdn.net/weixin_46649052/article/details/107728077
def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--train",action="store",dest="train",help="", default="")
    parser.add_argument("--test",action="store",dest="test",help="", default="")
    #parser.add_argument("--outfile",action="store",dest="outfile",help="",default='')
    args = parser.parse_args()
    return args

def get_df(train_file,test_file):
    traindf = pd.read_csv(train_file,sep='\t',header=0)
    testdf = pd.read_csv(test_file,sep='\t',header=0)
    X_train = traindf.iloc[:,1:]
    Y_train = traindf.iloc[:,0]
    x_test = testdf.iloc[:,1:]
    y_test = testdf.iloc[:,0]
    return X_train,Y_train,x_test,y_test

def model_build(X_train,Y_train,x_test,y_test):
    alpha = np.logspace(-2,2,20)
    models = [
        #['KNN',GridSearchCV(KNeighborsClassifier(),param_grid={'n_neighbors':[i for i in range(1,11,2)]})],
        ['KNN',KNeighborsClassifier(n_neighbors=3)],
        ['LogisticRegression',LogisticRegressionCV(Cs=alpha,penalty='l2',cv=3)],
        ['SVM(Linear)',GridSearchCV(SVC(kernel='linear',decision_function_shape='ovr'),param_grid={'C':alpha})],
        ['SVM(RBF)',GridSearchCV(SVC(kernel='rbf',decision_function_shape='ovr'),param_grid={'C':alpha,'gamma':alpha})]]
    colors = cycle('gmcr')
    mpl.rcParams['font.sans-serif'] = u'SimHei'
    mpl.rcParams['axes.unicode_minus'] = False
    for (name,model),color in zip(models,colors):
        model.fit(X_train,Y_train)
        print(name+":")
        if hasattr(model,'C_'):
            print("model.C_:{}".format(model.C_))
        if hasattr(model,'best_params_'):
            print("best_params:{}".format(model.best_params_))
        if hasattr(model,'predict_proba'):
            y_score = model.predict_proba(x_test)
        else:
            y_score = model.decision_function(x_test)
        if len(y_score.shape) >1:
            fpr, tpr, thresholds = metrics.roc_curve(y_test, y_score[:,1])
        else:
            fpr, tpr, thresholds = metrics.roc_curve(y_test, y_score)
        auc = metrics.auc(fpr, tpr)

        y_pred = model.predict(x_test)
        cm = metrics.confusion_matrix(y_test, y_pred)
        TP = cm[1,1]
        TN = cm[0,0]
        FP = cm[0,1]
        FN = cm[1,0]
        accuracy = (TP + TN)/float(TP+TN+FP+FN)
        sensitivity = TP/float(TP+FN)
        specificity = TN/float(TN+FP)
        print("AUC: {}\nAccuracy: {}\nSensitivity: {}\nSpecificity: {}\n".format(auc,accuracy,sensitivity,specificity))

        plt.plot(fpr, tpr, c=color, lw=2, alpha=0.7, label=u'%s, AUC=%.3f' % (name, auc))
    plt.plot((0, 1), (0, 1), c='#808080', lw=2, ls='--', alpha=0.7)
    plt.xlim((-0.01, 1.02))
    plt.ylim((-0.01, 1.02))
    plt.xticks(np.arange(0, 1.1, 0.1))
    plt.yticks(np.arange(0, 1.1, 0.1))
    plt.xlabel('False Positive Rate', fontsize=13)
    plt.ylabel('True Positive Rate', fontsize=13)
    plt.grid(b=True, ls=':')
    plt.legend(loc='lower right', fancybox=True, framealpha=0.8, fontsize=12)
    # plt.legend(loc='lower right', fancybox=True, framealpha=0.8, edgecolor='#303030', fontsize=12)
    plt.title(u'swgs_ROC_AUC', fontsize=17)
    #plt.show()
    plt.savefig('swgs_test_set_ROC_AUC.jpg')
    plt.close()
    #classifier = LogisticRegression()
    #clf = classifier.fit(X_train,Y_train)
   # result = cross_val_score(classifier, feature, label, cv=10)
    #y_pred = clf.predict(x_test)
    #prepro1 = clf.predict_proba(X_train)
    #prepro2 = clf.predict_proba(x_test)
    #acc1 = clf.score(X_train,Y_train)
    #acc2 = clf.score(x_test,y_test)
    #print(clf)
    #print(acc1,acc2)
if __name__ == "__main__":
    args = parse_args()
    X_train,Y_train,x_test,y_test = get_df(args.train,args.test)
    model_build(X_train,Y_train,x_test,y_test)
