	  .global __aeabi_idiv
	  .data
      @x@
      .text

      .global drawJuliaSet
drawJuliaSet:
      stmfd sp!,{r4-r11,lr} @ r4 frame r5 x r6 y r7 zx r8 zy r9 i r10 color
      add r4,sp,#40	@ r4 frame
	  add fp,sp,#0 @ move  frame to sp(fp) + 8
	  sub sp,sp,#48 @ push 48 space
	  str r0,[fp,#-4] @ store cX
	  str r1,[fp,#-8] @ ~    cY
	  str r2,[fp,#-12] @ ~    width
	  str r3,[fp,#-16] @ ~    height    -----------------homework request 1-1  OP2  store r3 to stack


      @ trash condition for homework request 1
      add r1,fp,#16 @ r1 = address of width
      mov r2,#0 @ r2 = 0
	  ldr r0,[r1],#0  @  -----------------homework request 1-2 OP2   r0 = width || width += 0
      ldr r0,[r1,r2,lsl #0] @ -----------------homework request 1-3 OP2   r0 = (r1+r2)*1
      ldr r0,[r1],r2,asr #0 @ -----------------homework request 1-4 OP2   r0 = r1 || r1 += r2 / 1
      @ trash condition for homework request 1

      mov r5,#0     @ x = 0 @ -----------------homework request 1-5 OP2   r5 = 0
	  b for_x

for_x: ldr r0,[fp,#-12] @ width
	  cmp r5,r0  @ compare x ,width
      movlt r6,#0 @ x < width  go for-> y = 0 -----------------homework request 2-1 Conditional Execution 1
	  blt for_y
	  b done @ end
for_y: ldr r0,[fp,#-16] @ height
	   cmp r6,r0 @ compare y, height
	   addge r5,r5,#1 @ x++ y >= height ------------------homework request 2-2 Conditional Execution 2
	   bge for_x @ go x
	   ldr r0,[fp,#-12] @ width
       ldr r3,.constant  @ 1500
	   mov r1,r0,lsr #1 @ width>>1
	   sub r0,r5,r1     @ x - width>>1
	   mul r0,r0,r3     @ 1500 * ( x - width>>1 )
	   bl __aeabi_idiv  @ 1500 * ( x - width>>1 ) / (width>>1)
	   mov r7,r0 @ r7 = zx =>  zx = 1500 * ( x - width>>1 ) / (width>>1)

	   ldr r0,[fp,#-16] @ height
	   ldr r3,.constant+4 @ 1000
	   mov r1,r0,lsr #1  @ (height>>1)
	   sub r0,r6,r1      @ (y - (height>>1)) / (height>>1)
	   mul r0,r0,r3      @  1000 * (y - (height>>1)) / (height>>1)
	   bl __aeabi_idiv
	   mov r8,r0 @ r8 = zy =>  zy = 1000 * (y - (height>>1)) / (height>>1)
	   mov r9,#255 @ r9 = maxitem

while1: mul r0,r7,r7 @ r0 = zx * zx
		mul r1,r8,r8 @ r1 = zy * zy
		add r2,r0,r1 @ r2 = zx * zx + zy * zy
		ldr r3,.constant+8 @ 4000000
		cmp r2,r3
	    bge for_y2 @ out loop zx * zx + zy * zy  4000000
		cmp r9,#0
		ble for_y2 @ out loop i <= 0 -----------------homework request 2-3 Conditional Execution 3
		b while2   @ zx * zx + zy * zy < 4000000 && i > 0


while2:  mul r0,r7,r7 @ r0 = zx * zx
		 mul r1,r8,r8 @ r1 = zy * zy
		 sub r0,r0,r1 @ r0 = (zx * zx - zy * zy)
		 ldr r1,.constant+4  @ r1 = 1000
		 bl __aeabi_idiv  @ r0 = (zx * zx - zy * zy)/1000
		 ldr r1,[fp,#-4] @ r1 = cX
		 add r0,r0,r1 @ r0 = (zx * zx - zy * zy)/1000 + cX
		 str r0,[fp,#-20] @tmp = = (zx * zx - zy * zy)/1000 + cX
		 mov r0,#2 @ r0 = 2
		 mul r0,r0,r7 @ r0 = r0*r7 = 2*zx
		 mul r0,r0,r8 @ r0 = r0*r8 = 2*zx * zy
		 ldr r1,.constant+4 @ r1 = 1000
		 bl __aeabi_idiv @ r0 = (2 * zx * zy)/1000
		 ldr r1,[fp,#-8] @ r1 = cY
		 add r8,r0,r1    @ r8(zy) => zy = (2 * zx * zy)/1000 + cY;
		 ldr r7,[fp,#-20] @ r7(zx)  zx = tmp
		 sub r9,r9,#1  @   r9(i) = i--
		 b while1 @ while loop

for_y2:  and r0,r9,#0xff  @ r0 = i&0xff
         mov r2,r0,lsl #8 @ r2 = (i&0xff)<<8
		 orr r1,r0,r2     @ r1 = ((i&0xff)<<8) | (i&0xff)  | = (or)
	     mov r10,r1       @ color = r1
         mov r3,#65536    @ r3 = 0xffff + 1  (65535 is no a 0~255 * 2')
	     sub r3,r3,#1     @ r3 = r3 - 1 = 0xffff
	     mvn r10,r10      @ color = (~color)
	     and r10,r10,r3  @ color = (~color) & 0xffff   & = (and)

		 mov r0,r4      @ r0 = frame pointer fp
         mov r1,#1280   @ (y) 640 * 2   (one y = x'->640 )  ( int16_t = 2) *2
         mov r2,#2      @ (x) x * 2     (one x = 0~640)     ( 2byte ) *2
         mul r1,r6,r1   @ 640 * 2 * y
         mul r2,r2,r5   @ 2 * 2 * x
         add r0,r1      @ frame + 640 * 2 * y -> frame[y][?]
         add r0,r2      @ frame + 2 * 2 * x  -> frame[y][x]
         strh r10,[r0,#0] @ frame[y][x] = color;
		 add r6,r6,#1  @ y++
		 b for_y  @ y loop

done: sub sp,fp,#0 @ pop sp
	  add lr,r0,pc @   ------------------homework request 3
      ldmfd sp!,{r4-r11,lr} @ restore r4-r11 lr
      mov pc, lr
      mov r0, #0 @ return 0


	 .constant:
c1:  .word 1500
c2:	 .word 1000
c3:	 .word 4000000
c4:	 .word 255 @ maxitem
	@	int maxIter = 255;
	@	int zx, zy;
	@	int tmp;
	@	int i;
	@	int x, y;


