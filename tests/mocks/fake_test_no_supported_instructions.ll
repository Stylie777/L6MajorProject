mov q0, #5
mov q1, #5
add q0, q0, q1

; CHECK: mov q0, #5
; CHECK-NEXT: mov q1, #5
; CHECK-NEXT: add q0, q0, q1