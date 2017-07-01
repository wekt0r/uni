{-# LANGUAGE Safe #-}
-- WERSJA DLA PRACOWNI NR 4 // COMPILER FOR TASK NO 4
module WiktorGarbarekCompiler(compile) where

import AST
import MacroAsm
import Control.Monad.State

freshlabel :: State Label Label

freshlabel = do
    l <- get
    put $ l+1 
    return l

-- freshlabel is to generate unique labels for jumps

compile :: [FunctionDef p] -> [Var] -> Expr p -> [MInstr]
compile _ env expr =
    let env_stack = zip env [0..]
    in (evalState (b_compile env_stack expr) 1) ++ [MRet]

find_on_stack :: [(Var, Int)] -> Var -> Int
find_on_stack [] _ = -1
find_on_stack ((v,n):vs) var = if var == v then n else find_on_stack vs var

-- we store variables' positions on stack on [(Var,Int)] list
-- actually we are sure that variable is on the list, empty list case is useless, but is there to keep solution elegant

b_compile :: [(Var, Int)] -> Expr p -> State Label [MInstr]

b_compile _ (ENum p int) = return $ [MConst int]

b_compile stack (EVar p var) = let n = find_on_stack stack var in return $ [MGetLocal n]

b_compile _ (EBool p bool) = 
    case bool of
        True -> return $ [MConst (-1)]
        False -> return $ [MConst 0]
-- true is -1 because of implementation of not (it is toggling all bits, so not (-1) is 0 and vice versa)

b_compile stack (EUnary p op e1) = do
    m1 <- b_compile stack e1
    return $ m1 ++ case op of
        UNot -> [MNot]
        UNeg -> [MNeg]

b_compile stack (EBinary p op e1 e2) =
    let new_stack = map (\(v,n) -> (v, n+1)) stack
    in do
        l1 <- freshlabel
        l2 <- freshlabel 
        m1 <- b_compile stack e1
        m2 <- b_compile new_stack e2 
        return $ m1 ++ [MPush] ++ m2 ++ case op of
            BAnd -> [MAnd]
            BOr -> [MOr]
            BEq -> [MBranch MC_NE l1, MConst (-1), MJump l2, MLabel l1, MConst 0, MLabel l2]
            BNeq ->[MBranch MC_EQ l1, MConst (-1), MJump l2, MLabel l1, MConst 0, MLabel l2]
            BLt -> [MBranch MC_GE l1, MConst (-1), MJump l2, MLabel l1, MConst 0, MLabel l2]
            BGt -> [MBranch MC_LE l1, MConst (-1), MJump l2, MLabel l1, MConst 0, MLabel l2]
            BLe -> [MBranch MC_GT l1, MConst (-1), MJump l2, MLabel l1, MConst 0, MLabel l2]
            BGe -> [MBranch MC_LT l1, MConst (-1), MJump l2, MLabel l1, MConst 0, MLabel l2]
            BAdd -> [MAdd]
            BSub -> [MSub]
            BMul -> [MMul]
            BDiv -> [MDiv]
            BMod -> [MMod]

-- comparison operators are implemented as "small ifs" due to instructions we can use
-- due to jumping to "false branch", every operator puts in code its opposing operator
-- ie. if we have 0 <= 1 then if 0 > 1 we jump to "false value"
-- of course we could switch branches and choose the same operator
-- but that doesn't seem to be elegant  

b_compile stack (ELet p var e1 e2) =
    let new_stack = (var, 0):(map (\(v,n) -> (v,n+1)) stack)
    in do
        m1 <- b_compile stack e1
        m2 <- b_compile new_stack e2
        return $ m1 ++ [MPush] ++ m2 ++ [MPopN 1]

b_compile stack (EIf p e1 e2 e3) = do
    l1 <- freshlabel
    l2 <- freshlabel
    m1 <- b_compile stack e1
    m2 <- b_compile stack e2
    m3 <- b_compile stack e3
    return $ m1 ++ [MBranch MC_Z l1] ++ m2 ++ [MJump l2, MLabel l1] ++ m3 ++ [MLabel l2]