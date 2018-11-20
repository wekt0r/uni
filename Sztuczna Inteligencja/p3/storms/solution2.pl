:- use_module(library(clpfd)).
solve([B_0_0, B_0_1, B_0_2, B_0_3, B_0_4, B_0_5, B_0_6, B_0_7, B_0_8, B_0_9, B_1_0, B_1_1, B_1_2, B_1_3, B_1_4, B_1_5, B_1_6, B_1_7, B_1_8, B_1_9, B_2_0, B_2_1, B_2_2, B_2_3, B_2_4, B_2_5, B_2_6, B_2_7, B_2_8, B_2_9, B_3_0, B_3_1, B_3_2, B_3_3, B_3_4, B_3_5, B_3_6, B_3_7, B_3_8, B_3_9, B_4_0, B_4_1, B_4_2, B_4_3, B_4_4, B_4_5, B_4_6, B_4_7, B_4_8, B_4_9, B_5_0, B_5_1, B_5_2, B_5_3, B_5_4, B_5_5, B_5_6, B_5_7, B_5_8, B_5_9, B_6_0, B_6_1, B_6_2, B_6_3, B_6_4, B_6_5, B_6_6, B_6_7, B_6_8, B_6_9, B_7_0, B_7_1, B_7_2, B_7_3, B_7_4, B_7_5, B_7_6, B_7_7, B_7_8, B_7_9, B_8_0, B_8_1, B_8_2, B_8_3, B_8_4, B_8_5, B_8_6, B_8_7, B_8_8, B_8_9, B_9_0, B_9_1, B_9_2, B_9_3, B_9_4, B_9_5, B_9_6, B_9_7, B_9_8, B_9_9]) :- 
   B_0_0 in 0..1,B_0_1 in 0..1,B_0_2 in 0..1,B_0_3 in 0..1,B_0_4 in 0..1,B_0_5 in 0..1,
   B_0_6 in 0..1,B_0_7 in 0..1,B_0_8 in 0..1,B_0_9 in 0..1,B_1_0 in 0..1,B_1_1 in 0..1,
   B_1_2 in 0..1,B_1_3 in 0..1,B_1_4 in 0..1,B_1_5 in 0..1,B_1_6 in 0..1,B_1_7 in 0..1,
   B_1_8 in 0..1,B_1_9 in 0..1,B_2_0 in 0..1,B_2_1 in 0..1,B_2_2 in 0..1,B_2_3 in 0..1,
   B_2_4 in 0..1,B_2_5 in 0..1,B_2_6 in 0..1,B_2_7 in 0..1,B_2_8 in 0..1,B_2_9 in 0..1,
   B_3_0 in 0..1,B_3_1 in 0..1,B_3_2 in 0..1,B_3_3 in 0..1,B_3_4 in 0..1,B_3_5 in 0..1,
   B_3_6 in 0..1,B_3_7 in 0..1,B_3_8 in 0..1,B_3_9 in 0..1,B_4_0 in 0..1,B_4_1 in 0..1,
   B_4_2 in 0..1,B_4_3 in 0..1,B_4_4 in 0..1,B_4_5 in 0..1,B_4_6 in 0..1,B_4_7 in 0..1,
   B_4_8 in 0..1,B_4_9 in 0..1,B_5_0 in 0..1,B_5_1 in 0..1,B_5_2 in 0..1,B_5_3 in 0..1,
   B_5_4 in 0..1,B_5_5 in 0..1,B_5_6 in 0..1,B_5_7 in 0..1,B_5_8 in 0..1,B_5_9 in 0..1,
   B_6_0 in 0..1,B_6_1 in 0..1,B_6_2 in 0..1,B_6_3 in 0..1,B_6_4 in 0..1,B_6_5 in 0..1,
   B_6_6 in 0..1,B_6_7 in 0..1,B_6_8 in 0..1,B_6_9 in 0..1,B_7_0 in 0..1,B_7_1 in 0..1,
   B_7_2 in 0..1,B_7_3 in 0..1,B_7_4 in 0..1,B_7_5 in 0..1,B_7_6 in 0..1,B_7_7 in 0..1,
   B_7_8 in 0..1,B_7_9 in 0..1,B_8_0 in 0..1,B_8_1 in 0..1,B_8_2 in 0..1,B_8_3 in 0..1,
   B_8_4 in 0..1,B_8_5 in 0..1,B_8_6 in 0..1,B_8_7 in 0..1,B_8_8 in 0..1,B_8_9 in 0..1,
   B_9_0 in 0..1,B_9_1 in 0..1,B_9_2 in 0..1,B_9_3 in 0..1,B_9_4 in 0..1,B_9_5 in 0..1,
   B_9_6 in 0..1,B_9_7 in 0..1,B_9_8 in 0..1,B_9_9 in 0..1,B_0_0 + B_0_1 + B_0_2 + B_0_3 + B_0_4 + B_0_5 + B_0_6 + B_0_7 + B_0_8 + B_0_9 #= 3,
   B_1_0 + B_1_1 + B_1_2 + B_1_3 + B_1_4 + B_1_5 + B_1_6 + B_1_7 + B_1_8 + B_1_9 #= 8,
   B_2_0 + B_2_1 + B_2_2 + B_2_3 + B_2_4 + B_2_5 + B_2_6 + B_2_7 + B_2_8 + B_2_9 #= 5,
   B_3_0 + B_3_1 + B_3_2 + B_3_3 + B_3_4 + B_3_5 + B_3_6 + B_3_7 + B_3_8 + B_3_9 #= 3,
   B_4_0 + B_4_1 + B_4_2 + B_4_3 + B_4_4 + B_4_5 + B_4_6 + B_4_7 + B_4_8 + B_4_9 #= 3,
   B_5_0 + B_5_1 + B_5_2 + B_5_3 + B_5_4 + B_5_5 + B_5_6 + B_5_7 + B_5_8 + B_5_9 #= 5,
   B_6_0 + B_6_1 + B_6_2 + B_6_3 + B_6_4 + B_6_5 + B_6_6 + B_6_7 + B_6_8 + B_6_9 #= 5,
   B_7_0 + B_7_1 + B_7_2 + B_7_3 + B_7_4 + B_7_5 + B_7_6 + B_7_7 + B_7_8 + B_7_9 #= 5,
   B_8_0 + B_8_1 + B_8_2 + B_8_3 + B_8_4 + B_8_5 + B_8_6 + B_8_7 + B_8_8 + B_8_9 #= 2,
   B_9_0 + B_9_1 + B_9_2 + B_9_3 + B_9_4 + B_9_5 + B_9_6 + B_9_7 + B_9_8 + B_9_9 #= 2,
   B_0_0 + B_1_0 + B_2_0 + B_3_0 + B_4_0 + B_5_0 + B_6_0 + B_7_0 + B_8_0 + B_9_0 #= 0,
   B_0_1 + B_1_1 + B_2_1 + B_3_1 + B_4_1 + B_5_1 + B_6_1 + B_7_1 + B_8_1 + B_9_1 #= 2,
   B_0_2 + B_1_2 + B_2_2 + B_3_2 + B_4_2 + B_5_2 + B_6_2 + B_7_2 + B_8_2 + B_9_2 #= 7,
   B_0_3 + B_1_3 + B_2_3 + B_3_3 + B_4_3 + B_5_3 + B_6_3 + B_7_3 + B_8_3 + B_9_3 #= 7,
   B_0_4 + B_1_4 + B_2_4 + B_3_4 + B_4_4 + B_5_4 + B_6_4 + B_7_4 + B_8_4 + B_9_4 #= 2,
   B_0_5 + B_1_5 + B_2_5 + B_3_5 + B_4_5 + B_5_5 + B_6_5 + B_7_5 + B_8_5 + B_9_5 #= 2,
   B_0_6 + B_1_6 + B_2_6 + B_3_6 + B_4_6 + B_5_6 + B_6_6 + B_7_6 + B_8_6 + B_9_6 #= 0,
   B_0_7 + B_1_7 + B_2_7 + B_3_7 + B_4_7 + B_5_7 + B_6_7 + B_7_7 + B_8_7 + B_9_7 #= 7,
   B_0_8 + B_1_8 + B_2_8 + B_3_8 + B_4_8 + B_5_8 + B_6_8 + B_7_8 + B_8_8 + B_9_8 #= 7,
   B_0_9 + B_1_9 + B_2_9 + B_3_9 + B_4_9 + B_5_9 + B_6_9 + B_7_9 + B_8_9 + B_9_9 #= 7,
   B_0_5 #= 0,B_0_6 #= 0,B_1_5 #= 1,B_1_6 #= 0,(B_1_1 #= 1) #==> (B_0_1 + B_2_1 #> 0), (B_1_1 #= 1) #==> (B_1_0 + B_1_2 #> 0),
   (B_1_2 #= 1) #==> (B_0_2 + B_2_2 #> 0), (B_1_2 #= 1) #==> (B_1_1 + B_1_3 #> 0),
   (B_1_3 #= 1) #==> (B_0_3 + B_2_3 #> 0), (B_1_3 #= 1) #==> (B_1_2 + B_1_4 #> 0),
   (B_1_4 #= 1) #==> (B_0_4 + B_2_4 #> 0), (B_1_4 #= 1) #==> (B_1_3 + B_1_5 #> 0),
   (B_1_5 #= 1) #==> (B_0_5 + B_2_5 #> 0), (B_1_5 #= 1) #==> (B_1_4 + B_1_6 #> 0),
   (B_1_6 #= 1) #==> (B_0_6 + B_2_6 #> 0), (B_1_6 #= 1) #==> (B_1_5 + B_1_7 #> 0),
   (B_1_7 #= 1) #==> (B_0_7 + B_2_7 #> 0), (B_1_7 #= 1) #==> (B_1_6 + B_1_8 #> 0),
   (B_1_8 #= 1) #==> (B_0_8 + B_2_8 #> 0), (B_1_8 #= 1) #==> (B_1_7 + B_1_9 #> 0),
   (B_2_1 #= 1) #==> (B_1_1 + B_3_1 #> 0), (B_2_1 #= 1) #==> (B_2_0 + B_2_2 #> 0),
   (B_2_2 #= 1) #==> (B_1_2 + B_3_2 #> 0), (B_2_2 #= 1) #==> (B_2_1 + B_2_3 #> 0),
   (B_2_3 #= 1) #==> (B_1_3 + B_3_3 #> 0), (B_2_3 #= 1) #==> (B_2_2 + B_2_4 #> 0),
   (B_2_4 #= 1) #==> (B_1_4 + B_3_4 #> 0), (B_2_4 #= 1) #==> (B_2_3 + B_2_5 #> 0),
   (B_2_5 #= 1) #==> (B_1_5 + B_3_5 #> 0), (B_2_5 #= 1) #==> (B_2_4 + B_2_6 #> 0),
   (B_2_6 #= 1) #==> (B_1_6 + B_3_6 #> 0), (B_2_6 #= 1) #==> (B_2_5 + B_2_7 #> 0),
   (B_2_7 #= 1) #==> (B_1_7 + B_3_7 #> 0), (B_2_7 #= 1) #==> (B_2_6 + B_2_8 #> 0),
   (B_2_8 #= 1) #==> (B_1_8 + B_3_8 #> 0), (B_2_8 #= 1) #==> (B_2_7 + B_2_9 #> 0),
   (B_3_1 #= 1) #==> (B_2_1 + B_4_1 #> 0), (B_3_1 #= 1) #==> (B_3_0 + B_3_2 #> 0),
   (B_3_2 #= 1) #==> (B_2_2 + B_4_2 #> 0), (B_3_2 #= 1) #==> (B_3_1 + B_3_3 #> 0),
   (B_3_3 #= 1) #==> (B_2_3 + B_4_3 #> 0), (B_3_3 #= 1) #==> (B_3_2 + B_3_4 #> 0),
   (B_3_4 #= 1) #==> (B_2_4 + B_4_4 #> 0), (B_3_4 #= 1) #==> (B_3_3 + B_3_5 #> 0),
   (B_3_5 #= 1) #==> (B_2_5 + B_4_5 #> 0), (B_3_5 #= 1) #==> (B_3_4 + B_3_6 #> 0),
   (B_3_6 #= 1) #==> (B_2_6 + B_4_6 #> 0), (B_3_6 #= 1) #==> (B_3_5 + B_3_7 #> 0),
   (B_3_7 #= 1) #==> (B_2_7 + B_4_7 #> 0), (B_3_7 #= 1) #==> (B_3_6 + B_3_8 #> 0),
   (B_3_8 #= 1) #==> (B_2_8 + B_4_8 #> 0), (B_3_8 #= 1) #==> (B_3_7 + B_3_9 #> 0),
   (B_4_1 #= 1) #==> (B_3_1 + B_5_1 #> 0), (B_4_1 #= 1) #==> (B_4_0 + B_4_2 #> 0),
   (B_4_2 #= 1) #==> (B_3_2 + B_5_2 #> 0), (B_4_2 #= 1) #==> (B_4_1 + B_4_3 #> 0),
   (B_4_3 #= 1) #==> (B_3_3 + B_5_3 #> 0), (B_4_3 #= 1) #==> (B_4_2 + B_4_4 #> 0),
   (B_4_4 #= 1) #==> (B_3_4 + B_5_4 #> 0), (B_4_4 #= 1) #==> (B_4_3 + B_4_5 #> 0),
   (B_4_5 #= 1) #==> (B_3_5 + B_5_5 #> 0), (B_4_5 #= 1) #==> (B_4_4 + B_4_6 #> 0),
   (B_4_6 #= 1) #==> (B_3_6 + B_5_6 #> 0), (B_4_6 #= 1) #==> (B_4_5 + B_4_7 #> 0),
   (B_4_7 #= 1) #==> (B_3_7 + B_5_7 #> 0), (B_4_7 #= 1) #==> (B_4_6 + B_4_8 #> 0),
   (B_4_8 #= 1) #==> (B_3_8 + B_5_8 #> 0), (B_4_8 #= 1) #==> (B_4_7 + B_4_9 #> 0),
   (B_5_1 #= 1) #==> (B_4_1 + B_6_1 #> 0), (B_5_1 #= 1) #==> (B_5_0 + B_5_2 #> 0),
   (B_5_2 #= 1) #==> (B_4_2 + B_6_2 #> 0), (B_5_2 #= 1) #==> (B_5_1 + B_5_3 #> 0),
   (B_5_3 #= 1) #==> (B_4_3 + B_6_3 #> 0), (B_5_3 #= 1) #==> (B_5_2 + B_5_4 #> 0),
   (B_5_4 #= 1) #==> (B_4_4 + B_6_4 #> 0), (B_5_4 #= 1) #==> (B_5_3 + B_5_5 #> 0),
   (B_5_5 #= 1) #==> (B_4_5 + B_6_5 #> 0), (B_5_5 #= 1) #==> (B_5_4 + B_5_6 #> 0),
   (B_5_6 #= 1) #==> (B_4_6 + B_6_6 #> 0), (B_5_6 #= 1) #==> (B_5_5 + B_5_7 #> 0),
   (B_5_7 #= 1) #==> (B_4_7 + B_6_7 #> 0), (B_5_7 #= 1) #==> (B_5_6 + B_5_8 #> 0),
   (B_5_8 #= 1) #==> (B_4_8 + B_6_8 #> 0), (B_5_8 #= 1) #==> (B_5_7 + B_5_9 #> 0),
   (B_6_1 #= 1) #==> (B_5_1 + B_7_1 #> 0), (B_6_1 #= 1) #==> (B_6_0 + B_6_2 #> 0),
   (B_6_2 #= 1) #==> (B_5_2 + B_7_2 #> 0), (B_6_2 #= 1) #==> (B_6_1 + B_6_3 #> 0),
   (B_6_3 #= 1) #==> (B_5_3 + B_7_3 #> 0), (B_6_3 #= 1) #==> (B_6_2 + B_6_4 #> 0),
   (B_6_4 #= 1) #==> (B_5_4 + B_7_4 #> 0), (B_6_4 #= 1) #==> (B_6_3 + B_6_5 #> 0),
   (B_6_5 #= 1) #==> (B_5_5 + B_7_5 #> 0), (B_6_5 #= 1) #==> (B_6_4 + B_6_6 #> 0),
   (B_6_6 #= 1) #==> (B_5_6 + B_7_6 #> 0), (B_6_6 #= 1) #==> (B_6_5 + B_6_7 #> 0),
   (B_6_7 #= 1) #==> (B_5_7 + B_7_7 #> 0), (B_6_7 #= 1) #==> (B_6_6 + B_6_8 #> 0),
   (B_6_8 #= 1) #==> (B_5_8 + B_7_8 #> 0), (B_6_8 #= 1) #==> (B_6_7 + B_6_9 #> 0),
   (B_7_1 #= 1) #==> (B_6_1 + B_8_1 #> 0), (B_7_1 #= 1) #==> (B_7_0 + B_7_2 #> 0),
   (B_7_2 #= 1) #==> (B_6_2 + B_8_2 #> 0), (B_7_2 #= 1) #==> (B_7_1 + B_7_3 #> 0),
   (B_7_3 #= 1) #==> (B_6_3 + B_8_3 #> 0), (B_7_3 #= 1) #==> (B_7_2 + B_7_4 #> 0),
   (B_7_4 #= 1) #==> (B_6_4 + B_8_4 #> 0), (B_7_4 #= 1) #==> (B_7_3 + B_7_5 #> 0),
   (B_7_5 #= 1) #==> (B_6_5 + B_8_5 #> 0), (B_7_5 #= 1) #==> (B_7_4 + B_7_6 #> 0),
   (B_7_6 #= 1) #==> (B_6_6 + B_8_6 #> 0), (B_7_6 #= 1) #==> (B_7_5 + B_7_7 #> 0),
   (B_7_7 #= 1) #==> (B_6_7 + B_8_7 #> 0), (B_7_7 #= 1) #==> (B_7_6 + B_7_8 #> 0),
   (B_7_8 #= 1) #==> (B_6_8 + B_8_8 #> 0), (B_7_8 #= 1) #==> (B_7_7 + B_7_9 #> 0),
   (B_8_1 #= 1) #==> (B_7_1 + B_9_1 #> 0), (B_8_1 #= 1) #==> (B_8_0 + B_8_2 #> 0),
   (B_8_2 #= 1) #==> (B_7_2 + B_9_2 #> 0), (B_8_2 #= 1) #==> (B_8_1 + B_8_3 #> 0),
   (B_8_3 #= 1) #==> (B_7_3 + B_9_3 #> 0), (B_8_3 #= 1) #==> (B_8_2 + B_8_4 #> 0),
   (B_8_4 #= 1) #==> (B_7_4 + B_9_4 #> 0), (B_8_4 #= 1) #==> (B_8_3 + B_8_5 #> 0),
   (B_8_5 #= 1) #==> (B_7_5 + B_9_5 #> 0), (B_8_5 #= 1) #==> (B_8_4 + B_8_6 #> 0),
   (B_8_6 #= 1) #==> (B_7_6 + B_9_6 #> 0), (B_8_6 #= 1) #==> (B_8_5 + B_8_7 #> 0),
   (B_8_7 #= 1) #==> (B_7_7 + B_9_7 #> 0), (B_8_7 #= 1) #==> (B_8_6 + B_8_8 #> 0),
   (B_8_8 #= 1) #==> (B_7_8 + B_9_8 #> 0), (B_8_8 #= 1) #==> (B_8_7 + B_8_9 #> 0),
   (B_0_0 + B_1_1 #= 2) #<==> (B_1_0 + B_0_1 #=2),(B_0_1 + B_1_2 #= 2) #<==> (B_1_1 + B_0_2 #=2),
   (B_0_2 + B_1_3 #= 2) #<==> (B_1_2 + B_0_3 #=2),(B_0_3 + B_1_4 #= 2) #<==> (B_1_3 + B_0_4 #=2),
   (B_0_4 + B_1_5 #= 2) #<==> (B_1_4 + B_0_5 #=2),(B_0_5 + B_1_6 #= 2) #<==> (B_1_5 + B_0_6 #=2),
   (B_0_6 + B_1_7 #= 2) #<==> (B_1_6 + B_0_7 #=2),(B_0_7 + B_1_8 #= 2) #<==> (B_1_7 + B_0_8 #=2),
   (B_0_8 + B_1_9 #= 2) #<==> (B_1_8 + B_0_9 #=2),(B_1_0 + B_2_1 #= 2) #<==> (B_2_0 + B_1_1 #=2),
   (B_1_1 + B_2_2 #= 2) #<==> (B_2_1 + B_1_2 #=2),(B_1_2 + B_2_3 #= 2) #<==> (B_2_2 + B_1_3 #=2),
   (B_1_3 + B_2_4 #= 2) #<==> (B_2_3 + B_1_4 #=2),(B_1_4 + B_2_5 #= 2) #<==> (B_2_4 + B_1_5 #=2),
   (B_1_5 + B_2_6 #= 2) #<==> (B_2_5 + B_1_6 #=2),(B_1_6 + B_2_7 #= 2) #<==> (B_2_6 + B_1_7 #=2),
   (B_1_7 + B_2_8 #= 2) #<==> (B_2_7 + B_1_8 #=2),(B_1_8 + B_2_9 #= 2) #<==> (B_2_8 + B_1_9 #=2),
   (B_2_0 + B_3_1 #= 2) #<==> (B_3_0 + B_2_1 #=2),(B_2_1 + B_3_2 #= 2) #<==> (B_3_1 + B_2_2 #=2),
   (B_2_2 + B_3_3 #= 2) #<==> (B_3_2 + B_2_3 #=2),(B_2_3 + B_3_4 #= 2) #<==> (B_3_3 + B_2_4 #=2),
   (B_2_4 + B_3_5 #= 2) #<==> (B_3_4 + B_2_5 #=2),(B_2_5 + B_3_6 #= 2) #<==> (B_3_5 + B_2_6 #=2),
   (B_2_6 + B_3_7 #= 2) #<==> (B_3_6 + B_2_7 #=2),(B_2_7 + B_3_8 #= 2) #<==> (B_3_7 + B_2_8 #=2),
   (B_2_8 + B_3_9 #= 2) #<==> (B_3_8 + B_2_9 #=2),(B_3_0 + B_4_1 #= 2) #<==> (B_4_0 + B_3_1 #=2),
   (B_3_1 + B_4_2 #= 2) #<==> (B_4_1 + B_3_2 #=2),(B_3_2 + B_4_3 #= 2) #<==> (B_4_2 + B_3_3 #=2),
   (B_3_3 + B_4_4 #= 2) #<==> (B_4_3 + B_3_4 #=2),(B_3_4 + B_4_5 #= 2) #<==> (B_4_4 + B_3_5 #=2),
   (B_3_5 + B_4_6 #= 2) #<==> (B_4_5 + B_3_6 #=2),(B_3_6 + B_4_7 #= 2) #<==> (B_4_6 + B_3_7 #=2),
   (B_3_7 + B_4_8 #= 2) #<==> (B_4_7 + B_3_8 #=2),(B_3_8 + B_4_9 #= 2) #<==> (B_4_8 + B_3_9 #=2),
   (B_4_0 + B_5_1 #= 2) #<==> (B_5_0 + B_4_1 #=2),(B_4_1 + B_5_2 #= 2) #<==> (B_5_1 + B_4_2 #=2),
   (B_4_2 + B_5_3 #= 2) #<==> (B_5_2 + B_4_3 #=2),(B_4_3 + B_5_4 #= 2) #<==> (B_5_3 + B_4_4 #=2),
   (B_4_4 + B_5_5 #= 2) #<==> (B_5_4 + B_4_5 #=2),(B_4_5 + B_5_6 #= 2) #<==> (B_5_5 + B_4_6 #=2),
   (B_4_6 + B_5_7 #= 2) #<==> (B_5_6 + B_4_7 #=2),(B_4_7 + B_5_8 #= 2) #<==> (B_5_7 + B_4_8 #=2),
   (B_4_8 + B_5_9 #= 2) #<==> (B_5_8 + B_4_9 #=2),(B_5_0 + B_6_1 #= 2) #<==> (B_6_0 + B_5_1 #=2),
   (B_5_1 + B_6_2 #= 2) #<==> (B_6_1 + B_5_2 #=2),(B_5_2 + B_6_3 #= 2) #<==> (B_6_2 + B_5_3 #=2),
   (B_5_3 + B_6_4 #= 2) #<==> (B_6_3 + B_5_4 #=2),(B_5_4 + B_6_5 #= 2) #<==> (B_6_4 + B_5_5 #=2),
   (B_5_5 + B_6_6 #= 2) #<==> (B_6_5 + B_5_6 #=2),(B_5_6 + B_6_7 #= 2) #<==> (B_6_6 + B_5_7 #=2),
   (B_5_7 + B_6_8 #= 2) #<==> (B_6_7 + B_5_8 #=2),(B_5_8 + B_6_9 #= 2) #<==> (B_6_8 + B_5_9 #=2),
   (B_6_0 + B_7_1 #= 2) #<==> (B_7_0 + B_6_1 #=2),(B_6_1 + B_7_2 #= 2) #<==> (B_7_1 + B_6_2 #=2),
   (B_6_2 + B_7_3 #= 2) #<==> (B_7_2 + B_6_3 #=2),(B_6_3 + B_7_4 #= 2) #<==> (B_7_3 + B_6_4 #=2),
   (B_6_4 + B_7_5 #= 2) #<==> (B_7_4 + B_6_5 #=2),(B_6_5 + B_7_6 #= 2) #<==> (B_7_5 + B_6_6 #=2),
   (B_6_6 + B_7_7 #= 2) #<==> (B_7_6 + B_6_7 #=2),(B_6_7 + B_7_8 #= 2) #<==> (B_7_7 + B_6_8 #=2),
   (B_6_8 + B_7_9 #= 2) #<==> (B_7_8 + B_6_9 #=2),(B_7_0 + B_8_1 #= 2) #<==> (B_8_0 + B_7_1 #=2),
   (B_7_1 + B_8_2 #= 2) #<==> (B_8_1 + B_7_2 #=2),(B_7_2 + B_8_3 #= 2) #<==> (B_8_2 + B_7_3 #=2),
   (B_7_3 + B_8_4 #= 2) #<==> (B_8_3 + B_7_4 #=2),(B_7_4 + B_8_5 #= 2) #<==> (B_8_4 + B_7_5 #=2),
   (B_7_5 + B_8_6 #= 2) #<==> (B_8_5 + B_7_6 #=2),(B_7_6 + B_8_7 #= 2) #<==> (B_8_6 + B_7_7 #=2),
   (B_7_7 + B_8_8 #= 2) #<==> (B_8_7 + B_7_8 #=2),(B_7_8 + B_8_9 #= 2) #<==> (B_8_8 + B_7_9 #=2),
   (B_8_0 + B_9_1 #= 2) #<==> (B_9_0 + B_8_1 #=2),(B_8_1 + B_9_2 #= 2) #<==> (B_9_1 + B_8_2 #=2),
   (B_8_2 + B_9_3 #= 2) #<==> (B_9_2 + B_8_3 #=2),(B_8_3 + B_9_4 #= 2) #<==> (B_9_3 + B_8_4 #=2),
   (B_8_4 + B_9_5 #= 2) #<==> (B_9_4 + B_8_5 #=2),(B_8_5 + B_9_6 #= 2) #<==> (B_9_5 + B_8_6 #=2),
   (B_8_6 + B_9_7 #= 2) #<==> (B_9_6 + B_8_7 #=2),(B_8_7 + B_9_8 #= 2) #<==> (B_9_7 + B_8_8 #=2),
   (B_8_8 + B_9_9 #= 2) #<==> (B_9_8 + B_8_9 #=2),
    labeling([ff], [B_0_0, B_0_1, B_0_2, B_0_3, B_0_4, B_0_5, B_0_6, B_0_7, B_0_8, B_0_9, B_1_0, B_1_1, B_1_2, B_1_3, B_1_4, B_1_5, B_1_6, B_1_7, B_1_8, B_1_9, B_2_0, B_2_1, B_2_2, B_2_3, B_2_4, B_2_5, B_2_6, B_2_7, B_2_8, B_2_9, B_3_0, B_3_1, B_3_2, B_3_3, B_3_4, B_3_5, B_3_6, B_3_7, B_3_8, B_3_9, B_4_0, B_4_1, B_4_2, B_4_3, B_4_4, B_4_5, B_4_6, B_4_7, B_4_8, B_4_9, B_5_0, B_5_1, B_5_2, B_5_3, B_5_4, B_5_5, B_5_6, B_5_7, B_5_8, B_5_9, B_6_0, B_6_1, B_6_2, B_6_3, B_6_4, B_6_5, B_6_6, B_6_7, B_6_8, B_6_9, B_7_0, B_7_1, B_7_2, B_7_3, B_7_4, B_7_5, B_7_6, B_7_7, B_7_8, B_7_9, B_8_0, B_8_1, B_8_2, B_8_3, B_8_4, B_8_5, B_8_6, B_8_7, B_8_8, B_8_9, B_9_0, B_9_1, B_9_2, B_9_3, B_9_4, B_9_5, B_9_6, B_9_7, B_9_8, B_9_9]).
:- solve(X), write(X), nl.