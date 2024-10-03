      .data
P1: .asciz "*****Print Name*****\n"
team: .asciz "Team 04\n\0"
person1: .asciz "Messi Chang\n\0"
person2: .asciz "Ronaldo Pon\n\0"
person3: .asciz "Neymar Wu\n\0"
E1: .asciz "*****End Print*****\n\n"
      .text
      .global name
name: stmfd sp!,{r0-r7,lr}
      mov r4,r0
      mov r5,r1
      mov r6,r2
      mov r7,r3
	  ldr r0, =P1
      bl printf
      ldr r0, =team
      bl printf
      ldr r0, =person1
      bl printf
      ldr r0, =person2
      bl printf
      ldr r0, =person3
      bl printf
      ldr r0, =E1
      bl printf

      ldmfd  sp!,{r0}
      ldr r1, =team
      bl strcpy

      ldmfd  sp!,{r1}
      mov r0,r1
      ldr r1, =person1
      bl strcpy

      ldmfd  sp!,{r2}
      mov r0,r2
      ldr r1, =person2
      bl strcpy

	  ldmfd  sp!,{r3}
	  mov r0,r3
      ldr r1, =person3
      bl strcpy

      mov r0,r4
      mov r1,r5
      mov r2,r6
      mov r3,r7
      ldmfd sp!,{r4-r7,lr}
      mov pc, lr




