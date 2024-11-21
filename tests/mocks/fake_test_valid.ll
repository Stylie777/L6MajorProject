mov q0, #5
mov q1, #5
vhcadd.s32 q2, q1, q0, #270
add q0, q0, q1
vhcadd.s8 q2, q1, q0, #90

; CHECK: mov q0, #5
; CHECK-NEXT: mov q1, #5
; CHECK-NEXT: vhcadd.s32 q2, q1, q0, #270
; CHECK-NEXT: add q0, q0, q1
; CHECK-NEXT: vhcadd.s8 q2, q1, q0, #90