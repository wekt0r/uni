-- Wymagamy, by moduł zawierał tylko bezpieczne funkcje
{-# LANGUAGE Safe #-}
-- Definiujemy moduł zawierający testy.
-- Należy zmienić nazwę modułu na {Imie}{Nazwisko}Tests gdzie za {Imie}
-- i {Nazwisko} należy podstawić odpowiednio swoje imię i nazwisko
-- zaczynające się wielką literą oraz bez znaków diakrytycznych.
module WiktorGarbarekTests(tests) where

-- Importujemy moduł zawierający typy danych potrzebne w zadaniu
import DataTypes

-- Lista testów do zadania
-- Należy uzupełnić jej definicję swoimi testami
tests :: [Test]
tests =
  [ Test "inc"      (SrcString "input x in x + 1") (Eval [42] (Value 43))
  , Test "undefVar" (SrcString "x")                TypeError
  , Test "lazyIf_with_vars"   (SrcString "input x in if true then x + 5 else 5 div 0") (Eval [5] (Value 10))
  , Test "lazyIf"   (SrcString "if true then 1 else 1 div 0") (Eval [] (Value 1))
  , Test "lazyIf_with_false" (SrcString "if false then 5 div 0 else 1") (Eval [] (Value 1))
  , Test "lazyIf_dependent_from_var" (SrcString "input x in if x >= 0 then x * 1 else x div 0") (Eval [42] (Value 42))
  , Test "let_test" (SrcString "input x in let t = 5 in t*t + x") (Eval [17] (Value 42))
  , Test "tricky_arithmetic" (SrcString "10 + -7") (Eval [] (Value 3))
  , Test "lots_of_minuses" (SrcString "10 - - - - 7") (Eval [] (Value 17))
  , Test "proper_or" (SrcString "input a in if a > 0 or a < 0 then 14*3 else 42 div 7") (Eval [-10] (Value 42))
  , Test "proper_and" (SrcString "input a b in if a < 0 and b >= 0 then 2*2 else 5 + 5") (Eval [1, 1] (Value 10))
  , Test "minus_bool" (SrcString "input a in if - true then 1 else 0") TypeError
  , Test "plus_associativity" (SrcString "input a b in 5 + b + a + 2 + 1") (Eval [3,4] (Value 15))
  , Test "or_associativity" (SrcString "if false or false or false or true then 1 else 0") (Eval [] (Value 1))
  , Test "variable_used_more_than_once" (SrcString "input a b in if a > 0 then a*b + a*5 + a else b*a + b*5 + b") (Eval [1,1000] (Value 1006))
  , Test "unused_variable" (SrcString "input a b in a*2") (Eval [5,2031] (Value 10)) 
  , Test "basic_arithmetic" (SrcString "100*2 + 10*5 + 6") (Eval [] (Value 256))
  , Test "arithmetic_with_bool_unary" (SrcString "not 100*2 + 3") TypeError
  , Test "arithmetic_with_bool_binary" (SrcString "(200*3 or 3) and 5") TypeError
  , Test "more_variables" (SrcString "input x y z in x + y + z") (Eval [1,2,3] (Value 6))
  , Test "variables_with_undefined" (SrcString "input x y in x*y + z") TypeError
  , Test "proper_order_of_let" (SrcString "let x = 5 in let x = x + 10 in x") (Eval [] (Value 15))
  , Test "is_number_true" (SrcString "if 5 then 5 else 5") TypeError
  , Test "normal_if" (SrcString "input var in if var > 1 then 10 else 5 + var") (Eval [0] (Value 5))
  , Test "trivial_associativity" (SrcString "input x in x + x * x") (Eval [2] (Value 6))
  , Test "number_as_bool" (SrcString "input a in if a or true then a else a + 1") TypeError
  , Test "negation" (SrcString "input x in if not false then 5 + x else 5 - x") (Eval [1] (Value 6))
  , Test "double_negation" (SrcString "input x in if not not false then 5 + x else 5 - x") (Eval [1] (Value 4))
  , Test "simple_arithmetic_with_parentheses" (SrcString "(2 + 3 + 4)*5 + 1") (Eval [] (Value 46))
  , Test "equality_operators_with_bool" (SrcString "if true <> false then 1 else 0") TypeError
  , Test "nested_let" (SrcString "let x = 2 in let x = 2*x in let x = x + 5 in let x = 3*x in x + 1") (Eval [] (Value 28))
   ]