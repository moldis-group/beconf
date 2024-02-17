import os
import numpy as np
import pandas as pd
import qml
from qml.representations import generate_atomic_coulomb_matrix
from setuptools import find_packages, setup
from pkg_resources import resource_filename
from datetime import datetime
import cebeconf

start_time = datetime.now()
formatted_datetime = start_time.strftime("%Y-%m-%d %H:%M:%S")

data_folder = resource_filename('cebeconf', 'data')

# Main
def calc_be(XYZfile,KRR_model,rep,**args_MaxN):

    # Read XYZfile
    mol_R=[]
    mol_Z=[]

    iline=0
    at_types=[]

    with open(XYZfile,'r') as f:

        for line in f:

            line=line.split()

            if iline == 0:
                N_at=int(line[0])

            if iline == 1:
                Mol_title=line[0]

            if iline > 1:
                at_R=[float(line[1]),float(line[2]),float(line[3])]
                at_R=np.array(at_R)
                mol_R.append(at_R)

                ele=line[0]
                at_types.append(ele)
                at_Z=cebeconf.atno(ele)
                mol_Z.append(at_Z)

            iline=iline+1

    # Load data
    time1 = datetime.now()

    if rep.lower() == 'acm':

        X_train_C=np.load(os.path.join(data_folder, 'C_representation_ACM.npy'))
        X_train_N=np.load(os.path.join(data_folder, 'N_representation_ACM.npy'))
        X_train_O=np.load(os.path.join(data_folder, 'O_representation_ACM.npy'))
        X_train_F=np.load(os.path.join(data_folder, 'F_representation_ACM.npy'))
    
        if KRR_model.lower() == 'direct':
    
            df = pd.read_csv(os.path.join(data_folder, 'C_model_direct_ACM.csv'), header=None)
            model_C=np.array(df.iloc[:,0].values)
            df = pd.read_csv(os.path.join(data_folder, 'N_model_direct_ACM.csv'), header=None)
            model_N=np.array(df.iloc[:,0].values)
            df = pd.read_csv(os.path.join(data_folder, 'O_model_direct_ACM.csv'), header=None)
            model_O=np.array(df.iloc[:,0].values)
            df = pd.read_csv(os.path.join(data_folder, 'F_model_direct_ACM.csv'), header=None)
            model_F=np.array(df.iloc[:,0].values)
    
            #using median kij
            sigma_C=1231.742 # 0.75
            sigma_N=2092.483 # 0.84
            sigma_O=3669.079 # 0.90
            sigma_F=10779.688 # 0.96
    
        if KRR_model.lower() == 'delta':
    
            df = pd.read_csv(os.path.join(data_folder, 'C_model_delta_ACM.csv'), header=None)
            model_C=np.array(df.iloc[:,0].values)
            df = pd.read_csv(os.path.join(data_folder, 'N_model_delta_ACM.csv'), header=None)
            model_N=np.array(df.iloc[:,0].values)
            df = pd.read_csv(os.path.join(data_folder, 'O_model_delta_ACM.csv'), header=None)
            model_O=np.array(df.iloc[:,0].values)
            df = pd.read_csv(os.path.join(data_folder, 'F_model_delta_ACM.csv'), header=None)
            model_F=np.array(df.iloc[:,0].values)
    
            #using median kij
            sigma_C=485.092 # 0.48
            sigma_N=646.678 # 0.57
            sigma_O=831.413 # 0.63
            sigma_F=1766.171 # 0.78

    if rep.lower() == 'atmenv':

        X_train_C=np.load(os.path.join(data_folder, 'C_representation_AtmEnv.npy'))
        X_train_N=np.load(os.path.join(data_folder, 'N_representation_AtmEnv.npy'))
        X_train_O=np.load(os.path.join(data_folder, 'O_representation_AtmEnv.npy'))
        X_train_F=np.load(os.path.join(data_folder, 'F_representation_AtmEnv.npy'))
    
        if KRR_model.lower() == 'direct':
    
            df = pd.read_csv(os.path.join(data_folder, 'C_model_direct_AtmEnv.csv'), header=None)
            model_C=np.array(df.iloc[:,0].values)                        
            df = pd.read_csv(os.path.join(data_folder, 'N_model_direct_AtmEnv.csv'), header=None)
            model_N=np.array(df.iloc[:,0].values)                        
            df = pd.read_csv(os.path.join(data_folder, 'O_model_direct_AtmEnv.csv'), header=None)
            model_O=np.array(df.iloc[:,0].values)                        
            df = pd.read_csv(os.path.join(data_folder, 'F_model_direct_AtmEnv.csv'), header=None)
            model_F=np.array(df.iloc[:,0].values)
    
            #using median kij
            sigma_C=3.483 #0.21
            sigma_N=4.234 # 0.51
            sigma_O=5.530 # 0.75
            sigma_F=7.488 # 0.96
    
        if KRR_model.lower() == 'delta':
    
            df = pd.read_csv(os.path.join(data_folder, 'C_model_delta_AtmEnv.csv'), header=None)
            model_C=np.array(df.iloc[:,0].values)                       
            df = pd.read_csv(os.path.join(data_folder, 'N_model_delta_AtmEnv.csv'), header=None)
            model_N=np.array(df.iloc[:,0].values)                       
            df = pd.read_csv(os.path.join(data_folder, 'O_model_delta_AtmEnv.csv'), header=None)
            model_O=np.array(df.iloc[:,0].values)                       
            df = pd.read_csv(os.path.join(data_folder, 'F_model_delta_AtmEnv.csv'), header=None)
            model_F=np.array(df.iloc[:,0].values)
    
            #using median kij
            sigma_C=3.598 # 0.24
            sigma_N=3.927 # 0.45
            sigma_O=4.700 # 0.66
            sigma_F=4.681 # 0.900

    time2 = datetime.now()
    elapsed_time = time2-time1
    formatted_elapsed_time = "{:.2f}".format(elapsed_time.total_seconds())

    mol_Z = np.array(mol_Z)
    mol_R = np.array(mol_R)

    if rep.lower() == 'acm':
        desc_q = cebeconf.LocalCM(mol_Z, mol_R, 23, 6.0)
    if rep.lower() == 'atmenv':
        #print(mol_Z,mol_R)
        desc_q = cebeconf.AtomicEnvt(mol_Z,mol_R,23,6.0)

    BE = []
   # Predict with KRR
    for i_at in range(N_at):

        avail=[6,7,8,9]

        if mol_Z[i_at] in avail:

            dQ=desc_q[i_at]
            dQ=np.array([dQ])

            if mol_Z[i_at] == 6:
                sigma=sigma_C
            elif mol_Z[i_at] == 7:
                sigma=sigma_N
            elif mol_Z[i_at] == 8:
                sigma=sigma_O
            elif mol_Z[i_at] == 9:
                sigma=sigma_F

            time1 = datetime.now()
            if rep.lower() == 'acm':
                choice_kernel='L'
            if rep.lower() == 'atmenv':
                choice_kernel='G'

            if mol_Z[i_at] == 6:

                Kpred=[]
                for i in range(len(X_train_C)):
                    dT=X_train_C[i]
                    Kiq=cebeconf.kernel(choice_kernel,sigma,dT,dQ)
                    Kpred.append(Kiq)
                Epred=np.dot(Kpred,model_C)

            elif mol_Z[i_at] == 7:

                Kpred=[]
                for i in range(len(X_train_N)):
                    dT=X_train_N[i]
                    Kiq=cebeconf.kernel(choice_kernel,sigma,dT,dQ)
                    Kpred.append(Kiq)
                Epred=np.dot(Kpred,model_N)

            elif mol_Z[i_at] == 8:

                Kpred=[]
                for i in range(len(X_train_O)):
                    dT=X_train_O[i]
                    Kiq=cebeconf.kernel(choice_kernel,sigma,dT,dQ)
                    Kpred.append(Kiq)
                Epred=np.dot(Kpred,model_O)

            elif mol_Z[i_at] == 9:

                Kpred=[]
                for i in range(len(X_train_F)):
                    dT=X_train_F[i]
                    Kiq=cebeconf.kernel(choice_kernel,sigma,dT,dQ)
                    Kpred.append(Kiq)
                Epred=np.dot(Kpred,model_F)
            BE.append(Epred)
            Kijmax=np.max(Kpred)
            Kijmed=np.median(Kpred)

            time2 = datetime.now()
            elapsed_time = time2-time1
            formatted_elapsed_time = "{:.2f}".format(elapsed_time.total_seconds())
           #print(f" {i_at+1:4d} {at_types[i_at]} {mol_R[i_at][0]:15.8f} {mol_R[i_at][1]:15.8f} {mol_R[i_at][2]:15.8f} {Epred:10.2f} eV")
      #      print(f" {at_types[i_at]} {mol_R[i_at][0]:15.8f} {mol_R[i_at][1]:15.8f} {mol_R[i_at][2]:15.8f} {Epred:10.2f} eV, {formatted_elapsed_time} seconds {Kijmax:10.4f} {Kijmed:10.4f}")
           #print(f" {at_types[i_at]} {mol_R[i_at][0]:15.8f} {mol_R[i_at][1]:15.8f} {mol_R[i_at][2]:15.8f} {Epred:10.2f} eV, {formatted_elapsed_time} seconds")

     #   else:

           #print(f" {i_at+1:4d} {at_types[i_at]} {mol_R[i_at][0]:15.8f} {mol_R[i_at][1]:15.8f} {mol_R[i_at][2]:15.8f}")
    #        print(f" {at_types[i_at]} {mol_R[i_at][0]:15.8f} {mol_R[i_at][1]:15.8f} {mol_R[i_at][2]:15.8f}")

    # Calculate elapsed time
#    end_time = datetime.now()
#    elapsed_time = end_time - start_time
#    formatted_elapsed_time = "{:.2f}".format(elapsed_time.total_seconds())
#    print('')
#    print(" Total elapsed Time (seconds):", formatted_elapsed_time)
    return  BE
