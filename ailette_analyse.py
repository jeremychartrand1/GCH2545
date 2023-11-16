# Importation des modules
import numpy as np
import matplotlib.pyplot as plt
import pytest
import ailette_corr
try:
    from ailette_fct import *
except:
    pass

#------------------------------------------------------------------------------
# Code principal pour l'analyse des résultats
# Il faudra faire appel aux fonctions programmées dans ailette_fct.py afin de
# modéliser les pertes de chaleurs selon différentes combinaisons géométriques.
# Ensuite, il faudra identifier le meilleur rendement.
#------------------------------------------------------------------------------

# Assignation des paramètres
# ATTENTION! Ne pas changer le nom des attributs
class parametres():
    k = 45
    T_a = 25+273.15
    T_w = 125+273.15
    h = 120
    N = 30
    L = 0.1
    D = 0.0025
class parametres2():
    k = 45
    T_a = 25+273.15
    T_w = 125+273.15
    h = 120
    N = 1000
    L = 0.1
    D = 0.0025

prm = parametres()

# Appel des fonctions pour le calcul du profil de température
T_n,p_n=mdf(parametres)
'fonction analytique'
z=np.linspace(0,parametres.L,parametres.N)
t_an=np.zeros(parametres.N)
m=((4*parametres.h)/(parametres.k*parametres.D))**0.5
T_an=parametres.T_a+(parametres.T_w-parametres.T_a)*((np.cosh(m*(parametres.L-z)))/(np.cosh(m*parametres.L)))
# Graphique
fig,ax=plt.subplots()
ax.plot(p_n,T_n,"bo",label="Methode numerique")
ax.plot(z,T_an,"r+",label="Methode analytique")
ax.set_title("La temperature en fonction de la position avec deux methodes a N=%s." % parametres.N) 
ax.set_ylabel("Temperature [K]")
ax.set_xlabel("Position sur l'ailette [m]")
ax.legend()


#plt.show()

print(inte(T_n,p_n,parametres))
# Calcul de la dissipation pour chaque géométrie
T_r,p_r=mdf(parametres2)
ref=inte(T_r,p_r,parametres2)
eur=0.01*ref
T_n2,p_n2=mdf(parametres)
num=inte(T_n2,p_n2,parametres)
e=abs(num-ref)/ref
if eur>e:
    print("N=%s. est bon"%parametres.N)
L_=np.array([0.01,0.0125,0.015])
D_=np.array([0.018,0.016,0.025])
chaleur=np.zeros(len(D_))

fig,ax2=plt.subplots()
for i in range(len(L_)):
    k=0
    Dia=np.zeros(len(D_))
    for j in range(len(D_)):
        parametres.L=L_[i]
        parametres.D=D_[j]
        T,p=mdf(parametres)
        chaleur[k]=inte(T,p,parametres)
        print(L_[i],D_[j],chaleur[k],((chaleur[k])/((L_[i]*np.pi*D_[j]**2)/4)))

        k=k+1  
    ax2.plot(D_,chaleur,"-+",label="L=%s. [m]" %L_[i])    
ax2.plot(D_,(np.ones(len(D_))*10),label="q=10 W")
ax2.legend()
ax2.set_title("La dissipation de l'ailette en fonction du diametre [0.001,0.02] m  pour plusieurs L [m]")
ax2.set_ylabel("Dissipation en W")
ax2.set_xlabel("Diametre de l'ailette [m]")
plt.show()
# Graphique


# Correction
pytest.main(['-q', '--tb=long', 'ailette_corr.py'])
