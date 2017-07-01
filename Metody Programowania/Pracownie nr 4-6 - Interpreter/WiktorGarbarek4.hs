{-# LANGUAGE Safe #-}
module WiktorGarbarek (typecheck, eval) where

import AST
import DataTypes

-- Possible_Types p are types that can be used in our program (Bt - Bool_type, It - Integer_type, Err - Error), p stores position given by parser
-- Possible_Evaluations - similar to above - ZeroDivision is error given by mod 0 or div 0 operation

data Possible_Types p = Bt p | It p | Err p String
data Possible_Evaluations = B Bool | I Integer | ZeroDivision 

-- member_type is used in b_typecheck to give us type of variable var
-- var is uninitialized when it does not occur on the list 

member_type :: p -> [(Var, Possible_Types p)] -> Var -> Possible_Types p
member_type p [] var = Err p ("Unknown variable: " ++ var)
member_type p ((x,y):xs) var = 
    case var == x of
        True -> y
        False -> member_type p xs var

-- member_value is used in b_eval to give value int of variable var
-- we assume that (v1,_) is on the list (because of earlier typecheck)

member_value :: [(Var, Possible_Evaluations)] -> Var -> Possible_Evaluations

member_value ((val, int):xs) var = 
    case (val == var) of
        True -> int
        False -> member_value xs var

typecheck :: [Var] -> Expr p -> TypeCheckResult p
typecheck var expr =
    let var_ext = map aux var where
        aux x = (x, It (getData expr))
    in case b_typecheck var_ext expr of
        It p -> Ok
        Bt p -> Error p ("TypeCheckError: Invalid type of program - Given: Bool, Expected: Integer")
        Err p m -> Error p m

b_typecheck :: [(Var, Possible_Types p)] -> Expr p -> Possible_Types p

b_typecheck vars (EVar p var) = member_type p vars var
b_typecheck _ (ENum p _) = It p
b_typecheck _ (EBool p _) = Bt p
b_typecheck vars (EUnary p unop e1) =
    case b_typecheck vars e1 of
        Bt p -> case unop of
            UNot -> Bt p
            UNeg -> Err p ("TypeCheckError: Integer operator - was given bool expression")
        It p -> case unop of
            UNeg -> It p
            UNot -> Err p ("TypeCheckError: Bool operator 'not' was given integer expression")
        Err p m -> Err p m
b_typecheck vars (EBinary p binop e1 e2) =
    let x = b_typecheck vars e1
    in let y = b_typecheck vars e2 
    in case (x, y) of
            (Err p1 m, _) -> Err p1 m
            (_, Err p1 m) -> Err p1 m
            (Bt _, Bt _) -> case binop of
                BAnd -> Bt p
                BOr -> Bt p
                _ -> Err p ("TypeCheckError: Integer operator " ++ show binop ++ " was given two bool expressions")
            (It _, It _) -> case binop of
                BEq -> Bt p
                BNeq -> Bt p
                BLt -> Bt p 
                BGt -> Bt p
                BLe -> Bt p
                BGe -> Bt p
                BAdd -> It p 
                BSub -> It p
                BMul -> It p
                BDiv -> It p
                BMod -> It p
                _ -> Err p ("TypeCheckError: Bool operator " ++ show binop ++ " was given two integer expressions")
            _ -> Err p ("TypeCheckError: Arguments of binary operator " ++ show binop ++ " have different types")

b_typecheck vars (ELet p var e1 e2) =
    case b_typecheck vars e1 of
        Err p1 m -> Err p1 m
        t -> b_typecheck ((var,t):vars) e2

b_typecheck vars (EIf p e0 e1 e2) =
    case b_typecheck vars e0 of 
        Bt p1 -> let x = b_typecheck vars e1
            in let y = b_typecheck vars e2
            in case (x,y) of
                (Err p2 m, _) -> Err p2 m
                (_, Err p2 m) -> Err p2 m
                (Bt _, Bt _) -> x
                (It _, It _) -> x
                _ -> Err (getData e1) ("TypeCheckError: Branches of If expression have different types")
        Err p1 m -> Err p1 m
        _ -> Err p ("TypeCheckError: Condition is not a bool expression")

eval :: [(Var,Integer)] -> Expr p -> EvalResult
 
eval vars expr = 
    let vars_big = map aux vars where
        aux (var, int) = (var, I int)
    in case b_eval vars_big expr of 
        I val -> Value val
        _ -> RuntimeError

b_eval :: [(Var, Possible_Evaluations)] -> Expr p -> Possible_Evaluations

b_eval env (EVar _ var) = member_value env var
b_eval _ (ENum _ int) = I int
b_eval _ (EBool _ bool) = B bool
b_eval env (EUnary _ unop expr) =
    case b_eval env expr of
        ZeroDivision -> ZeroDivision
        I v -> I (- v)
        B v -> B (not v)
      
b_eval env (EBinary _ binop e1 e2) = 
    case b_eval env e1 of 
        ZeroDivision -> ZeroDivision
        I v1 -> case b_eval env e2 of
            ZeroDivision -> ZeroDivision
            I v2 -> case binop of 
                
                BEq -> B (v1 == v2)
                BNeq -> B (v1 /= v2)
                BLt -> B (v1 < v2)
                BGt -> B (v1 > v2)
                BLe -> B (v1 <= v2)
                BGe -> B (v1 >= v2)

                BAdd -> I (v1 + v2)
                BSub -> I (v1 - v2)
                BMul -> I (v1 * v2)
                BDiv -> case v2 == 0 of
                    False -> I (v1 `div` v2)
                    True -> ZeroDivision
                BMod -> case v2 == 0 of
                    False -> I (v1 `mod` v2)
                    True -> ZeroDivision
        B p1 -> case b_eval env e2 of 
            ZeroDivision -> ZeroDivision 
            B p2 -> case binop of
                BAnd -> B (p1 && p2)
                BOr -> B (p1 || p2)

b_eval env (ELet _ var e1 e2) =
    case b_eval env e1 of
        ZeroDivision -> ZeroDivision    
        av -> b_eval ((var, av):env) e2

b_eval env (EIf _ e0 e1 e2) =
    case b_eval env e0 of
        ZeroDivision -> ZeroDivision
        B True -> b_eval env e1
        B False -> b_eval env e2