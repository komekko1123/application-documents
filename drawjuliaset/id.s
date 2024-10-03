

      .data
str1: .asciz "%d"
str2: .asciz " %c"
str3: .asciz "%*"
strEl: .asciz "%d\n"
I1:   .asciz "*****Input ID*****\n** Please Enter Member 1 ID:**\n" @ I1 and M1
M1SID:.word 0
M2:   .asciz "** Please Enter Member 2 ID:**\n"
M2SID:.word 0
M3:   .asciz "** Please Enter Member 3 ID:**\n"
M3SID:.word 0
P1:   .asciz "** Please Enter Command **\n"
S1:   .asciz "*****Print Team Member ID and ID Summation*****\n"
S1M:  .asciz "\nID Summation = %d\n"
EP:   .asciz "*****End Print*****\n\n"
C:    .byte '\0'
CP:   .byte 'p'
CP1:  .byte '\0'
SUM:  .word 0
      .text
      .global id

id:   stmfd sp!,{r0-r10,lr}  @ r4~7 123-id   r8 = sum
      ldr r0, =I1
      bl printf
      ldrvc r0, =str1 @ CE-1 vc (no overflow)
      subs r1, pc, lr
      ldr r1, =M1SID
	  mov r10,#0 @ r10 = 0
	  mov r9, #0 @ r9 = 0
      str r10,[r1,#0]  @ OP1   r10 store it r1 => r1's value = 0  LS-1  str
      ldr r10,[r1],#0  @ OP2   r10 = r1 => r10 = 0 || r1 += 0     LS-2  ldr
      ldr r10,[r1,r10,lsl #0] @ OP3 r10 = r1 + r10 logical shift left => r10 = 0+0*1 => ldr r10 = 0
      ldr r10,[r1],r9,asr #0 @ OP4 r10 = r1 = > r10 = 0  || r1 += r9 / 1 (r9 = 0)  Arithmetic shift right
      bl scanf
      ldr r1, =M1SID
      ldr r1,[r1]     @ OP5 r1 = [r1] value
      mov r4,r1
      @ 111111
      ldr r0, =M2
      bl printf
      ldr r0, =str1
      ldr r1, =M2SID
      bl scanf
      ldr r1, =M2SID
      ldr r1,[r1]
      mov r5,r1
      @ 222222
      ldr r0, =M3
      bl printf
      ldr r0, =str1
      ldr r1, =M3SID
      bl scanf
      ldr r1, =M3SID
      ldr r1,[r1]
      mov r6,r1
      @ 333333
      ldr r0, =P1
      bl printf
	  b while

while: ldr r7,=CP
       ldr r9,=CP1
       ldrb r7,[r7] @ LS-2     ldrb
	   strb r7,[r9] @ LS-3     strb
       bl getchar   @ read \n
       bl getchar
       cmp r0,r7
	   beq done      @ CE-2 eq      (equal)
	   bne while     @ CE-3 ne      (not equal)
	   addge r10,#0  @ CE-4 ge (great than or equal)
	   addle r10,#1  @ CE-5 le  ( lower than or equal)

done: ldr r0,=S1
      bl printf
      ldr r0,=strEl
      mov r1,r4
      bl printf
      ldr r0,=strEl
      mov r1,r5
      bl printf
      ldr r0,=strEl
      mov r1,r6
      bl printf
      ldr r0,=S1M
      ldr r1,=SUM
      ldr r1,[r1]
      add r1,r4
      add r1,r5
      add r1,r6
      mov r8,r1
      bleq printf
      @CP = p
      ldr r0,=EP
      bl printf
	  ldmfd sp!,{r0-r3}
	  str r4, [r0]
	  str r5, [r1]
	  str r6, [r2]
	  str r8, [r3]
      ldmfd sp!,{r4-r10,lr}
      mov pc,lr

