from .holtwinters_lib import linear,additive,multiplicative

_teste_array=[1,2,3,4,4,3,2,1,1,2,3,4,4,3,2,1,1,2,3,4]
_teste_sazonal_size=8
_teste_numero_previsoes=10

previsao,alpha,beta,gama,rmse=additive(_teste_array,_teste_sazonal_size,_teste_numero_previsoes)
print("previsao aditiva:alpha="+str(alpha)+",beta="+str(beta)+",gama="+str(gama)+",rmse="+str(rmse))
print("Array previsões:"+str(previsao))

previsao,alpha,beta,gama,rmse=multiplicative(_teste_array,_teste_sazonal_size,_teste_numero_previsoes)
print("previsao multiplicativa:alpha="+str(alpha)+",beta="+str(beta)+",gama="+str(gama)+",rmse="+str(rmse))
print("Array previsões:"+str(previsao))

previsao,alpha,beta,rmse=linear(_teste_array,_teste_sazonal_size,_teste_numero_previsoes)
print("previsao linear:alpha="+str(alpha)+",beta="+str(beta)+",rmse="+str(rmse))
print("Array previsões:"+str(previsao))