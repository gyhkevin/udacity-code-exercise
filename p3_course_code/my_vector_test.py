# -*- coding: utf-8 -*-
from my_vector import Vector

v1 = Vector([8.218,-9.341])
w1 = Vector([-1.129,2.111])
print(v1.plus(w1))

v2 = Vector([7.119,8.215])
w2 = Vector([-8.223,0.878])
print(v2.minus(w2))

v3 = Vector([1.671,-1.012,-0.318])
c = 7.41
print(v3.times_scalar(c))

v4 = Vector([-0.221,7.437])
print(v4.magnitude())

v5 = Vector([8.813,-1.331,-6.247])
print(v5.magnitude())

v6 = Vector([5.581,-2.136])
print(v6.normalized())

v7 = Vector([1.996,3.108,-4.554])
print(v7.normalized())

v8 = Vector([7.887,4.138])
w8 = Vector([-8.802,6.776])
print(v8.dot(w8))

v9 = Vector([-5.955,-4.904,-1.874])
w9 = Vector([-4.496,-8.755,7.103])
print(v9.dot(w9))

v10 = Vector([3.183,-7.627])
w10 = Vector([-2.668,5.319])
print(v10.angle_with(w10))

v11 = Vector([7.35,0.221,5.188])
w11 = Vector([2.751,8.259,3.985])
print(v11.angle_with(w11, in_degrees=True))

v12 = Vector(['-7.579','-7.88'])
w12 = Vector(['22.737','23.64'])
print('v12 is parallel: ', v12.is_parallel_to(w12))
print('v12 is orthogonal: ', v12.is_orthogonal_to(w12))

v13 = Vector([-2.029,9.97,4.172])
w13 = Vector([-9.231,-6.639,-7.245])
print('v13 is parallel: ', v13.is_parallel_to(w13))
print('v13 is orthogonal: ', v13.is_orthogonal_to(w13))

v14 = Vector([-2.328,-7.284,-1.214])
w14 = Vector([-1.821,1.072,-2.94])
print('v14 is parallel: ', v14.is_parallel_to(w14))
print('v14 is orthogonal: ', v14.is_orthogonal_to(w14))

v15 = Vector([2.118,4.827])
w15 = Vector([0,0])
print('v15 is parallel: ', v15.is_parallel_to(w15))
print('v15 is orthogonal: ', v15.is_orthogonal_to(w15))

v16 = Vector([3.039,1.879])
w16 = Vector([0.825,2.036])
print v16.component_parallel_to(w16)

v17 = Vector([-9.88,-3.264,-8.159])
w17 = Vector([-2.155,-9.353,-9.473])
print v17.component_orthogonal_to(w17)

v18 = Vector([3.009,-6.172,3.692,-2.51])
w18 = Vector([6.404,-9.144,2.759,8.718])
pord = v18.component_parallel_to(w18)
oord = v18.component_orthogonal_to(w18)
print 'parallel component: ', pord
print 'orthogonal component: ', oord 

v19 = Vector([8.462,7.893,-8.187])
w19 = Vector([6.984,-5.975,4.778])
crr = v19.cross(w19)
print '#1: ',crr

v20 = Vector([-8.987,-9.838,5.031])
w20 = Vector([-4.268,-1.861,-8.866])
print('#2: ',v20.area_of_parallelogram_with(w20))

v21 = Vector([1.5,9.547,3.691])
w21 = Vector([-6.007,0.124,5.772])
print('#3: ',v21.area_of_triangle_with(w21))