{-# LANGUAGE Safe #-}
module WiktorGarbarek (typecheck, eval) where

import AST
import DataTypes

data ExtMaybe p = ExtJust Type | ExtNothing p String

data Evaluation = VInt Integer | VBool Bool | VUnit | VPair Evaluation Evaluation | VList [Evaluation] | ZeroDivision

-- find_fun takes [f1, f2, ..., fn] and name and returns Just fi such that funcName fi = name or Nothing otherwise
find_fun :: [FunctionDef p] -> FSym -> Maybe (FunctionDef p)
find_fun [] name = Nothing
find_fun (f1:fs) name = 
    if funcName f1 == name then Just f1 else find_fun fs name  

-- function_list_check takes [f1,...,fn] (list of all functions) twice and returns Ok if all functions are correct
-- first [f1, ..., fn] is to know what functions are in program
-- second is to order functions which we are checking
function_list_check :: [FunctionDef p] -> [FunctionDef p] -> TypeCheckResult p
function_list_check env fs =
    case fs of
        [] -> Ok
        (function:rest) -> case b_typecheck env [(funcArg function, ExtJust (funcArgType function))] (funcBody function) of
                    ExtNothing p m -> Error p m
                    ExtJust a -> if a == funcResType function 
                        then function_list_check env rest 
                        else Error (funcPos function) ("TypeCheckError: Wrong type of result of " ++ (funcName function) ++ " function")

member_type :: p -> [(Var, ExtMaybe p)] -> Var -> ExtMaybe p

member_type p [] var = ExtNothing p ("TypeCheckError: Uninitialized variable" ++ var)
member_type p ((val, kind):xs) var = if val == var then kind else member_type p xs var        

typecheck :: [FunctionDef p] -> [Var] -> Expr p -> TypeCheckResult p
typecheck fs vars input =
    case function_list_check fs fs of
        Error p m -> Error p m
        _ -> let vars_typed = map aux vars where
                    aux var = (var, ExtJust TInt)
                in case b_typecheck fs vars_typed input of
                    ExtJust TInt -> Ok
                    ExtJust _ -> Error (getData input) ("TypeCheckError: Invalid type of program")
                    ExtNothing p m -> Error p m

b_typecheck :: [FunctionDef p] -> [(Var, ExtMaybe p)] -> Expr p -> ExtMaybe p

b_typecheck fs vars (EVar p var) = member_type p vars var
b_typecheck fs _ (ENum p _) = ExtJust TInt
b_typecheck fs _ (EBool p _) = ExtJust TBool
b_typecheck fs vars (EUnary p unop e1) =
    case b_typecheck fs vars e1 of
        ExtNothing p m -> ExtNothing p m
        ExtJust TBool -> case unop of
            UNot -> ExtJust TBool
            UNeg -> ExtNothing p ("TypeCheckError: Integer operator '-' was given bool expression")
        ExtJust TInt -> case unop of
            UNeg -> ExtJust TInt
            UNot -> ExtNothing p ("TypeCheckError: Bool operator 'not' was given integer expression")
        _ -> ExtNothing p ("TypeCheckError: Unary operator was applied to type different than Bool or Integer")

b_typecheck fs vars (EBinary p binop e1 e2) =
    let x = b_typecheck fs vars e1
    in let y = b_typecheck fs vars e2 
    in case (x, y) of
            (ExtNothing p1 m, _) -> ExtNothing p1 m
            (_, ExtNothing p1 m) -> ExtNothing p1 m
            (ExtJust TBool, ExtJust TBool) -> case binop of
                BAnd -> ExtJust TBool
                BOr -> ExtJust TBool
                _ -> ExtNothing p ("TypeCheckError: Integer operator " ++ show binop ++ " was given two bool expressions")
            (ExtJust TInt, ExtJust TInt) -> case binop of
                BEq -> ExtJust TBool
                BNeq -> ExtJust TBool
                BLt -> ExtJust TBool 
                BGt -> ExtJust TBool
                BLe -> ExtJust TBool
                BGe -> ExtJust TBool
                BAdd -> ExtJust TInt 
                BSub -> ExtJust TInt
                BMul -> ExtJust TInt
                BDiv -> ExtJust TInt
                BMod -> ExtJust TInt
                _ -> ExtNothing p ("TypeCheckError: Bool operator " ++ show binop ++ " was given two integer expressions")
            _ -> ExtNothing p ("TypeCheckError: Arguments of binary operator " ++ show binop ++ " have wrong types")

b_typecheck fs vars (ELet p var e1 e2) =
    case b_typecheck fs vars e1 of
        ExtNothing p1 m -> ExtNothing p1 m
        t -> b_typecheck fs ((var,t):vars) e2

b_typecheck fs vars (EIf p e0 e1 e2) =
    case b_typecheck fs vars e0 of 
        ExtJust TBool -> case (b_typecheck fs vars e1, b_typecheck fs vars e2) of
                (ExtNothing p2 m, _) -> ExtNothing p2 m
                (_, ExtNothing p2 m) -> ExtNothing p2 m
                (ExtJust t1, ExtJust t2) -> if t1 == t2 
                    then ExtJust t1 
                    else ExtNothing (getData e1) ("TypeCheckError: Branches of If expression have different types")
        ExtNothing p1 m -> ExtNothing p1 m
        _ -> ExtNothing p ("TypeCheckError: Condition is not a bool expression")


b_typecheck fs vars (EApp p name e1) = 
    case find_fun fs name of
        Nothing -> ExtNothing p ("TypeCheckError: Undefined function " ++ name)
        Just f1 -> case b_typecheck fs vars e1 of
            ExtNothing p m -> ExtNothing p m
            ExtJust t -> if t == funcArgType f1 
                then ExtJust $ funcResType f1 
                else ExtNothing p ("TypeCheckError: Argument given to function " ++ name ++" has invalid type")

b_typecheck _ _ (EUnit _) = ExtJust TUnit
b_typecheck fs vars (EPair p e1 e2) = 
    case b_typecheck fs vars e1 of
        ExtNothing p1 m -> ExtNothing p1 m
        ExtJust t1 -> case b_typecheck fs vars e2 of
            ExtNothing p2 m2 -> ExtNothing p2 m2
            ExtJust t2 -> ExtJust $ TPair t1 t2

b_typecheck fs vars (EFst p e1) = 
    case b_typecheck fs vars e1 of
        ExtNothing p1 m -> ExtNothing p1 m
        ExtJust (TPair t1 _) -> ExtJust t1
        _ -> ExtNothing p ("TypeCheckError: Argument given to function fst is not a pair")

b_typecheck fs vars (ESnd p e1) =
    case b_typecheck fs vars e1 of
        ExtNothing p1 m -> ExtNothing p1 m
        ExtJust (TPair _ t2) -> ExtJust t2
        _ -> ExtNothing p ("TypeCheckError: Argument given to function snd is not a pair")

b_typecheck fs vars (ENil p t) = case t of 
        TList _ -> ExtJust t
        _ -> ExtNothing p ("TypeCheckError: List has to have list type")

b_typecheck fs vars (ECons p e1 e2) = 
    case b_typecheck fs vars e2 of
        ExtNothing p1 m1 -> ExtNothing p1 m1
        ExtJust (TList tt) -> case b_typecheck fs vars e1 of
            ExtNothing p2 m2 -> ExtNothing p2 m2
            ExtJust th -> if tt == th 
                then ExtJust (TList tt) 
                else ExtNothing p ("TypeCheckError: List and its element have mismatching types")
        _ -> ExtNothing p ("TypeCheckError: List constructor was called on non-list expression")

b_typecheck fs vars (EMatchL p e1 e2 (head,tail,e3)) = 
    case b_typecheck fs vars e1 of
        ExtNothing p1 m1 -> ExtNothing p1 m1
        ExtJust (TList t) -> case (b_typecheck fs vars e2, b_typecheck fs ((head, ExtJust t):(tail, ExtJust (TList t)):vars) e3) of
                (ExtNothing p1 m1, _) -> ExtNothing p1 m1
                (_, ExtNothing p1 m1) -> ExtNothing p1 m1
                (ExtJust a, ExtJust b) -> case a == b of 
                    True -> ExtJust a
                    _ -> ExtNothing p ("TypeCheckError: Branches of match-statement have mismatching types")
        _ -> ExtNothing p ("TypeCheckError: Match-statement was called on non-list expression")



-- Funkcja obliczająca wyrażenia
-- Dla wywołania eval fs input e przyjmujemy, że dla każdej pary (x, v)
-- znajdującej się w input, wartość zmiennej x wynosi v.
-- Możemy założyć, że definicje funckcji fs oraz wyrażenie e są dobrze
-- typowane, tzn. typecheck fs (map fst input) e = Ok
-- UWAGA: to nie jest jeszcze rozwiązanie; należy zmienić jej definicję.
eval :: [FunctionDef p] -> [(Var,Integer)] -> Expr p -> EvalResult
eval fs vars input =
    let vars_ext = map aux vars where
        aux (var,val) = (var, VInt val)
    in case b_eval fs vars_ext input of
        VInt value -> Value value
        _ -> RuntimeError


member_value :: [(Var, Evaluation)] -> Var -> Evaluation

member_value ((key, value):xs) var = 
    case (key == var) of
        True -> value 
        False -> member_value xs var

b_eval :: [FunctionDef p] -> [(Var, Evaluation)] -> Expr p -> Evaluation

b_eval fs env (EVar _ var) = member_value env var
b_eval fs _ (ENum _ int) = VInt int
b_eval fs _ (EBool _ bool) = VBool bool
b_eval fs env (EUnary _ unop expr) =
    case b_eval fs env expr of
        ZeroDivision -> ZeroDivision
        VInt v -> VInt (- v)
        VBool v -> VBool (not v)
      
b_eval fs env (EBinary _ binop e1 e2) = 
    case b_eval fs env e1 of 
        ZeroDivision -> ZeroDivision
        VInt v1 -> case b_eval fs env e2 of
            ZeroDivision -> ZeroDivision
            VInt v2 -> case binop of 
                
                BEq -> VBool (v1 == v2)
                BNeq -> VBool (v1 /= v2)
                BLt -> VBool (v1 < v2)
                BGt -> VBool (v1 > v2)
                BLe -> VBool (v1 <= v2)
                BGe -> VBool (v1 >= v2)

                BAdd -> VInt (v1 + v2)
                BSub -> VInt (v1 - v2)
                BMul -> VInt (v1 * v2)
                BDiv -> case v2 == 0 of
                    False -> VInt (v1 `div` v2)
                    True -> ZeroDivision
                BMod -> case v2 == 0 of
                    False -> VInt (v1 `mod` v2)
                    True -> ZeroDivision
        VBool p1 -> case b_eval fs env e2 of 
            ZeroDivision -> ZeroDivision 
            VBool p2 -> case binop of
                BAnd -> VBool (p1 && p2)
                BOr -> VBool (p1 || p2)

b_eval fs env (ELet _ var e1 e2) =
    case b_eval fs env e1 of
        ZeroDivision -> ZeroDivision    
        av -> b_eval fs ((var, av):env) e2

b_eval fs env (EIf _ e0 e1 e2) =
    case b_eval fs env e0 of
        ZeroDivision -> ZeroDivision
        VBool True -> b_eval fs env e1
        VBool False -> b_eval fs env e2

b_eval fs env (EApp p name expr) =
    let Just f1 = find_fun fs name in case b_eval fs env expr of
        ZeroDivision -> ZeroDivision
        argument -> b_eval fs [(funcArg f1, argument)] (funcBody f1)

b_eval _ _ (EUnit p) = VUnit

b_eval fs env (EPair p e1 e2) = 
    case (b_eval fs env e1, b_eval fs env e2) of
        (ZeroDivision, _) -> ZeroDivision
        (_, ZeroDivision) -> ZeroDivision
        (a,b) -> VPair a b

b_eval fs env (EFst p e1) = 
    case b_eval fs env e1 of 
        ZeroDivision -> ZeroDivision
        VPair a b -> a

b_eval fs env (ESnd p e1) = 
    case b_eval fs env e1 of 
        ZeroDivision -> ZeroDivision
        VPair a b -> b

b_eval fs env (ENil p _) = VList []

b_eval fs env (ECons p e1 e2) = 
    case b_eval fs env e2 of
        ZeroDivision -> ZeroDivision
        VList xs -> case b_eval fs env e1 of
            ZeroDivision -> ZeroDivision
            x -> VList (x:xs)

b_eval fs env (EMatchL p e1 e2 (head,tail,e3)) = 
    case b_eval fs env e1 of
            ZeroDivision -> ZeroDivision
            VList [] -> b_eval fs env e2
            VList (x:xs) -> b_eval fs ((tail,VList xs):(head,x):env) e3






