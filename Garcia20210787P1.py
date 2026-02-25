
# -*- coding: utf-8 -*-
"""
Práctica 1: Mecánica pulmonar


Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México


Nombre del alumno: Alan Omar Garcia Toledo
Número de control: 20210787
Correo institucional: alan.garciat201@tectijuana.edu.mx


Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""

#libreria pip install controll
#libreria pip install slycot
# Librerias para calculo numerico y generacon de graficas
import numpy as np
import math as m
import matplotlib.pyplot as plt
import control as ctrl


# Datos de la simulación
x0,t0,tend,dt,w,h = 0,0,10,1E-3,7,3.5
N = round(tend/dt) + 1
t = np.linspace(t0,tend,N)
u1 = np.ones(N) #Step
u2 = np.zeros(N); u2[round(1/dt):round(2/dt)] = 1 #Impulse
u3 = t/tend #Ramp
u4 = np.sin(m.pi/2*t) #Sine function




# Componentes del circuito RLC y función de transferencia
R,L,C = 10,330E-6,470E-6
num = [C*L*R,C*R**2+L,R]
den = [3*C*L*R,5*C*R**2+L,2*R]
sys = ctrl.tf(num,den)
print(f"Función de transferencia del sistema: {sys}")
print(f"Lambda1: {np.roots(den)[0]}")
print(f"Lambda2: {np.roots(den)[1]}")


#\
# Componentes del controlador

kI = 33.8053

#%%Componentes del controlador
Cr = 1E-6
Re = 1/(Cr*kI)

print(f"El valor de capacitancia Cr es de {Cr} Faradios.\n")
print(f"El valor de resistencia de Re es de {Re} Ohms.\n")




numPID = [1]
denPID = [Re*Cr,0]
PID = ctrl.tf(numPID,denPID)
print(f"Funcion de transferencia del controlador I; {PID}")

# Sistema de control en lazo cerrado
x = ctrl.series(PID,sys)
sysPID = ctrl.feedback(x,1,sign = -1)
print(f"función de transferencia del sistema de control en lazo cerrado: {sysPID}")


# Respuesta del sistema en lazo abierto y en lazo cerrado
_,Vsu1 = ctrl.forced_response(sys,t,u1,x0)
_,Vsu2 = ctrl.forced_response(sys,t,u2,x0)
_,Vsu3 = ctrl.forced_response(sys,t,u3,x0)
_,Vsu4 = ctrl.forced_response(sys,t,u4,x0)

_,PIDu1 = ctrl.forced_response(sysPID,t,u1,x0)
_,PIDu2 = ctrl.forced_response(sysPID,t,u2,x0)
_,PIDu3 = ctrl.forced_response(sysPID,t,u3,x0)
_,PIDu4 = ctrl.forced_response(sysPID,t,u4,x0)

clr1 = np.array([184, 219, 128])/255
clr2 = np.array([247, 246, 211])/255
clr3 = np.array([255, 228, 239])/255
clr4 = np.array([243, 158, 182])/255
clr5 = np.array([250, 92, 92])/255

fg1 = plt.figure()#Respuesta al escalon
plt.plot(t,u1,'-',color = clr1,label='Ve(t)') #Entrada
plt.plot(t,Vsu1,'--',color = clr4,label='Vs(t)') #Respuesta en lazo abierto
plt.plot(t,PIDu1,':',linewidth=3,color = clr5,label='I(t)') #Respuesta en lazo cerrado
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(0,1.1); plt.yticks(np.arange(0,1.11,0.25))
plt.xlabel('t [s]',fontsize=11)
plt.ylabel('Vi(t) [V]',fontsize=11)
plt.legend(bbox_to_anchor=(0.5,-0.2),loc='center',ncol=3,
           fontsize=9,frameon=True)
plt.show()
fg1.savefig('step_python.pdf',bbox_inches='tight')


fg2 = plt.figure()#Respuesta al impulso
plt.plot(t,u2,'-',color = clr1,label='Ve(t)') #Entrada
plt.plot(t,Vsu2,'--',color = clr4,label='Vs(t)') #Respuesta en lazo abierto
plt.plot(t,PIDu2,':',linewidth=3,color = clr5,label='I(t)') #Respuesta en lazo cerrado
plt.xlim(0,1.5); plt.xticks(np.arange(0,11,1))
plt.ylim(0,1.2); plt.yticks(np.arange(0,1.21,0.2))
plt.xlabel('t [s]',fontsize=11)
plt.ylabel('Vi(t) [V]',fontsize=11)
plt.legend(bbox_to_anchor=(0.5,-0.2),loc='center',ncol=3,
           fontsize=9,frameon=True)
plt.show()
fg2.savefig('impulse_python.pdf',bbox_inches='tight')


fg3 = plt.figure()#Respuesta al rampa
plt.plot(t,u3,'-',color = clr1,label='Ve(t)') #Entrada
plt.plot(t,Vsu3,'--',color = clr4,label='Vs(t)') #Respuesta en lazo abierto
plt.plot(t,PIDu3,':',linewidth=3,color = clr5,label='I(t)') #Respuesta en lazo cerrado
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(0,1.2); plt.yticks(np.arange(0,1.2,0.1))
plt.xlabel('t [s]',fontsize=11)
plt.ylabel('Vi(t) [V]',fontsize=11)
plt.legend(bbox_to_anchor=(0.5,-0.2),loc='center',ncol=3,
           fontsize=9,frameon=True)
plt.show()
fg3.savefig('ramp_python.pdf',bbox_inches='tight')



fg4 = plt.figure()#Respuesta al sinusoidal
plt.plot(t,u4,'-',color = clr1,label='Ve(t)') #Entrada
plt.plot(t,Vsu4,'--',color = clr4,label='Vs(t)') #Respuesta en lazo abierto
plt.plot(t,PIDu4,':',linewidth=3,color = clr5,label='I(t)') #Respuesta en lazo cerrado
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(-1.2,1.2); plt.yticks(np.arange(-1,1.1,0.5))
plt.xlabel('t [s]',fontsize=11)
plt.ylabel('Vi(t) [V]',fontsize=11)
plt.legend(bbox_to_anchor=(0.5,-0.2),loc='center',ncol=3,
           fontsize=9,frameon=True)
plt.show()
fg4.savefig('sin_python.pdf',bbox_inches='tight')

